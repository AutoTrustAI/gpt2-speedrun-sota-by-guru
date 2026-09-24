# Time-to-GPT-2 chart data and sources

The history figure shows six nanochat leaderboard runs, two selected comparison results, and ScienceGuru's completed 72.2419-minute experiment. Every plotted time uses an 8×H100 node. The chart and main comparison use the cream and green presentation of the latest [NanoGPT reference page](https://github.com/AutoTrustAI/nanogpt-speedrun-sota-by-guru/blob/fcdc062afd12b50684361d04451b5681670bb843/README.md), with Time-to-GPT-2 data throughout.

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

The solid line connects the six official runs. Diamonds show selected comparisons, and the star shows ScienceGuru. The dashed segment connects the official Run 6 reference to ScienceGuru for comparison. It does not represent additional measurements. The 2019 GPT-2 training used different hardware and is outside this plot.

## Comparison arithmetic

The comparison figure reads the [measured nc033 result](../results/nc033/metrics.json) and checks its values against the [public source snapshot](../results/public-baselines.json). The bar axis starts at zero. CORE accompanies every bar, and the main table gives each result's run count.

```text
ScienceGuru time = 4,334.512382268906 / 60 = 72.2418730378151 minutes
Speedup = reference time / ScienceGuru time
Time reduction = 1 - ScienceGuru time / reference time
```

The rounded official 99-minute reference gives approximately **1.370× speedup**, **27.03% less time**, and **26.76 minutes saved**.

## Regenerate the figures

With Python and Matplotlib installed, from the repository root:

```bash
python3 assets/render_history.py
python3 assets/render_comparison.py
```

Both scripts export SVG with selectable text and accessible descriptions, plus PNG for sharing. They verify plotted values against the result and reference data before rendering.

- [History data](../assets/speedrun-history-data.json) · [History SVG](../assets/speedrun-history.svg) · [History PNG](../assets/speedrun-history.png)
- [Comparison data](../assets/comparison-data.json) · [Comparison SVG](../assets/gpt2-comparison.svg) · [Comparison PNG](../assets/gpt2-comparison.png)
- [Page reference snapshot](../provenance/page-reference.json) · [Benchmark and CORE protocol](BENCHMARK.md)
