#!/usr/bin/env python3
"""Export browser-ready FireRed field-effect sprites into the engine's public assets."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "decomp" / "graphics" / "field_effects" / "pics"
DEST_DIR = ROOT / "engine" / "public" / "sprites"


def export_sprite(source_path: Path, dest_path: Path, expected_size: tuple[int, int], description: str) -> None:
    if not source_path.is_file():
        raise SystemExit(f"Missing FireRed source asset: {source_path}")
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source_path) as source:
        source.load()
        rgba = source.convert("RGBA")
        if rgba.size != expected_size:
            raise SystemExit(
                f"Unexpected {source_path.name} dimensions: {rgba.width}x{rgba.height}; "
                f"expected {expected_size[0]}x{expected_size[1]} ({description})"
            )
        rgba.save(dest_path, format="PNG", optimize=True)
    with Image.open(dest_path) as check:
        check.verify()
    print(f"  Exported {description}: {dest_path} ({expected_size[0]}x{expected_size[1]} RGBA PNG)")


def main() -> None:
    export_sprite(
        SOURCE_DIR / "tall_grass.png",
        DEST_DIR / "tall_grass.png",
        (16, 80),
        "FireRed tall grass animation (five 16x16 frames)",
    )
    export_sprite(
        SOURCE_DIR / "ground_impact_dust.png",
        DEST_DIR / "landing_dust.png",
        (16, 24),
        "FireRed landing dust animation (three 16x8 frames)",
    )


if __name__ == "__main__":
    main()
