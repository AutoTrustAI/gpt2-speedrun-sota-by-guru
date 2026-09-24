# Time-to-GPT-2 chart data and sources

The README uses three figures styled after the supplied [NanoGPT blog](https://github.com/AutoTrustAI/nanogpt-speedrun-sota-by-guru/blob/66418f828a8a747cf1186a7faef4d7bd90e12dd1/README.md): a dark green result card with a gold headline number, a cream historical chart, and a cream research workflow with measured experiments. Each PNG is 2400×1350; each SVG has selectable text and an accessible description. All measurements come from this GPT-2 repository.

## Result card

The [scorecard](../assets/gpt2-scorecard.svg) reads [nc033 metrics](../results/nc033/metrics.json) and [public baselines](../results/public-baselines.json). It shows **72.24 minutes**, approximately **1.37×** the official Run 6 training speed, **1.13×** the ClimbMix main recipe's speed, **0.259212 CORE**, and approximately **27.03% less training time** than Run 6. The displayed time is rounded from 72.2418730378151 minutes. Ratios and time savings are calculated from the full recorded precision. The result is one completed run, not a repeated-run mean.

The history figure shows six nanochat leaderboard runs, two selected comparison results, and ScienceGuru's completed experiment. Every plotted time uses an 8×H100 node.

## History values

| Chart date | Result | Training minutes | Source |
|---|---|---:|---|
| 2026-01-29 | Run 1: d24 baseline | ≈182.4 | [nanochat leaderboard](https://github.com/karpathy/nanochat/blob/92d63d4e8bb4df75c3b71618f31ddde2378b2bcd/README.md#time-to-gpt-2-leaderboard), 3.04 hours |
| 2026-02-02 | Run 2: FP8 | ≈174.6 | Same leaderboard, 2.91 hours |
| 2026-02-05 | Run 3: larger batch | ≈165.6 | Same leaderboard, 2.76 hours |
| 2026-03-04 | Run 4: ClimbMix | ≈121.2 | Same leaderboard, 2.02 hours |
| 2026-03-09 | Run 5: autoresearch round 1 | ≈108 | Same leaderboard, 1.80 hours |
| 2026-03-14 | Run 6: autoresearch round 2 | ≈99 | Same leaderboard, 1.65 hours |
| 2026-08-15 | Giovanni Zinzi: ClimbMix | 81.835 | [#830](https://github.com/karpathy/nanochat/pull/830), six-run result |
| 2026-09-11 | Oriole Networks: host-RAM n-grams | 91.74 | [#854](https://github.com/karpathy/nanochat/pull/854), three-run result |
| 2026-09-24 | ScienceGuru + Guru Turbo 1.2 | 72.241873 | [nc033 metrics](../results/nc033/metrics.json), seed 42 |

The six official dates and times follow the pinned nanochat README. Its hours are rounded, so their conversion to minutes and comparisons against them are approximate. Run 4 uses March 4 from that table; the detailed run note instead says March 3. The first three run notes contain more precise seconds, but the history consistently uses the table's published hours.

The Giovanni point uses #830's opening date; the Oriole point uses #854's opening date. Their values were read from the submission bodies on September 24, 2026. These dates identify the submissions and do not assert the precise date of each underlying experiment. ScienceGuru uses the date of this repository's [first publication commit](https://github.com/AutoTrustAI/gpt2-speedrun-sota-by-guru/commit/9f154239f71c7075db60af0203a2c1131a8e120e), September 24, 2026 UTC.

The minutes axis is linear. The solid stepped line connects the six official runs, with a pale horizontal guide extending the standing Run 6 reference. Outlined circles show selected comparisons, and the green star shows ScienceGuru. The dashed vertical segment compares ScienceGuru with the 99-minute reference at the final date; the guides do not represent additional measurements. The 2019 GPT-2 training used different hardware and is outside this plot.

## Research workflow and experiments

The [research workflow](../assets/gpt2-research-loop.svg) presents five stages: survey, size the MLP, schedule training, execute, and verify. Below it are the three completed experiments, read directly from their individual metrics files: **nc027, 73.377287 minutes**; **nc029, 73.497218 minutes**; and **nc033, 72.241873 minutes**. Each row includes its MLP width, update count and complete CORE score. Bars start at zero and retain experiment order, including the increase from nc027 to nc029.

At the same 9,841-update horizon, nc033 took **75.32 seconds less** than nc029, while CORE decreased from **0.263907** to **0.259212** and remained above the **0.256525** target. Each row is one seed 42 run. The workflow does not present these measurements as repeated-run averages or as independent causal effects of each illustrated stage. See [experimental results](RESULTS.md) and [strategy](STRATEGY.md).

## Comparison arithmetic

The supplementary comparison figure reads the [measured nc033 result](../results/nc033/metrics.json) and checks its values against the [public source snapshot](../results/public-baselines.json). The bar axis starts at zero. CORE accompanies every bar, and contributor labels give each result's run count.

```text
ScienceGuru time = 4,334.512382268906 / 60 = 72.2418730378151 minutes
Speedup = reference time / ScienceGuru time
Time reduction = 1 - ScienceGuru time / reference time
```

The rounded official 99-minute reference gives approximately **1.370× speedup**, **27.03% less time**, and **26.76 minutes saved**.

## Regenerate the figures

With Python and Matplotlib installed, from the repository root:

```bash
python3 assets/render_scorecard.py
python3 assets/render_history.py
python3 assets/render_research_loop.py
python3 assets/render_comparison.py
```

All scripts export SVG with selectable text and accessible descriptions, plus PNG for sharing. They verify plotted values against the result and reference data before rendering.

- [Scorecard SVG](../assets/gpt2-scorecard.svg) · [Scorecard PNG](../assets/gpt2-scorecard.png)
- [History data](../assets/speedrun-history-data.json) · [History SVG](../assets/speedrun-history.svg) · [History PNG](../assets/speedrun-history.png)
- [Research workflow SVG](../assets/gpt2-research-loop.svg) · [Research workflow PNG](../assets/gpt2-research-loop.png)
- [Comparison data](../assets/comparison-data.json) · [Comparison SVG](../assets/gpt2-comparison.svg) · [Comparison PNG](../assets/gpt2-comparison.png)
- [Page reference snapshot](../provenance/page-reference.json) · [Benchmark and CORE protocol](BENCHMARK.md)
