**AUTOTRUST AI  ·  SCIENCEGURU  ·  RESEARCH**

# ScienceGuru 将 GPT-2 Speedrun 压缩至 72.24 分钟

AutoTrust 的科研平台运行 Guru Turbo 1.2，在八张 H100 上用 72.24 分钟将 GPT 语言模型训练到超过 GPT-2 质量门槛：相较官方 99 分钟的纪录，加速约 1.37 倍。

2026 年 9 月 25 日  ·  ScienceGuru  ·  Guru Turbo 1.2  ·  Time-to-GPT-2

[English](README.md)

今天，我们发布 ScienceGuru 在 Time-to-GPT-2 上的成绩。这个开放基准考察的是：训练出具备 GPT-2 下游能力的语言模型，最快需要多久。ScienceGuru 运行 Guru Turbo 1.2，开发出一套训练方案，在八张 H100 GPU 上用 **72.2419 分钟**达到完整 22 项任务 **0.259212 的 CORE 得分**，超过 **0.256525** 的目标。

相较官方 Run 6 的 99 分钟参考成绩，这一结果**加速约 1.37 倍**，训练时间减少 **27.03%**，即 **26.76 分钟**。其训练速度也是 Giovanni Zinzi 报告的 81.835 分钟 ClimbMix 主方案的 **1.13 倍**、Oriole Networks 的 91.74 分钟方案的 **1.27 倍**。对比来源核对于 2026 年 9 月 24 日；由于官方时间经过舍入，以它为基准的计算均为近似值。代码、日志、源码哈希与核验说明已公开在 [github.com/AutoTrustAI/gpt2-speedrun-sota-by-guru](https://github.com/AutoTrustAI/gpt2-speedrun-sota-by-guru)。

<a id="performance-comparison"></a>

![ScienceGuru 与 Guru Turbo 1.2：72.24 分钟，约为官方 Run 6 训练速度的 1.37 倍，CORE 0.259212，训练时间减少约 27.03%。](assets/gpt2-scorecard.svg)

*8×H100 上的一次完整运行，完成全部 22 项 CORE 任务评估。官方 Run 6 时间经过舍入，因此相关对比为近似值。[下载成绩卡 PNG](assets/gpt2-scorecard.png) · [详细对比图](assets/gpt2-comparison.svg) · [数据与来源](docs/BENCHMARK.md#public-comparisons)。*

## 为什么选择 GPT-2 speedrun

这个 speedrun 固定了硬件与目标：在一台 8×H100 节点上训练，直到模型超过 GPT-2 的参考 CORE 得分 0.256525。CORE 汇总 22 项任务的表现，并根据各任务的随机基线进行调整。达到目标既需要高效的训练系统，也需要模型从数据中学到足够的能力。架构、数值精度、GPU kernel、内存使用和收敛速度都会影响成绩。

这一基准由 [Andrej Karpathy 在 nanochat 中维护](https://github.com/karpathy/nanochat)。六次官方运行记录展示了通过 FP8 训练、更大批量、ClimbMix 数据以及两轮 autoresearch 实现的改进。本次对比采用的最新官方参考是 Run 6，用时约 99 分钟，CORE 为 0.262634。

社区贡献者进一步推进了这一系统。[Giovanni Zinzi 的主方案](https://github.com/karpathy/nanochat/pull/830) 报告了融合交叉熵、选择性 RMSNorm 缩放以及 49,152 token 的 speedrun 词表。[Oriole Networks 的 Nihir Patel、Alessandro Ottino 和 Robin Matzner](https://github.com/karpathy/nanochat/pull/854) 则探索了驻留主机内存的 n-gram 表。他们的成绩为达到同一质量门槛提供了更多对比参照。[贡献者背景与来源](docs/TEAMS.md)。

![Time-to-GPT-2 训练时间历史](assets/speedrun-history.svg)

*nanochat 的六次官方运行记录、领先的公开对比方案以及 ScienceGuru 的成绩。官方参考时间以舍入后的分钟数报告。[历史数据与来源](docs/SPEEDRUN_CHART.md) · [下载 PNG](assets/speedrun-history.png)。*

## ScienceGuru 改了什么

这一结果来自让模型容量与训练步数适配质量目标，同时保留已有的快速执行路径。ScienceGuru 公开的方案采用 22 层 GPT，缩小前馈网络，并训练 9,841 次更新。仓库保留了此前完成的实验及最快达到门槛的结果，因此可以直接检查速度与质量之间的取舍。

### 1. 缩小前馈网络宽度

最终模型保留了 22 层 Transformer、1,408 的模型宽度、11 个注意力头、49,152 token 的词表以及 2,048 token 的上下文。变化发生在 MLP：隐藏层宽度从 5,120 降至 4,864。这减少了 **15,859,712 个参数**，以及约 **2.56% 的单 token 估算浮点运算量**。调整后的模型共有 1,375,503,474 个参数。

在相同的 9,841 次更新下，记录中的 MLP5120 运行用时 **73.4972 分钟**，MLP4864 用时 **72.2419 分钟**，节省 **75.32 秒**。CORE 从 0.263907 变为 0.259212，仍高于目标；验证集每字节比特数（BPB）从 0.723137 变为 0.724029。这一改进用一部分实测质量余量换取更短的训练时间。[完整实验结果](docs/RESULTS.md)。

### 2. 明确训练步数

方案训练 **9,841 次更新**，处理 **5,159,518,208 个 token**。每次更新的全局批量为 524,288 token，每张 GPU 使用 32 条序列。训练采用 170 个 ClimbMix 分片和原有的独立验证分片。

显式指定的迭代次数决定训练长度，`target_param_data_ratio=9.20` 仍作为原有超参数缩放规则的输入。训练调度使用 40 步预热、0.65 的学习率下降阶段比例，以及 0.05 的最终学习率比例。权重衰减和优化器公式保持不变。[精确方案与启动参数](reproduction/recipes.json)。

### 3. 保留快速执行路径

模型采用逐张量 FP8 矩阵计算，周边计算使用 BF16，并沿用 FlashAttention 3、原有的 Liger 融合 softcap 交叉熵以及 Muon/AdamW 优化器实现。注意力窗口模式仍为 SSSL。这些构成了公开方案保留的执行基础；归档对比则在相同更新次数下考察更小 MLP 带来的变化。

训练与模型源码复制自记录中的实验版本。发布材料包含精确配置、依赖版本和源码哈希，以便重建实测方案。[技术方案](docs/STRATEGY.md) · [复现说明](docs/REPRODUCE.md)。

![ScienceGuru 研究流程与三次完整 GPT-2 实验，展示准确训练时间及 CORE 得分。](assets/gpt2-research-loop.svg)

*已记录的实验展示了速度与质量的取舍。在相同的 9,841 次更新下，MLP4864 比 MLP5120 少用 75.32 秒训练时间，两者均达到 CORE 目标。每行对应一次完整运行。[下载流程图 PNG](assets/gpt2-research-loop.png) · [实验结果](docs/RESULTS.md)。*

## 我们如何核验

速度结果很容易出错，因此发布材料按可核验的方式组织：

- **完整下游评估。** 使用相同的 MLP4864 配置恢复 checkpoint，并通过 `--max-per-task=-1` 对全部 22 项 CORE 任务中的所有样本进行评估，得到 CORE 0.259212。标准 BPB 评估在每个数据划分上使用 20,971,520 个 token，得到验证集 BPB 0.724029。所有单项任务得分均予保留，包括表现下降的项目。

- **原生计时边界。** 原始 `total_training_time` 为 **4,334.512382 秒**，覆盖 9,841 次更新中的 **9,830 次计时更新**。最初 11 次更新记录、评估、日志和 checkpoint 写入不在这一计时内。完整复现还需额外的环境准备、tokenizer 准备和最终评估时间。

- **已记录的实验。** 公开成绩来自一次完整的 seed 42 运行 nc033。材料还保留了此前完成的两次 MLP5120 实验 nc027 和 nc029，包括它们的配置、完整 CORE 结果与原生指标记录。实测表中不包含推算成绩。

- **固定的源码与文件。** 源码清单标识了实验版本 `a72e2f4b16595a3409edc39b00e07e22bee45c09` 中 22 个未经修改的源码、许可证和依赖文件。另有清单记录公开结果及复现包的哈希。运行 `python3 reproduction/verify.py source` 即可在 CPU 上核验冻结源码；[证据说明](docs/EVIDENCE.md#verify-the-published-package)还提供了实验文件的检查方法。

## 范围与限制

- 这是从方案开发过程中选出的一次达标运行，不能据此确定重复运行之间的波动。对比方案报告了各自的运行次数与汇总方式，最终 CORE 得分也有所不同。

- 报告的时间衡量原生训练区间，不包含完整研究过程，也不包含从头准备输入、训练和评估所需的全部时间。

- 输入清单记录了训练分片的名称与大小，并提供了独立验证数据、tokenizer 文件和评估文件的哈希。完整训练分片的内容哈希未被记录，依赖锁文件也未固定外部 FlashAttention 3 二进制文件的版本。

- 测量值来自原始归档运行。可移植启动脚本已通过静态检查和 describe 模式检查，其端到端 GPU 执行仍有待验证。数据集内容、tokenizer 文件、训练权重和编译后的 kernel 缓存需要在复现过程中获取或生成。

## 接下来

这次发布使后续核验有了明确的起点：从头复现冻结的方案，运行完整下游评估，并测量全新运行之间的结果波动。源码清单、启动命令和单项任务得分，为其他研究者检查训练效率以及超出目标的质量余量提供了材料。

AutoTrust 是位于新加坡的应用 AI 研究实验室，研究方向包括科学智能体、持续科研任务和自我改进的编程智能体。旗下 ScienceGuru 工作空间将科研模型用于文献阅读、科学推理、写作与实验。Guru Turbo 1.2 是本项目研究和编程使用的模型；报告的 72.24 分钟衡量的是 GPT 模型训练方案的用时。[AutoTrust](https://autotrust.ai/about) · [Guru 模型](https://autotrust.ai/models) · [项目归属说明](provenance/project-attribution.json)。

### SCIENCEGURU

将创造这一结果的系统用于你自己的研究。前往 [ScienceGuru.ai](https://scienceguru.ai) 下载 ScienceGuru。

[下载 ScienceGuru →](https://scienceguru.ai)

代码、日志与核验：[github.com/AutoTrustAI/gpt2-speedrun-sota-by-guru](https://github.com/AutoTrustAI/gpt2-speedrun-sota-by-guru)

社区纪录：[karpathy/nanochat — Time-to-GPT-2](https://github.com/karpathy/nanochat/blob/92d63d4e8bb4df75c3b71618f31ddde2378b2bcd/dev/LEADERBOARD.md)。官方时间取自记录中的榜单参考版本。

基于 [karpathy/nanochat](https://github.com/karpathy/nanochat)。上游版权及 MIT 许可证保留在 [LICENSE](LICENSE) 和 [NOTICE](NOTICE) 中。
