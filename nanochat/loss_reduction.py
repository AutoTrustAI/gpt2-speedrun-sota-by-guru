"""An opaque ATen reduction preserving the loss tensor's output rounding."""

import torch


@torch.library.custom_op("nanochat::rounded_loss_sum", mutates_args=())
def rounded_loss_sum(losses: torch.Tensor) -> torch.Tensor:
    # Stock Liger returns sum in the input dtype before GPT casts to float32.
    # Keep this materialization outside Inductor fusion: eliminating the BF16
    # scalar intermediate changes the returned loss, even with identical rows.
    return torch.sum(losses)


@rounded_loss_sum.register_fake
def _rounded_loss_sum_fake(losses):
    return torch.empty((), device=losses.device, dtype=losses.dtype)
