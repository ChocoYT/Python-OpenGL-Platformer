import json, os
from PIL       import Image
from OpenGL.GL import *

from texture_array import TextureArray

def load_directory(root: str) -> dict:
    image_paths = []
    meta  = {}
    match = {}

    # Collect Images and JSONs
    for current_dir, _, files in os.walk(root):
        pngs = [f for f in files if f.lower().endswith(".png")]
        jsons = [f for f in files if f.lower().endswith(".json")]

        # Match JSON to PNG
        for json_file in jsons:
            base = os.path.splitext(json_file)[0]
            for png_file in pngs:
                if os.path.splitext(png_file)[0] == base:
                    match[os.path.join(current_dir, json_file)] = os.path.join(current_dir, png_file)

        # Collect Images
        for file in pngs:
            full_path = os.path.join(current_dir, file)
            if can_load(full_path):
                image_paths.append(full_path)

    textures = TextureArray(image_paths)

    # Inject Layer Index
    layer_map = {path: i for i, path in enumerate(image_paths)}
    
    for json_path, img_path in match.items():
        layer = layer_map[img_path]

        with open(json_path, "r") as f:
            data = json.load(f)

        if "tiles" in data:
            if "tiles" not in meta:
                meta["tiles"] = {}
            for name, coords in data["tiles"].items():
                x, y = coords
                meta["tiles"][name] = [x, y, layer]

        if "tile_size" in data:
            if "tile_size" not in meta:
                meta["tile_size"] = data["tile_size"]
            elif meta["tile_size"] != data["tile_size"]:
                print(f"Warning: Tile size mismatch in {json_path}")

    return {"textures": textures, "meta": meta}

def can_load(path: str) -> bool:
    try:
        with Image.open(path) as img:
            img.verify()
        return True
    except Exception:
        return False

assets = {}

def load_assets() -> None:
    global assets
    assets = load_directory("Assets")
