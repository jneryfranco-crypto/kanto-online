#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
ENGINE="$ROOT/engine"
cd "$ENGINE"

# Apply the small compatibility patch against the pinned upstream engine.
# The ledge-landing dust is cosmetic; a missing optional image must not abort boot.
PATCH_FILE="$ROOT/patches/engine/landing-dust-optional.patch"
LANDING_DUST_SOURCE="$ENGINE/src/effects/LandingDustEffect.ts"
if ! grep -q "Landing dust sprite unavailable; landing effect disabled" "$LANDING_DUST_SOURCE"; then
  git -C "$ENGINE" apply --check "$PATCH_FILE"
  git -C "$ENGINE" apply "$PATCH_FILE"
fi

# Run every asset exporter in dependency order. The upstream aggregate script
# validates the player sprite before exporting it, so use the individual stages.
for step in \
  02_extract_layouts.py \
  01_render_metatile_atlases.py \
  03_extract_map_headers.py \
  04_extract_warps.py \
  05_extract_collision.py \
  06_stitch_overworld.py \
  07_export_interiors.py \
  08_extract_sprites.py \
  09_extract_tile_anims.py \
  10_extract_door_anims.py \
  11_extract_surf_sprites.py \
  12_extract_npc_sprites.py
do
  echo
  echo "===== $step ====="
  python3 "scripts/$step"
done

echo
echo "===== Export FireRed field-effect sprites ====="
python3 "$ROOT/extract-field-effects.py"

echo
echo "===== Verify required runtime assets ====="
python3 "$ROOT/validate-runtime-assets.py"
python3 "$ROOT/validate-kanto-route.py"

echo
echo "===== Full validation suite ====="
npm test
