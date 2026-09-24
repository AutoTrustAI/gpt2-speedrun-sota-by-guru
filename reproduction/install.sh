#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT_DIR"
if [[ $# == 0 ]]; then
    printf '%s\n' 'uv sync --locked --python 3.12 --extra gpu --extra liger'
    exit 0
fi
[[ $# == 1 && "$1" == --execute ]] || { printf 'Usage: bash reproduction/install.sh [--execute]\n' >&2; exit 2; }
command -v uv >/dev/null || { printf 'Install uv before running this script.\n' >&2; exit 1; }
python3 reproduction/verify.py source
uv sync --locked --python 3.12 --extra gpu --extra liger
