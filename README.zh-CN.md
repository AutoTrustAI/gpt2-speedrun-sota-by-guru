# ScienceGuru：72.2419 分钟达到 GPT-2 能力，较官方 SOTA 加速约 1.37 倍

**AutoTrust 的 ScienceGuru 科研平台，使用 Guru Turbo 1.2，在 8×H100 上用 72.2419 分钟训练出超过 GPT-2 质量门槛的 GPT 语言模型。** 完整 22 项 CORE 得分为 **0.259212**，超过 **0.256525** 的门槛。相对官方 SOTA 的约 **99 分钟**，训练时间减少约 **27.03%**，节省约 **26.76 分钟**。[成绩与对比来源](docs/BENCHMARK.md)。

| 训练时间 | 相对官方 SOTA 的加速比 | 训练时间减少 | 完整 CORE |
|---:|---:|---:|---:|
| **72.2419 分钟** | **约 1.37×** | **约 27.03%** | **0.259212** |

nanochat 官方榜单收录了 **6 次 8×H100 运行纪录**，依次通过 FP8、更大批量、ClimbMix 数据和两轮 autoresearch 提高训练效率。下图将 ScienceGuru 的成绩与这段优化历程及主要公开方案放在一起。

![Time-to-GPT-2 训练时间历史：从 nanochat 的六次榜单纪录到 ScienceGuru + Guru Turbo 1.2 的 72.2419 分钟。](assets/speedrun-history.svg)

[图表数据与来源](docs/SPEEDRUN_CHART.md) · [下载历史图 PNG](assets/speedrun-history.png)

[English](README.md) · [复现说明](docs/REPRODUCE.md) · [技术方案](docs/STRATEGY.md) · [实验材料](docs/EVIDENCE.md) · [完整成绩](docs/RESULTS.md) · [团队与贡献者](docs/TEAMS.md) · [评测规则](docs/BENCHMARK.md)

## AutoTrust、ScienceGuru 与 Guru Turbo 1.2

### AutoTrust

