#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
git submodule update --init --recursive
if [ ! -e "$ROOT/engine/decomp" ]; then
  ln -s ../decomp "$ROOT/engine/decomp"
fi
cd "$ROOT/engine"
npm ci
python3 -m pip install -r scripts/requirements.txt
cd "$ROOT"
bash ./extract-map.sh
cd "$ROOT/engine"
npm run typecheck
npm run build
printf '\nPreparação concluída. Para iniciar: npm run dev\n'
