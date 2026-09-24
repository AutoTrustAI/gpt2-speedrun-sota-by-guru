#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT_DIR"
export NANOCHAT_BASE_DIR=${NANOCHAT_BASE_DIR:-"$HOME/.cache/nanochat"}
export HF_HOME=${HF_HOME:-"$NANOCHAT_BASE_DIR/huggingface"}
PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
if [[ $# == 0 ]]; then
    printf '%s\n' 'Download8 ClimbMix shards + heldout; train49152-vocabulary tokenizer; download170 train shards + heldout; download canonical eval_bundle; verify fixed input identity.' "NANOCHAT_BASE_DIR=$NANOCHAT_BASE_DIR"
    exit 0
fi
[[ $# == 1 && "$1" == --execute ]] || { printf 'Usage: bash reproduction/prepare_data.sh [--execute]\n' >&2; exit 2; }
[[ -x "$PYTHON_BIN" ]] || { printf 'Run reproduction/install.sh --execute first.\n' >&2; exit 1; }
"$PYTHON_BIN" reproduction/verify.py source
# Preparation uses the original data/tokenizer code and does not initialize CUDA.
export CUDA_VISIBLE_DEVICES=""
export NANOCHAT_DTYPE=bfloat16
"$PYTHON_BIN" -m nanochat.dataset -n 8
if [[ -e "$NANOCHAT_BASE_DIR/tokenizer/tokenizer.pkl" || -e "$NANOCHAT_BASE_DIR/tokenizer/token_bytes.pt" ]]; then
    [[ -f "$NANOCHAT_BASE_DIR/tokenizer/tokenizer.pkl" && -f "$NANOCHAT_BASE_DIR/tokenizer/token_bytes.pt" ]] || { printf 'Incomplete existing tokenizer; use a fresh NANOCHAT_BASE_DIR.\n' >&2; exit 1; }
else
    "$PYTHON_BIN" -m scripts.tok_train --vocab-size=49152
fi
"$PYTHON_BIN" -m nanochat.dataset -n 170
"$PYTHON_BIN" - <<'PY'
from pathlib import Path
from nanochat.common import get_base_dir, download_file_with_lock
from scripts.base_eval import EVAL_BUNDLE_URL, place_eval_bundle
base = Path(get_base_dir())
if not (base / 'eval_bundle').exists():
    path = download_file_with_lock(EVAL_BUNDLE_URL, 'eval_bundle.zip')
    place_eval_bundle(path)
PY
"$PYTHON_BIN" reproduction/verify.py inputs