[**AutoTrust**](https://autotrust.ai/about) 是位于新加坡的应用 AI 研究实验室，致力于开发服务科学研究的 AI 系统，研究方向包括科学智能体、持续科研任务、自我改进的编程智能体和 AI 科学家。实验室将真实科研工作流与模型训练、推理和智能体协作相结合，提升研究系统的能力。

### ScienceGuru

[**ScienceGuru**](https://scienceguru.ai/) 是 AutoTrust 的科研工作空间，支持网页版和桌面端，将科研模型用于探索、阅读、推理和写作。在本项目中，ScienceGuru 将这一工作方式用于 GPT 预训练：分析瓶颈、实现候选方案、运行实验，再评估训练所得模型。

### Guru Turbo 1.2

**Guru Turbo 1.2** 是本次 ScienceGuru 项目中负责研究和编程的模型。AutoTrust 的 [**Guru 系列**](https://autotrust.ai/models) 包含 Nano、Pro 和 Turbo，面向科学智能体工作负载与持续科研任务。本项目由 Guru Turbo 1.2 开发训练方案；benchmark 测量的是 [`nanochat/`](nanochat/) 中 GPT 语言模型的训练成绩。[项目归属说明](provenance/project-attribution.json)。

方案采用 22 层 GPT、较紧凑的前馈网络、明确的训练步数，以及 FP8、FlashAttention 3 和融合交叉熵，减少每步计算量及达到能力门槛所需的训练时间。[技术方案](docs/STRATEGY.md)。

## 实测成绩

**AutoTrust · ScienceGuru · Guru Turbo 1.2** 在 **8×H100 80GB** 上，从头训练 seed 42，完成 **9841 次更新**，用时 **72.2419 分钟**，完整 **22 项 CORE 为 0.259212**。独立评估得到的验证集 BPB 为 **0.724029**。

原生 `total_training_time` 为 **4334.512382 秒**，包含 **9830 次计时更新**。训练循环将最初 11 次更新记录、评估、日志与 checkpoint 写入排除在这一计时之外。[计时规则](docs/BENCHMARK.md#core-and-timing)。

[完整结果与配置](results/nc033/) · [机器可读实验历史](results/experiments.json) · [实验材料说明](docs/EVIDENCE.md)

## 成绩对比

以下结果核对于 **2026-09-24 UTC**，使用 **8×H100 / CORE >0.256525**，按训练时间排序。各方案采用来源报告的时间与运行次数；ScienceGuru 使用已完成的 seed 42 成绩。官方约 99 分钟为经过舍入的数值。

![GPT-2 训练时间对比：ScienceGuru 72.2419 分钟、ClimbMix 方案 81.835 分钟、Oriole Networks 91.74 分钟、官方 Run 6 约 99 分钟。](assets/gpt2-comparison.svg)

[下载对比图 PNG](assets/gpt2-comparison.png) · [对比数据](assets/comparison-data.json) · [来源与规则](docs/BENCHMARK.md)

| 方案 | 团队 / 作者 | 训练时间 | CORE | 运行次数 | ScienceGuru 加速比 |
|---|---|---:|---:|---:|---:|
| **ScienceGuru，MLP4864** | **AutoTrust · Guru Turbo 1.2** | **72.2419 分钟** | **0.259212** | **1** | — |
| [ClimbMix 方案](https://github.com/karpathy/nanochat/pull/830) | Giovanni Zinzi | **81.835 分钟** | 0.261814 | 6 | **1.133×** |
| [主机内存 n-gram](https://github.com/karpathy/nanochat/pull/854) | Oriole Networks · Nihir Patel 等 | **91.74 分钟** | 0.2578 | 3 | **1.270×** |
| [**官方 SOTA — Run 6**](https://github.com/karpathy/nanochat/blob/92d63d4e8bb4df75c3b71618f31ddde2378b2bcd/dev/LEADERBOARD.md#run-6) | Andrej Karpathy | **约 99 分钟** | 0.262634 | 5 | **约 1.370×** |

相对官方 Run 6，ScienceGuru 节省约 **26.76 分钟**，加速约 **1.370 倍**。本方案使用 ClimbMix、原 tokenizer 和完整下游评估。[对比说明](docs/BENCHMARK.md#public-comparisons)。

## 主要贡献者背景

| 贡献者 | 公开背景 | 本页对比成绩 |
|---|---|---|
| **Andrej Karpathy** | [nanochat](https://github.com/karpathy/nanochat) 的创建者与维护者；最新官方成绩采用第二轮 autoresearch 的改进。 | **约 99 分钟** |
| **Giovanni Zinzi** | [#830](https://github.com/karpathy/nanochat/pull/830) 的作者，方案涉及融合交叉熵、选择性 RMSNorm 缩放和 49152 词表。 | **81.835 分钟** |
| **Oriole Networks · Nihir Patel 等** | [#854](https://github.com/karpathy/nanochat/pull/854) 明确列出 Nihir Patel、Alessandro Ottino 和 Robin Matzner 的 Oriole Networks 归属。 | **91.74 分钟** |

[Recursive](https://github.com/recursive-org/first-steps-toward-automated-ai-research/tree/main/nanochat_autoresearch) 也公开了 NanoChat autoresearch 实验：单张 B200、五分钟预算、10 个 seed 的平均验证 BPB 为 **0.9109**，采用另一套硬件和评测规则。[团队、贡献与相关研究](docs/TEAMS.md)。

## 这个 benchmark 考察什么

Time-to-GPT-2 衡量**达到固定下游能力门槛所需的训练时间**。模型容量、数据质量、收敛速度和 GPU 执行效率共同决定成绩，涉及架构设计、数值精度、GPU kernel、分布式通信、显存使用和可复现实验。

它的价值在于把系统速度与模型能力联系起来：优化需要让足够强的 GPT 模型更早训练完成。官方纪录中包含 autoresearch 自动发现的改进，也让它成为研究 AI 辅助训练优化的具体实验场景。[评测意义与 CORE 规则](docs/BENCHMARK.md)。

## 仓库内容

- [`nanochat/`](nanochat/) 和 [`scripts/`](scripts/)：冻结的模型、训练、tokenizer 与评估实现。
- [`reproduction/source-manifest.json`](reproduction/source-manifest.json)：22 个保留源文件、许可证和依赖文件的哈希。
- [`results/`](results/)：三次完整实验、逐项 CORE、原生训练日志和评估指标。
- [`docs/REPRODUCE.md`](docs/REPRODUCE.md)：9841 步方案的环境、数据与启动说明。
- [`docs/EVIDENCE.md`](docs/EVIDENCE.md)：源码版本、实验文件与核验命令。

参考硬件为 **8× NVIDIA H100 80GB**。训练使用 **170 个 ClimbMix 数据分片**、独立验证分片、**49152 词表**、**2048 token 序列**和 **524288 token 全局批量**。[复现说明](docs/REPRODUCE.md)包含依赖安装、输入准备、从头训练和完整 CORE/BPB 评估步骤。

## 致谢与许可证

基于 [karpathy/nanochat](https://github.com/karpathy/nanochat)，在 [LICENSE](LICENSE) 和 [NOTICE](NOTICE) 中保留上游版权及 MIT 许可证。[源码与依赖归属](NOTICE) · [ScienceGuru 项目归属](provenance/project-attribution.json)。
