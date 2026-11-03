#!/usr/bin/env python3
"""Export browser-ready FireRed field-effect sprites into the engine's public assets."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "decomp" / "graphics" / "field_effects" / "pics" / "tall_grass.png"
DEST = ROOT / "engine" / "public" / "sprites" / "tall_grass.png"

def main() -> None:
    if not SOURCE.is_file():
        raise SystemExit(f"Missing FireRed source asset: {SOURCE}")
    DEST.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(SOURCE) as source:
        source.load()
        rgba = source.convert("RGBA")
        if rgba.size != (16, 80):
            raise SystemExit(
                f"Unexpected tall_grass.png dimensions: {rgba.width}x{rgba.height}; "
                "expected 16x80 (five 16x16 animation frames)"
            )
        rgba.save(DEST, format="PNG", optimize=True)
    with Image.open(DEST) as check:
        check.verify()
    print(f"  Exported browser-ready tall grass animation: {DEST} (16x80 RGBA PNG)")

if __name__ == "__main__":
    main()
