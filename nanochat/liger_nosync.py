"""Training-only, no-padding adapter for the pinned Liger 0.8.0 CE kernels.

The caller must validate every CPU-packed row with the same vocabulary before
H2D. This deliberately is not a general-purpose CrossEntropyLoss replacement.
"""

from importlib.metadata import version

import torch
import triton
import triton.language as tl

from liger_kernel.ops.cross_entropy import MAX_FUSED_SIZE, liger_cross_entropy_kernel
from liger_kernel.ops.utils import element_mul_kernel
from nanochat.loss_reduction import rounded_loss_sum


@triton.jit
def _element_mul_unless_unit_kernel(
    X_ptr,
    X_stride,
    grad_output_ptr,
    n_cols,
    BLOCK_SIZE: tl.constexpr,
):
    # This is GPU control flow over a device scalar, not a host scalar read.
    # Leave saved gradient storage untouched for the common unit upstream.
    # A nested JIT call retains the pinned kernel's exact non-unit arithmetic,
    # row addressing and masks; it is not a second host kernel launch.
    grad_output = tl.load(grad_output_ptr)
    if grad_output != 1.0:
        element_mul_kernel(X_ptr, X_stride, grad_output_ptr, n_cols, BLOCK_SIZE)


class _NoPaddingCrossEntropy(torch.autograd.Function):
    @staticmethod
    def forward(ctx, logits, targets):
        # These checks inspect metadata only; the dataloader checks token values
        # on CPU before copying to CUDA. No CUDA scalar is read by Python here.
        if logits.device.type != "cuda" or targets.device != logits.device:
            raise ValueError("no-sync Liger CE requires logits and targets on the same CUDA device")
        if logits.ndim != 2 or targets.ndim != 1 or logits.shape[0] != targets.numel():
            raise ValueError("expected logits [N,V] and targets [N]")
        if logits.shape[0] == 0 or logits.shape[1] == 0:
            raise ValueError("empty logits/targets are unsupported")
        if logits.dtype not in (torch.bfloat16, torch.float16, torch.float32):
            raise TypeError("unsupported logit dtype")
        if targets.dtype != torch.int64:
            raise TypeError("targets must be int64")
        if logits.stride(-1) != 1:
            # Autograd.Function.forward runs without grad tracking: a hidden
            # contiguous copy here would lose requires_grad and add a logits
            # allocation. GPT's padded head slices already have stride 1.
            raise ValueError("no-sync Liger CE requires last-dimension logit stride 1")
        if targets.stride(-1) != 1:
            targets = targets.contiguous()
        n_rows, vocab_size = logits.shape
        block_size = min(MAX_FUSED_SIZE, triton.next_power_of_2(vocab_size))
        losses = torch.zeros(n_rows, dtype=logits.dtype, device=logits.device)
        # Import and launch the ORIGINAL kernel. Keep normalization inside the
        # kernel before BF16 storage, followed by the original torch.sum.
        liger_cross_entropy_kernel[(n_rows,)](
            X_ptr=logits,
            X_stride=logits.stride(-2),
            Y_ptr=targets,
            Y_stride=targets.stride(-1),
            weight_ptr=None,
            loss_ptr=losses,
            z_loss_ptr=None,
            loss_stride=losses.stride(-1),
            token_accuracy_ptr=None,
            token_accuracy_stride=0,
            predicted_tokens_ptr=None,
            predicted_tokens_stride=0,
            n_cols=vocab_size,
            n_non_ignore=targets.numel(),
            sum_non_ignore_weight=targets.numel(),
            weight_sum=0.0,
            ignore_index=-1,
            lse_square_scale=0.0,
            label_smoothing=0.0,
            reduction="mean",
            softcap=15,
            RETURN_Z_LOSS=False,
            RETURN_TOKEN_ACCURACY=False,
            RETURN_PREDICTED_TOKENS=False,
            BLOCK_SIZE=block_size,
            HAS_WEIGHT=False,
            HAS_SOFTCAPPING=True,
            HAS_GRADIENTS=logits.requires_grad,
            num_warps=32,
        )
        if logits.requires_grad:
            # Match Liger's storage reuse; do not save another logits allocation.
            ctx.save_for_backward(logits.detach())
        return rounded_loss_sum(losses)

    @staticmethod
    def backward(ctx, grad_output):
        (logit_gradient,) = ctx.saved_tensors
        if grad_output.ndim != 0:
            raise ValueError("mean CE requires a scalar upstream gradient")
        n_rows, vocab_size = logit_gradient.shape
        # Launch for every scalar without asking Python to read its value.
        # Each GPU program skips gradient reads/writes when the scalar is 1;
        # other values use the original Liger multiplication inside the branch.
        _element_mul_unless_unit_kernel[(n_rows,)](
            logit_gradient,
            logit_gradient.stride(-2),
            grad_output,
            vocab_size,
            BLOCK_SIZE=min(MAX_FUSED_SIZE, triton.next_power_of_2(vocab_size)),
            num_warps=32,
        )
        return logit_gradient, None


class LigerNoSyncCrossEntropyLoss(torch.nn.Module):
    """Fixed mean/softcap-15 loss for CPU-validated, unpadded training targets.

    Like stock Liger, forward consumes logits as scratch gradient storage. Use
    a single backward per forward, without higher-order derivatives or reusing
    the consumed logits. The logits' last dimension must have stride 1; padded
    row strides are supported. Evaluation uses the ordinary GPT evaluation path.
    """

    def __init__(self, vocab_size, *, targets_validated_on_cpu=False):
        super().__init__()
        if version("liger-kernel") != "0.8.0":
            raise RuntimeError("no-sync experiment requires liger-kernel==0.8.0")
        if torch.version.hip is not None:
            raise RuntimeError("no-sync experiment is pinned to NVIDIA CUDA")
        if not targets_validated_on_cpu:
            raise ValueError("no-sync CE requires the CPU token-bounds validation contract")
        if not isinstance(vocab_size, int) or vocab_size <= 0:
            raise ValueError("vocab_size must be a positive integer")
        self.vocab_size = vocab_size

    def forward(self, logits, targets):
        if logits.shape[-1] != self.vocab_size:
            raise ValueError("logit width differs from the CPU-validated vocabulary")
        return _NoPaddingCrossEntropy.apply(logits, targets)
