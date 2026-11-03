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

    # The bottom layer must never reference a fully transparent metatile.
    # This catches broken primary/secondary tileset pairing before a black map ships.
    overworld = read_json("maps/overworld.json")
    if overworld is not None:
        bottom_layer = next(
            (layer for layer in overworld.get("layers", [])
             if layer.get("name") == "bottom" and layer.get("type") == "tilelayer"),
            None,
        )
        if bottom_layer is None:
            ERRORS.append("Overworld is missing its bottom tile layer")
        else:
            tileset_refs = sorted(overworld.get("tilesets", []), key=lambda item: item["firstgid"])
            atlas_cache = {}
            tileset_cache = {}
            used_gids = sorted({int(gid) for gid in bottom_layer.get("data", []) if int(gid) > 0})
            for gid in used_gids:
                candidates = [ref for ref in tileset_refs if int(ref["firstgid"]) <= gid]
                if not candidates:
                    ERRORS.append(f"Bottom layer GID {gid} has no tileset")
                    continue
                ref = candidates[-1]
                source = ref["source"]
                if source not in tileset_cache:
                    tileset_cache[source] = read_json(f"tilesets/{source}")
                tsj = tileset_cache[source]
                if tsj is None:
                    continue
                local_id = gid - int(ref["firstgid"])
                tile_count = int(tsj.get("tilecount", 0))
                if local_id < 0 or local_id >= tile_count:
                    ERRORS.append(
                        f"Bottom layer GID {gid} exceeds {source} tilecount ({tile_count})"
                    )
                    continue
                if source not in atlas_cache:
                    image_path = f"tilesets/{tsj.get('image', '')}"
                    atlas_file = require_file(image_path)
                    if atlas_file is None:
                        continue
                    try:
                        atlas_cache[source] = Image.open(atlas_file).convert("RGBA")
                    except Exception as exc:
                        ERRORS.append(f"Cannot open bottom atlas public/{image_path}: {exc}")
                        continue
                atlas = atlas_cache.get(source)
                if atlas is None:
                    continue
                columns = int(tsj.get("columns", 0))
                tile_w = int(tsj.get("tilewidth", 0))
                tile_h = int(tsj.get("tileheight", 0))
                if columns <= 0 or tile_w <= 0 or tile_h <= 0:
                    ERRORS.append(f"Invalid tile geometry in {source}")
                    continue
                px = (local_id % columns) * tile_w
                py = (local_id // columns) * tile_h
                tile = atlas.crop((px, py, px + tile_w, py + tile_h))
                if tile.getchannel("A").getbbox() is None:
                    ERRORS.append(
                        f"Used bottom tile GID {gid} ({source}, local tile {local_id}) is fully transparent"
                    )
            for atlas in atlas_cache.values():
                atlas.close()
            print(f"  Checked {len(used_gids)} unique bottom-layer tile GIDs for transparency")

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
