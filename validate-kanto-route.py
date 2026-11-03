#!/usr/bin/env python3
"""Validate the actual Pallet Town → Viridian Forest → Pewter route."""
import json
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "engine" / "public"
ERRORS: list[str] = []

def load_json(path: Path):
    if not path.is_file():
        ERRORS.append(f"Missing route data: {path.relative_to(PUBLIC)}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        ERRORS.append(f"Invalid route data {path}: {exc}")
        return None

def layer_data(map_json, name: str):
    if not map_json:
        return None
    return next(
        (layer.get("data") for layer in map_json.get("layers", [])
         if layer.get("type") == "tilelayer" and layer.get("name") == name),
        None,
    )

def object_warps(map_json):
    if not map_json:
        return []
    layer = next(
        (layer for layer in map_json.get("layers", [])
         if layer.get("type") == "objectgroup" and layer.get("name") == "warps"),
        None,
    )
    result = []
    for obj in (layer or {}).get("objects", []):
        props = {p.get("name"): p.get("value") for p in obj.get("properties", [])}
        result.append({
            "dest": str(props.get("destMap", "")),
            "x": int(obj.get("x", 0)) // 16,
            "y": int(obj.get("y", 0)) // 16,
        })
    return result

def flood(width: int, height: int, collision: list[int], start: tuple[int, int]) -> set[tuple[int, int]]:
    sx, sy = start
    if not (0 <= sx < width and 0 <= sy < height):
        return set()
    if collision[sy * width + sx] != 0:
        return set()
    seen = {start}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                point = (nx, ny)
                if point not in seen and collision[ny * width + nx] == 0:
                    seen.add(point)
                    queue.append(point)
    return seen

def in_zone(point: tuple[int, int], bounds: dict) -> bool:
    x, y = point
    return (
        bounds["x"] <= x < bounds["x"] + bounds["width"]
        and bounds["y"] <= y < bounds["y"] + bounds["height"]
    )

def main() -> int:
    overworld = load_json(PUBLIC / "maps" / "overworld.json")
    zones_data = load_json(PUBLIC / "data" / "overworld_zones.json")
    warp_data = load_json(PUBLIC / "data" / "warp_table.json")
    if not all((overworld, zones_data, warp_data)):
        return 1

    width, height = int(overworld["width"]), int(overworld["height"])
    collision = layer_data(overworld, "collision")
    if collision is None or len(collision) != width * height:
        ERRORS.append("Overworld collision grid is missing or has the wrong size")
        return 1

    zones = {zone["id"]: zone["bounds"] for zone in zones_data.get("zones", [])}
    required_zones = ("MAP_ROUTE1", "MAP_VIRIDIAN_CITY", "MAP_ROUTE2", "MAP_PEWTER_CITY")
    for zone_id in required_zones:
        if zone_id not in zones:
            ERRORS.append(f"Main Kanto route is missing zone {zone_id}")

    # The real initial spawn reported by the browser smoke test.
    south_reachable = flood(width, height, collision, (80, 278))
    if not south_reachable:
        ERRORS.append("Pallet Town spawn (80,278) is not a walkable tile")
    else:
        for zone_id in ("MAP_ROUTE1", "MAP_VIRIDIAN_CITY", "MAP_ROUTE2"):
            if zone_id in zones and not any(in_zone(p, zones[zone_id]) for p in south_reachable):
                ERRORS.append(f"{zone_id} cannot be reached on foot from the Pallet Town spawn")

    overworld_warps = warp_data.get("overworldWarps", [])
    south_entries = [
        (int(w["overworldX"]), int(w["overworldY"]))
        for w in overworld_warps
        if w.get("destMap") == "MAP_ROUTE2_VIRIDIAN_FOREST_SOUTH_ENTRANCE"
    ]
    north_entries = [
        (int(w["overworldX"]), int(w["overworldY"]))
        for w in overworld_warps
        if w.get("destMap") == "MAP_ROUTE2_VIRIDIAN_FOREST_NORTH_ENTRANCE"
    ]
    if not any(p in south_reachable for p in south_entries):
        ERRORS.append("The south Viridian Forest entrance cannot be reached from Pallet Town")

    # The forest is the bridge between the two otherwise disconnected Route 2 sides.
    north_reachable = set()
    for point in north_entries:
        north_reachable = flood(width, height, collision, point)
        if north_reachable:
            break
    if not north_reachable:
        ERRORS.append("The north Viridian Forest exit does not lead to a walkable Route 2 tile")
    elif "MAP_PEWTER_CITY" in zones and not any(
        in_zone(p, zones["MAP_PEWTER_CITY"]) for p in north_reachable
    ):
        ERRORS.append("Pewter City cannot be reached on foot from the north Viridian Forest exit")

    interiors = PUBLIC / "maps" / "interiors"
    south_gate = load_json(interiors / "MAP_ROUTE2_VIRIDIAN_FOREST_SOUTH_ENTRANCE.json")
    forest = load_json(interiors / "MAP_VIRIDIAN_FOREST.json")
    north_gate = load_json(interiors / "MAP_ROUTE2_VIRIDIAN_FOREST_NORTH_ENTRANCE.json")

    def has_destination(map_json, destination: str) -> bool:
        return any(w["dest"] == destination for w in object_warps(map_json))

    if not has_destination(south_gate, "MAP_VIRIDIAN_FOREST"):
        ERRORS.append("South Route 2 gatehouse has no warp into Viridian Forest")
    if not has_destination(forest, "MAP_ROUTE2_VIRIDIAN_FOREST_NORTH_ENTRANCE"):
        ERRORS.append("Viridian Forest has no north exit to the Route 2 gatehouse")
    if not has_destination(north_gate, "MAP_ROUTE2"):
        ERRORS.append("North Route 2 gatehouse has no return warp to Route 2")

    if ERRORS:
        print(f"FAIL: {len(ERRORS)} main-route errors")
        for error in ERRORS:
            print(f"  - {error}")
        return 1

    print(
        "PASS: Pallet Town → Route 1 → Viridian City → Route 2 south → "
        "Viridian Forest → Route 2 north → Pewter City"
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
