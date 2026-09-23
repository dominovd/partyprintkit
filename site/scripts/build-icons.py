#!/usr/bin/env python3
"""Site icon: a two-tone pennant, the thing the site actually makes.

One shape, three colours, no lettering: at 16 px a letter is mush and a
silhouette still reads. No hole marks either, two dots near the top read as a
face once the icon is large. Run after changing the palette.

    python3 scripts/build-icons.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

TEAL = (31, 94, 96, 255)
CREAM = (255, 253, 248, 255)
CORAL = (235, 114, 91, 255)

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="PartyPrintKit">
  <rect width="64" height="64" rx="14" fill="#1F5E60"/>
  <path d="M17 11H47V40L32 53L17 40Z" fill="#FFFDF8"/>
  <path d="M17 35H47V40L32 53L17 40Z" fill="#EB725B"/>
</svg>
"""


def draw_icon(size: int, radius_ratio: float = 14 / 64) -> Image.Image:
    """Draw at 4x and downsample: PIL has no antialiasing on polygons."""
    scale = 4
    s = size * scale
    image = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    unit = s / 64

    if radius_ratio:
        draw.rounded_rectangle([0, 0, s - 1, s - 1], radius=radius_ratio * s, fill=TEAL)
    else:
        draw.rectangle([0, 0, s - 1, s - 1], fill=TEAL)

    flag = [(17, 11), (47, 11), (47, 40), (32, 53), (17, 40)]
    draw.polygon([(x * unit, y * unit) for x, y in flag], fill=CREAM)

    skirt = [(17, 35), (47, 35), (47, 40), (32, 53), (17, 40)]
    draw.polygon([(x * unit, y * unit) for x, y in skirt], fill=CORAL)

    return image.resize((size, size), Image.LANCZOS)


def main() -> None:
    PUBLIC.mkdir(parents=True, exist_ok=True)

    (PUBLIC / "favicon.svg").write_text(SVG)

    # .ico carries three sizes; browsers and Windows pick what they need.
    ico = draw_icon(64)
    ico.save(PUBLIC / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

    # iOS masks the icon itself, so this one is full-bleed.
    draw_icon(180, radius_ratio=0).save(PUBLIC / "apple-touch-icon.png")

    for size in (192, 512):
        draw_icon(size).save(PUBLIC / f"icon-{size}.png")

    for name in ("favicon.svg", "favicon.ico", "apple-touch-icon.png", "icon-192.png", "icon-512.png"):
        print(PUBLIC / name)


if __name__ == "__main__":
    main()
