# Results and evidence

**AutoTrust · ScienceGuru · Guru Turbo 1.2** produced the published **72.241873-minute** Time-to-GPT-2 result. The complete 22-task CORE is **0.259212**, above **0.256525**, and validation BPB is **0.724029**. This is one completed **seed 42** run on **8×H100 80GB**, selected from the recorded recipe development. [Exact result](../results/nc033/metrics.json) · [Project attribution](../provenance/project-attribution.json).

## Measured result

| Measurement | Published nc033 result |
|---|---:|
| Native training time | 4,334.512382 seconds |
| Training updates / timed updates | 9,841 / 9,830 |
| Training tokens | 5,159,518,208 |
| Complete CORE | 0.259212 |
| Validation BPB | 0.724029 |
| Seed | 42 |

CORE uses all examples in all 22 tasks through `--max-per-task=-1`. The [per-task scores](../results/nc033/core.csv) and [evaluation metric lines](../results/nc033/evaluation-metrics.log) retain the individual results. Standard BPB evaluation uses 20,971,520 tokens per split. See [Benchmark protocol](BENCHMARK.md#core-and-timing) for the centered CORE calculation.

The time comes from the original `total_training_time` metric. The native timer excludes the first eleven update records, evaluation, logging and checkpoint writing; setup and tokenizer preparation are separate. The [training log](../results/nc033/training-native.log) preserves native step and summary lines. It measures the training interval, rather than the complete reproduction process.

The [experiment history](RESULTS.md) also retains nc027 and nc029: earlier MLP5120 recipes run with seed 42. Each row records its own architecture, training horizon, and complete evaluation.

## What is preserved

| Material | Evidence and scope |
|---|---|
| [Published result files](../results/nc033/) | Exact summary metrics, configuration, complete per-task CORE, and selected original training/evaluation lines. Machine-specific startup diagnostics are excluded from the public logs. |
| [Experiment JSON](../results/experiments.json) and [CSV](../results/experiments.csv) | Three completed qualifying experiments and their source identities. Each metrics JSON records the original full-result SHA-256. |
| [Artifact manifest](../results/artifact-manifest.json) | SHA-256 hashes of the published measurements, logs, configuration and public comparison data. |
| [Source manifest](../reproduction/source-manifest.json) | Identities of 22 unchanged source, license and dependency files from the recorded training revision `a72e2f4b16595a3409edc39b00e07e22bee45c09`. |
| [Publication manifest](../reproduction/publication-manifest.json) | Hashes for the frozen code and portable reproduction package; the publication prose and figures are maintained separately. |
| [Input manifest](../reproduction/input-manifest.json) | Names and sizes for 170 training shards and one held-out shard; hashes for the held-out/tokenizer artifacts and 77 evaluation files. Full training-shard content hashes were not recorded. |
| [Recipes](../reproduction/recipes.json) and [environment](../reproduction/environment.json) | Exact launch arguments, model configuration and required package versions. The original FlashAttention 3 hub resolver is retained; its external binary revision is not pinned by the dependency lock. |

The repository distributes source and result evidence. Dataset contents, tokenizer artifacts, trained weights and compiled kernel caches are obtained or produced during reproduction.

## Verify the published package

From the repository root, these Python 3 commands check frozen source identities and published artifact hashes without launching training:

```bash
python3 reproduction/verify.py source
python3 - <<'PY'
import hashlib
import json
from pathlib import Path

manifest = json.loads(Path('results/artifact-manifest.json').read_text())['sha256']
for name, expected in manifest.items():
    actual = hashlib.sha256(Path(name).read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(f'Artifact hash differs: {name}')
print(f'Verified {len(manifest)} published artifacts')
PY
```

The [recorded static validation](../reproduction/static-validation.json) covers source identity, local imports, Python parsing, locked package versions, shell syntax and exact command arguments. The portable launch scripts have been checked in describe mode; their end-to-end GPU execution remains to be validated. The measurements above come from the original archived runs. Follow [Reproduce](REPRODUCE.md) to run the published recipe and validate fresh outputs.
