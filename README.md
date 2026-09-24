# GPT-2 Speedrun · 72.2419 minutes

**AutoTrust's ScienceGuru research platform, using Guru Turbo 1.2, trained a GPT language model past the GPT-2 quality target in 72.2419 minutes on 8×H100.** The complete 22-task CORE score is **0.259212**, above the target of **0.256525**.

![GPT-2 training-time comparison on eight H100 GPUs](assets/gpt2-comparison.svg)

[中文](README.zh-CN.md) · [Reproduce](docs/REPRODUCE.md) · [Strategy](docs/STRATEGY.md) · [Results](docs/RESULTS.md) · [Benchmark and baselines](docs/BENCHMARK.md)

## Performance comparison

The result uses **27.03% less training time** than the official leaderboard's rounded **99-minute** reference, and **2.27% less** than Giovanni Zinzi's **73.917-minute** mixed-data result. The table brings the comparisons together; the run counts accompany each reported score. Sources checked on September 24, 2026.

| Strategy | Team / contributor | Training time | CORE | Runs |
|---|---|---:|---:|---:|
| **GPT-2 Speedrun, MLP4864** | **AutoTrust · ScienceGuru · Guru Turbo 1.2** | **72.2419 min** | **0.259212** | **1** |
| [ClimbMix / Cosmopedia mixture](https://github.com/karpathy/nanochat/pull/830) | Giovanni Zinzi | 73.917 min | 0.267123 | 3 |
| [ClimbMix recipe](https://github.com/karpathy/nanochat/pull/830) | Giovanni Zinzi | 81.835 min | 0.261814 | 6 |
| [Host-RAM n-grams](https://github.com/karpathy/nanochat/pull/854) | Oriole Networks · Nihir Patel and collaborators | 91.74 min | 0.2578 | 3 |
| [**Official leaderboard — Run 6**](https://github.com/karpathy/nanochat/blob/92d63d4e8bb4df75c3b71618f31ddde2378b2bcd/dev/LEADERBOARD.md#run-6) | Andrej Karpathy | ≈99 min | 0.262634 | 5 |

Training time follows the benchmark's native `total_training_time` metric. [Timing, evaluation, and comparison details](docs/BENCHMARK.md).

## The result

| Measurement | Value |
|---|---:|
| Native training time | **4,334.512382 seconds** |
| Complete CORE, 22 tasks | **0.259212** |
| Validation bits per byte | **0.724029** |
| Training updates | **9,841** |
| Native timed updates | **9,830** |
| Training tokens | **5,159,518,208** |
| Seed | **42** |
| Hardware | **8× NVIDIA H100 80GB** |

The [result files](results/nc033/) include per-task CORE, native training-step logs, evaluation metrics, and model configuration. [Machine-readable experiment history](results/experiments.json) includes the earlier MLP5120 runs.

## The strategy

The model is a 22-layer GPT with width 1,408, 11 attention heads, a 49,152-token vocabulary, and an **MLP hidden width of 4,864**. A smaller feed-forward network reduces training work while retaining the model depth and attention width. The training horizon is set explicitly to **9,841 updates**, with complete downstream evaluation used to choose the final recipe.

Execution uses tensorwise FP8 matrix operations, FlashAttention 3, Liger's fused softcapped cross entropy, BF16 computation, and the original Muon/AdamW optimizer implementation. Sequences contain 2,048 tokens, with a global batch of 524,288 tokens across eight GPUs. Training uses ClimbMix and the original tokenizer and evaluation bundle. [Architecture and training details](docs/STRATEGY.md).

## Reproduce

Use a Linux machine with eight H100 80GB GPUs, a CUDA-compatible driver, Python 3.12, and `uv`:

```bash
export NANOCHAT_BASE_DIR="$HOME/.cache/gpt2-speedrun"
bash reproduction/install.sh --execute
bash reproduction/prepare_data.sh --execute
bash reproduce.sh 9841 --execute
```

The final command trains from scratch, saves the checkpoint, and runs complete CORE and standard BPB evaluation. Run each script without `--execute` to inspect its commands. [Setup and output paths](docs/REPRODUCE.md).

## ScienceGuru and Guru Turbo 1.2

[AutoTrust](https://autotrust.ai/) develops AI for scientific research. This experiment was carried out with its **ScienceGuru** platform and **Guru Turbo 1.2** research model. The model trained by the benchmark is the GPT language model described above. [Project attribution](provenance/project-attribution.json).

Built on [karpathy/nanochat](https://github.com/karpathy/nanochat). Upstream copyright and the MIT license are retained in [LICENSE](LICENSE) and [NOTICE](NOTICE).
