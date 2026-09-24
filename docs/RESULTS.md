# Experimental results

All three rows are complete seed 42 runs with full 22-task CORE evaluation. The published model uses the fastest qualifying row, nc033.

| Run | MLP width | Updates | Training minutes | CORE | Validation BPB |
|---|---:|---:|---:|---:|---:|
| [nc027](../results/nc027/) | 5120 | 9873 | 73.377287 | 0.258965 | 0.723000 |
| [nc029](../results/nc029/) | 5120 | 9841 | 73.497218 | 0.263907 | 0.723137 |
| [nc033](../results/nc033/) | 4864 | 9841 | 72.241873 | 0.259212 | 0.724029 |

nc033 saves 68.124845 seconds relative to nc027 and 75.320702 seconds relative to nc029. Its CORE is 0.000247 higher than nc027 and 0.004695 lower than nc029. The complete per-task scores are retained, including tasks that decline.

Published training logs contain the original native step and summary lines. Evaluation logs contain the original task and BPB metric lines; machine-specific startup diagnostics are excluded. The original full-result SHA and frozen source revision are retained in each metrics JSON. Published artifact hashes are in [artifact-manifest.json](../results/artifact-manifest.json).

A 9,777-update run was in progress at publication preparation time. No projected result is included in the measured table.
