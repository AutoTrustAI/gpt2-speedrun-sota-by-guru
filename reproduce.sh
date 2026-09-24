#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$ROOT_DIR"
[[ $# == 1 || $# == 2 ]] || { printf 'Usage: bash reproduce.sh {9841|9777} [--execute]\n' >&2; exit 2; }
STEPS="$1"
[[ "$STEPS" == 9841 || "$STEPS" == 9777 ]] || { printf 'Choose the frozen9841 or9777 recipe.\n' >&2; exit 2; }
[[ $# == 1 || "$2" == --execute ]] || { printf 'Only --execute is accepted.\n' >&2; exit 2; }
export NANOCHAT_BASE_DIR=${NANOCHAT_BASE_DIR:-"$HOME/.cache/nanochat"}
export HF_HOME=${HF_HOME:-"$NANOCHAT_BASE_DIR/huggingface"}
export TORCHINDUCTOR_CACHE_DIR=${TORCHINDUCTOR_CACHE_DIR:-"$NANOCHAT_BASE_DIR/inductor"}
export OMP_NUM_THREADS=1 PYTHONUNBUFFERED=1 NANOCHAT_DTYPE=bfloat16
PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
TORCHRUN_BIN="$ROOT_DIR/.venv/bin/torchrun"
MODEL_TAG="gpt2-mlp4864-${STEPS}-seed42"
TRAIN_ARGS=(
    --run=dummy
    --device-type=cuda
    --compile-mode=default
    --depth=22
    --aspect-ratio=64
    --head-dim=128
    --max-seq-len=2048
    --window-pattern=SSSL
    --learnable-rmsnorm
    --fp8
    --fp8-recipe=tensorwise
    --liger-cross-entropy
    --device-batch-size=32
    --total-batch-size=524288
    "--num-iterations=${STEPS}"
    --target-param-data-ratio=9.20
    --embedding-lr=0.3
    --unembedding-lr=0.008
    --matrix-lr=0.02
    --scalar-lr=0.5
    --weight-decay=0.28
    --warmup-steps=40
    --warmdown-ratio=0.65
    --final-lr-frac=0.05
    --resume-from-step=-1
    --eval-every=999999
    --core-metric-every=-1
    --sample-every=-1
    --save-every=-1
    --mlp-hidden-dim=4864
    "--model-tag=gpt2-mlp4864-${STEPS}-seed42"
)
EVAL_ARGS=(
    "--model-tag=gpt2-mlp4864-${STEPS}-seed42"
    "--step=${STEPS}"
    --eval=core,bpb
    --max-per-task=-1
    --device-batch-size=16
    --split-tokens=20971520
    --device-type=cuda
)
if [[ $# == 1 ]]; then
    printf '%q ' "$TORCHRUN_BIN" --standalone --nproc_per_node=8 -m scripts.base_train "${TRAIN_ARGS[@]}"; printf '\n'
    printf '%q ' "$TORCHRUN_BIN" --standalone --nproc_per_node=8 -m scripts.base_eval "${EVAL_ARGS[@]}"; printf '\n'
    exit 0
fi
[[ -x "$PYTHON_BIN" && -x "$TORCHRUN_BIN" ]] || { printf 'Run reproduction/install.sh --execute first.\n' >&2; exit 1; }
OUTPUT_DIR="$NANOCHAT_BASE_DIR/benchmark_results/$MODEL_TAG"
CHECKPOINT_DIR="$NANOCHAT_BASE_DIR/base_checkpoints/$MODEL_TAG"
[[ ! -e "$OUTPUT_DIR" && ! -e "$CHECKPOINT_DIR" ]] || { printf 'Fresh run required: output or checkpoint already exists. Use a fresh NANOCHAT_BASE_DIR.\n' >&2; exit 1; }
"$PYTHON_BIN" reproduction/verify.py source
"$PYTHON_BIN" reproduction/verify.py inputs
"$PYTHON_BIN" reproduction/verify.py environment
mkdir -p "$OUTPUT_DIR"
cp reproduction/recipes.json "$OUTPUT_DIR/recipes.json"
cp reproduction/source-manifest.json "$OUTPUT_DIR/source-manifest.json"
printf '%q ' "$TORCHRUN_BIN" --standalone --nproc_per_node=8 -m scripts.base_train "${TRAIN_ARGS[@]}" > "$OUTPUT_DIR/train-command.sh"; printf '\n' >> "$OUTPUT_DIR/train-command.sh"
printf '%q ' "$TORCHRUN_BIN" --standalone --nproc_per_node=8 -m scripts.base_eval "${EVAL_ARGS[@]}" > "$OUTPUT_DIR/eval-command.sh"; printf '\n' >> "$OUTPUT_DIR/eval-command.sh"
"$TORCHRUN_BIN" --standalone --nproc_per_node=8 -m scripts.base_train "${TRAIN_ARGS[@]}" 2>&1 | tee "$OUTPUT_DIR/train.log"
CORE_CSV=$(printf '%s/base_eval/base_model_%06d.csv' "$NANOCHAT_BASE_DIR" "$STEPS")
if [[ -e "$CORE_CSV" ]]; then
    mv "$CORE_CSV" "$OUTPUT_DIR/preexisting-core.csv"
fi
"$TORCHRUN_BIN" --standalone --nproc_per_node=8 -m scripts.base_eval "${EVAL_ARGS[@]}" 2>&1 | tee "$OUTPUT_DIR/eval.log"
cp "$CORE_CSV" "$OUTPUT_DIR/core.csv"
"$PYTHON_BIN" reproduction/verify.py source
"$PYTHON_BIN" reproduction/verify.py inputs
"$PYTHON_BIN" reproduction/verify.py result --steps="$STEPS"
