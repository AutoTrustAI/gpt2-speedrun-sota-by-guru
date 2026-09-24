# GPT-2 Speedrun · 72.2419 分钟

**AutoTrust 的 ScienceGuru 科研平台，使用 Guru Turbo 1.2，在 8×H100 上用 72.2419 分钟训练出超过 GPT-2 质量门槛的 GPT 语言模型。** 完整 22 项 CORE 得分为 **0.259212**，门槛为 **0.256525**。

![GPT-2训练时间对比](assets/gpt2-comparison.svg)

[English](README.md) · [复现说明](docs/REPRODUCE.md) · [技术方案](docs/STRATEGY.md) · [完整成绩](docs/RESULTS.md)

## 成绩对比

| 方案 | 团队 / 作者 | 训练时间 | CORE | 运行次数 |
|---|---|---:|---:|---:|
| **GPT-2 Speedrun，MLP4864** | **AutoTrust · ScienceGuru · Guru Turbo 1.2** | **72.2419 分钟** | **0.259212** | **1** |
| [ClimbMix / Cosmopedia 混合数据](https://github.com/karpathy/nanochat/pull/830) | Giovanni Zinzi | 73.917 分钟 | 0.267123 | 3 |
| [ClimbMix 方案](https://github.com/karpathy/nanochat/pull/830) | Giovanni Zinzi | 81.835 分钟 | 0.261814 | 6 |
| [主机内存 n-gram](https://github.com/karpathy/nanochat/pull/854) | Oriole Networks | 91.74 分钟 | 0.2578 | 3 |
| [**官方榜单 Run 6**](https://github.com/karpathy/nanochat/blob/92d63d4e8bb4df75c3b71618f31ddde2378b2bcd/dev/LEADERBOARD.md#run-6) | Andrej Karpathy | 约99 分钟 | 0.262634 | 5 |

相对官方榜单约 99 分钟的成绩，训练时间减少 **27.03%**；相对 73.917 分钟的混合数据成绩，减少 **2.27%**，节省 **100.51 秒**。各项均按来源的运行次数报告，使用 benchmark 原生训练计时。

## 方案

训练的是完整 GPT 语言模型：22 层、宽度 1408、11 个注意力头、49152 词表。MLP4864 指每层前馈网络的隐藏宽度。缩小前馈网络后保留模型深度与注意力宽度，配合 9841 步的明确训练长度控制计算量。

使用 tensorwise FP8、FlashAttention 3、Liger 融合交叉熵、BF16 和原 Muon/AdamW 优化器。序列长度 2048，全局批量 524288 token，训练数据为 ClimbMix；最终进行完整 22 项 CORE 和标准 BPB 评估。

## 复现

```bash
export NANOCHAT_BASE_DIR="$HOME/.cache/gpt2-speedrun"
bash reproduction/install.sh --execute
bash reproduction/prepare_data.sh --execute
bash reproduce.sh 9841 --execute
```

[逐项 CORE 与训练日志](results/nc033/) · [机器可读历史成绩](results/experiments.json)

基于 [karpathy/nanochat](https://github.com/karpathy/nanochat)，保留原 MIT 许可证与版权说明。ScienceGuru 和 Guru Turbo 1.2 的项目归属见[说明](provenance/project-attribution.json)。
