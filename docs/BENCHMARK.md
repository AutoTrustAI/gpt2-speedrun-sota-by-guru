# Time-to-GPT-2: benchmark and comparisons

## What it measures

Time-to-GPT-2 asks how quickly a GPT language model trained on one 8-H100 node can exceed the GPT-2 reference score of **0.256525 CORE**. It measures training-system efficiency together with learned downstream capability. Faster kernels help, but capacity, data and optimization must still produce a model that crosses the quality target. [Official overview](https://github.com/karpathy/nanochat/blob/92d63d4e8bb4df75c3b71618f31ddde2378b2bcd/README.md#time-to-gpt-2-leaderboard).

This makes it a useful compact test of practical LLM training: architecture design, GPU execution, distributed throughput, memory use, convergence and data quality all affect time to the target. It is a pretraining benchmark; supervised fine-tuning and chat-interface behavior are separate stages.

## CORE and timing

CORE is the equal-weight mean of 22 task scores after adjusting for each task's random baseline:

```text
CORE = mean((accuracy_i - random_baseline_i) / (1 - random_baseline_i))
```

Here `random_baseline_i` is a probability: divide the evaluator's recorded percentage by 100. Chance performance maps to zero, perfect performance to one. The evaluator uses the prescribed answer/continuation scoring for each task. The final evaluation here uses every example through `--max-per-task=-1`. [Evaluator](https://github.com/karpathy/nanochat/blob/92d63d4e8bb4df75c3b71618f31ddde2378b2bcd/scripts/base_eval.py#L51-L111).

The reported time is the original `total_training_time` accumulated by the training loop. Evaluation and logging are excluded; the first eleven update records and checkpoint writing are outside that timer. The full process also includes setup, data/tokenizer preparation and final evaluation. Upstream submissions ask for straightforward implementations and principled behavior across model depths. [Protocol](https://github.com/karpathy/nanochat/blob/92d63d4e8bb4df75c3b71618f31ddde2378b2bcd/dev/LEADERBOARD.md).

## Public comparisons

All comparison rows appear together in the [main page](../README.md#performance-comparison). Data and direct sources are in [public-baselines.json](../results/public-baselines.json), checked September 24, 2026.

- The maintained official table lists Run 6 at approximately 99 minutes, CORE 0.262634, five runs.
- [Giovanni Zinzi's #830](https://github.com/karpathy/nanochat/pull/830) reports 81.835 minutes and CORE 0.261814 over six runs for its main ClimbMix recipe. Its three-run 80/20 ClimbMix/Cosmopedia experiment reports 73.917 minutes and CORE 0.267123. The mixture was omitted from the main recipe after worse d14 results.
- [Oriole Networks' #854](https://github.com/karpathy/nanochat/pull/854) reports 91.74 minutes and CORE 0.2578 over three runs. The authors explicitly identify their Oriole affiliation. Two of the three listed runs exceed the individual CORE floor.

The chart uses each source's reported training time. It displays rounded 99 minutes for the official reference; calculations against that row are approximate. The ScienceGuru row is one seed 42 run, while the cited comparison rows report their stated aggregates. CORE values are shown alongside time because they differ between recipes.

## Organizations and related work

Andrej Karpathy maintains nanochat and its official reference. Oriole Networks is explicitly represented in #854. The checked #830 sources identify Giovanni Zinzi but do not establish a company affiliation. NVIDIA provides the ClimbMix data used in these experiments; the historical GPT-2 reference comes from OpenAI.

[Recursive's NanoChat research](https://github.com/recursive-org/first-steps-toward-automated-ai-research/tree/main/nanochat_autoresearch) reports 0.9109 mean validation BPB over ten seeds on **one B200 for five minutes**. It studies a different fixed-budget protocol, so its BPB cannot be placed on this 8-H100 time-to-target chart.
