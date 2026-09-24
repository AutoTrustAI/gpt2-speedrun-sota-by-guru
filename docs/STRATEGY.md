# Training strategy

The published result trains a GPT-style autoregressive language model from scratch to the Time-to-GPT-2 CORE target. Nanochat is the implementation framework.

## Model and execution

| Component | Setting |
|---|---|
| Transformer layers | 22 |
| Model width / attention heads | 1,408 / 11 |
| MLP hidden width | 4,864 |
| Vocabulary | 49,152 |
| Context / attention window pattern | 2,048 / SSSL |
| Total parameters | 1,375,503,474 |
| Matrix computation | Tensorwise FP8 with BF16 surrounding computation |
| Attention | FlashAttention 3 |
| Training loss | Original Liger fused softcapped cross entropy |
| Optimizer | Original Muon/AdamW implementation |
| Per-GPU batch / global tokens | 32 sequences / 524,288 tokens |
| Training data | ClimbMix, 170 training shards; original held-out shard |

## Capacity and horizon

Reducing the MLP width from 5,120 to 4,864 removes 15,859,712 parameters and approximately 2.56% of the model's estimated per-token FLOPs. Depth, attention width, vocabulary and context length stay fixed. At the same 9,841-update horizon, measured time changes from 73.4972 to 72.2419 minutes. CORE changes from 0.263907 to 0.259212, which still exceeds 0.256525. Validation BPB changes from 0.723137 to 0.724029.

The 9,841-update recipe sees 5,159,518,208 tokens. The explicit iteration count sets the training horizon; `target_param_data_ratio=9.20` remains an input to the original hyperparameter scaling. There are 40 warmup steps, a 0.65 warmdown fraction and a final learning-rate fraction of 0.05. Weight decay and optimizer equations are unchanged.

## Learning-rate inputs

| Parameter group | Learning-rate input |
|---|---:|
| Token embeddings | 0.3 |
| Output projection | 0.008 |
| Matrix parameters | 0.02 |
| Scalar parameters | 0.5 |
| Weight decay | 0.28 |

The implementation applies its original scaling rules to these inputs. [Exact commands and configurations](../reproduction/recipes.json) are provided, along with byte hashes for the frozen source files.

## Evaluation

The checkpoint is restored into the same MLP4864 configuration. Complete CORE uses all 22 tasks and `--max-per-task=-1`; BPB uses 20,971,520 tokens per split. The publication selects completed runs that cross the CORE threshold.

The shipped model and optimizer source is copied from the recorded training revision. The unverified compiler-pass draft is not part of this implementation.
