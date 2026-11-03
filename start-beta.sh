#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
ENGINE="$ROOT/engine"
if [[ ! -d "$ENGINE/node_modules" ]]; then
  echo "Dependências não instaladas. Execute primeiro: bash ./setup-map.sh" >&2
  exit 1
fi
if [[ ! -f "$ENGINE/public/maps/overworld.json" ]]; then
  echo "Mapas ainda não extraídos. Execute primeiro: bash ./setup-map.sh" >&2
  exit 1
fi
cd "$ENGINE"
echo "Kanto Online Beta local: http://127.0.0.1:3000"
echo "Mantenha este terminal aberto enquanto joga. Ctrl+C encerra o servidor."
npm run dev -- --host 127.0.0.1
