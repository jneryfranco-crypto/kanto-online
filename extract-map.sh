#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT/engine"

# The upstream extract_all.py validates the player sprite before its own
# sprite-export step. Run the same stages in dependency order instead.
for step in \
  01_render_metatile_atlases.py \
  02_extract_layouts.py \
  03_extract_map_headers.py \
  04_extract_warps.py \
  05_extract_collision.py \
  06_stitch_overworld.py \
  07_export_interiors.py \
  08_extract_sprites.py
do
  echo
  echo "===== $step ====="
  python3 "scripts/$step"
done

echo
echo "===== Full validation suite ====="
npm test
