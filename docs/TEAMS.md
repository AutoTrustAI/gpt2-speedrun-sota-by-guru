# Teams and contributors

The comparison brings together the maintained Time-to-GPT-2 leaderboard and selected public submissions at the **8×H100 / CORE >0.256525** target. Names and affiliations below follow the linked primary sources. The source snapshot and reported measurements are preserved in [public-baselines.json](../results/public-baselines.json).

## AutoTrust · ScienceGuru · Guru Turbo 1.2

[AutoTrust](https://autotrust.ai/about) is the organization behind this project; [ScienceGuru](https://scienceguru.ai/) is its research platform; **Guru Turbo 1.2** is the model used for the research and coding work. [Project attribution](../provenance/project-attribution.json). The benchmark trains the GPT language model in this repository. Its published result is **72.241873 minutes, CORE 0.259212**, from the completed seed 42 experiment [nc033](../results/nc033/).

## Contributors in the performance comparison

| Contributor | Publicly documented contribution | Reported result |
|---|---|---|
| **Andrej Karpathy** | Maintains [nanochat](https://github.com/karpathy/nanochat). The official [Run 6 account](https://github.com/karpathy/nanochat/blob/92d63d4e8bb4df75c3b71618f31ddde2378b2bcd/dev/LEADERBOARD.md#run-6) describes architecture improvements from the second autoresearch round. | **≈99 min**, CORE **0.262634**, five runs. |
| **Giovanni Zinzi** | Author of [PR #830](https://github.com/karpathy/nanochat/pull/830): a d22 recipe with a 49,152-token vocabulary, fused cross entropy and selective RMSNorm scales. The submission identifies the contributor without establishing a company affiliation. | Main ClimbMix recipe: **81.835 min**, CORE **0.261814**, six runs. |
| **Oriole Networks · Nihir Patel** | The disclosure in [PR #854](https://github.com/karpathy/nanochat/pull/854) identifies Nihir Patel, Alessandro Ottino and Robin Matzner with Oriole Networks. The method adds hashed bigram/trigram tables in host RAM to a d24 model. | **91.74 min**, CORE **0.2578**, three runs. |

Oriole's individual CORE scores are 0.2592, 0.2557 and 0.2584; two of the three exceed the individual threshold. These details accompany the aggregate results in [Benchmark and comparisons](BENCHMARK.md).

## Related organizations and research

**NVIDIA** supplies the ClimbMix data introduced in official [Run 4](https://github.com/karpathy/nanochat/blob/92d63d4e8bb4df75c3b71618f31ddde2378b2bcd/dev/LEADERBOARD.md#run-4). **OpenAI** trained the original GPT-2 model used to set the historical CORE target, as described in the [benchmark overview](https://github.com/karpathy/nanochat/blob/92d63d4e8bb4df75c3b71618f31ddde2378b2bcd/dev/LEADERBOARD.md). These are data and reference-model roles, respectively.

**Recursive** publishes [NanoChat autoresearch artifacts](https://github.com/recursive-org/first-steps-toward-automated-ai-research/tree/main/nanochat_autoresearch) for a different protocol: one B200 GPU and a fixed five-minute budget, evaluated by validation BPB. Those results provide related research context and are outside the Time-to-GPT-2 training-time chart.

Implementation acknowledgments and licensing are retained in [NOTICE](../NOTICE), [LICENSE](../LICENSE), and the original source files.
