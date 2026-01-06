import io
import os
import random
import uvicorn
from fastapi import FastAPI, Response
from PIL import Image

CATEGORIES = [
    "body",
    "fur",
    "eyes",
    "mouth",
    "accessories",
]


def get_assets(category: str) -> list[str]:
    """Returns the root path for assets."""
    root = "assets"
    asset_dir = f"{root}/{category}"
    if not os.path.isdir(asset_dir):
        raise ValueError(f"{category} directory does not exist.")
    file_names = [
        os.path.join(category, file_name)
        for file_name in os.listdir(asset_dir)
        if os.path.isfile(os.path.join(asset_dir, file_name))
        and file_name.lower().endswith(".png")
    ]

    if not file_names:
        raise ValueError(f"No assets found for category: {category}")
    return file_names


def get_part_path(category: str, seed: int) -> str:
    """Returns a part name based on category and seed."""
    if category not in CATEGORIES:
        raise ValueError(f"Invalid category: {category}")
    assets = get_assets(category)
    part = random.Random(seed).choice(assets)
    return part


def build_avatar(name: str) -> bytes:
    """Builds an avatar image based on the given name."""
    seed = sum(ord(c) for c in name)

    canvas = Image.new("RGBA", (256, 256))

    for part in CATEGORIES:
        part_path = get_part_path(part, seed)
        part_image = Image.open(os.path.join("assets", part_path)).convert("RGBA")
        canvas.alpha_composite(part_image)

    output_buffer = io.BytesIO()
    canvas.save(output_buffer, format="WEBP")
    return output_buffer.getvalue()


app = FastAPI()
@app.get("/api/avatar/{name}")
def get_avatar(name: str):
    """API endpoint to get avatar image by name."""
    image_data = build_avatar(name)
    return Response(content=image_data, media_type="image/webp")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0", port=8000)
