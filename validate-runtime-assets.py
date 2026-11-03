#!/usr/bin/env python3
"""Fail fast when an asset exporter omitted or corrupted a runtime asset."""
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "engine" / "public"
ERRORS: list[str] = []

def require_file(relative: str) -> Path | None:
    path = PUBLIC / relative
    if not path.is_file() or path.stat().st_size == 0:
        ERRORS.append(f"Missing or empty runtime asset: public/{relative}")
        return None
    return path

def read_json(relative: str):
    path = require_file(relative)
    if path is None:
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        ERRORS.append(f"Invalid JSON public/{relative}: {exc}")
        return None

def check_image(relative: str, expected_size: tuple[int, int] | None = None) -> None:
    path = require_file(relative)
    if path is None:
        return
    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            if expected_size and image.size != expected_size:
                ERRORS.append(
                    f"Wrong dimensions public/{relative}: {image.width}x{image.height}; "
                    f"expected {expected_size[0]}x{expected_size[1]}"
                )
    except Exception as exc:
        ERRORS.append(f"Invalid image public/{relative}: {exc}")

def main() -> int:
    # Core world and player assets used during initial boot.
    for rel in (
        "maps/overworld.json",
        "data/overworld_zones.json",
        "data/warp_table.json",
        "sprites/player.json",
    ):
        require_file(rel)
    check_image("sprites/player_male.png", (48, 128))
    check_image("sprites/tall_grass.png", (16, 80))

    # Every animation manifest must resolve to real, decodable files.
    tile_manifest = read_json("data/tile_anims.json")
    if tile_manifest is not None:
        for tileset, data in tile_manifest.get("tilesets", {}).items():
            for anim in data.get("animations", []):
                for key in ("atlasImage", "atlasTopImage"):
                    rel = f"tilesets/{anim.get(key, '')}"
                    path = require_file(rel)
                    if path:
                        try:
                            with Image.open(path) as image:
                                image.verify()
                        except Exception as exc:
                            ERRORS.append(f"Invalid animation atlas public/{rel}: {exc}")

    door_manifest = read_json("data/door_anims.json")
    if door_manifest is not None:
        for key, door in door_manifest.items():
            rel = f"sprites/{door.get('image', '')}"
            path = require_file(rel)
            if path:
                try:
                    with Image.open(path) as image:
                        image.verify()
                except Exception as exc:
                    ERRORS.append(f"Invalid door animation public/{rel} ({key}): {exc}")

    check_image("sprites/player_surf.png", (16, 128))
    check_image("sprites/surf_blob.png", (256, 32))
    read_json("sprites/surf_blob.json")

    npc_manifest = read_json("sprites/npcs/manifest.json")
    if npc_manifest is not None:
        for name, sprite in npc_manifest.get("sprites", {}).items():
            rel = f"sprites/npcs/{sprite.get('sheet', '')}"
            path = require_file(rel)
            if path:
                try:
                    with Image.open(path) as image:
                        image.verify()
                except Exception as exc:
                    ERRORS.append(f"Invalid NPC sprite public/{rel} ({name}): {exc}")

    if ERRORS:
        print(f"FAIL: {len(ERRORS)} runtime asset errors")
        for error in ERRORS:
            print(f"  - {error}")
        return 1

    print("PASS: core maps, player, field effects, tile/door animations, surf and NPC assets are present and valid")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
