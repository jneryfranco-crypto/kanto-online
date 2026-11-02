#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
git submodule update --init --recursive
if [ ! -e "$ROOT/engine/decomp" ]; then
  ln -s ../decomp "$ROOT/engine/decomp"
fi
cd "$ROOT/engine"
npm install
python3 -m pip install -r scripts/requirements.txt
npm run extract
npm test
npm run typecheck
printf '\nPreparação concluída. Para iniciar: cd engine && npm run dev\n'
