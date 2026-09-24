# Reproduce GPT-2 Speedrun

## Environment

Use one Linux node with **8×H100 80GB** GPUs and a driver compatible with CUDA 12.8. The dependency lock pins PyTorch 2.9.1, Triton 3.5.1 and Liger 0.8.0. Install `uv`; the setup script selects Python 3.12. Source and dependency identities are listed in [source-manifest.json](../reproduction/source-manifest.json) and [environment.json](../reproduction/environment.json).

```bash
export NANOCHAT_BASE_DIR="$HOME/.cache/gpt2-speedrun"
bash reproduction/install.sh --execute
bash reproduction/prepare_data.sh --execute
```

Data preparation downloads ClimbMix shards, trains the 49,152-token tokenizer with the original code, downloads the canonical evaluation bundle, and checks the input manifest. Data preparation and tokenizer creation happen before benchmark training.

Leave enough disk for the complete dataset, kernel cache, evaluation bundle, logs, and a roughly 9.1 GiB model/optimizer checkpoint. The eight GPUs should be dedicated to the run. GPU scheduling and shared filesystem activity can change measured training time.

## Published 9,841-step recipe

```bash
# Inspect both training and evaluation commands.
bash reproduce.sh 9841

# Train from scratch and run complete evaluation.
bash reproduce.sh 9841 --execute
```

The original code initializes seed 42. The script uses a fresh model tag and does not resume an existing checkpoint. Training completes before independent evaluation starts. CORE uses every example in all 22 tasks; standard BPB uses 20,971,520 tokens per split.

Results are written below:

- `$NANOCHAT_BASE_DIR/benchmark_results/gpt2-mlp4864-9841-seed42/`: commands, logs, CORE and verification result.
- `$NANOCHAT_BASE_DIR/base_checkpoints/gpt2-mlp4864-9841-seed42/`: model, metadata and eight optimizer shards.

Use the native metadata field `loop_state.total_training_time` for the benchmark time. Data/tokenizer setup, evaluation and checkpoint writing are outside the recorded native training interval. The first eleven update records are excluded by the original timer. `time bash reproduce.sh ...` measures the complete process instead.

## Additional recorded recipe

`bash reproduce.sh 9777` prints the subsequent 9,777-update recipe, which uses the same model and source. Its complete experiment was still running when this publication was prepared. It has no published performance result here; the headline and default recommendation remain the completed 9,841-update result.

## Integrity

`reproduction/verify.py` checks the copied source, fixed input identities, required package versions, and complete evaluation outputs. The portable scripts replace machine-specific directory names with environment variables; training and optimizer source files retain their original byte hashes. [Release preparation notes](../reproduction/source-manifest.json).

The measured run used the archived orchestration. The new portable scripts have been checked locally for source identity, import closure, exact command arguments, shell syntax and describe-mode behavior; their end-to-end GPU execution remains to be validated. [Recorded checks](../reproduction/static-validation.json).
