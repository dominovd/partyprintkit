#!/usr/bin/env python3
"""Build distinct 1000 x 1500 previews from the actual geometric PDFs."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output" / "pdf"
DOWNLOADS = ROOT / "site" / "public" / "downloads"
SOCIAL = ROOT / "site" / "public" / "social"
PHOTOS = ROOT / "site" / "src" / "assets" / "photos"
import shutil

PDFTOPPM = Path(
    next(
        (
            candidate
            for candidate in (
                "/Users/denis/.cache/codex-runtimes/codex-primary-runtime/"
                "dependencies/bin/override/pdftoppm",
                shutil.which("pdftoppm") or "",
            )
            if candidate and Path(candidate).exists()
        ),
        "pdftoppm",
    )
)
FONT_ROOT = Path(
    next(
        (
            str(candidate)
            for candidate in (
                Path(__file__).resolve().parent / "fonts",
                Path(
                    "/Users/denis/.cache/codex-runtimes/codex-primary-runtime/dependencies/"
                    "node/node_modules/pdfjs-dist/standard_fonts"
                ),
                Path("/usr/share/fonts/truetype/liberation"),
                Path("/usr/share/fonts/truetype/liberation2"),
            )
            if (candidate / "LiberationSans-Regular.ttf").exists()
        ),
        "",
    )
)

W, H = 1000, 1500
PAPER = "#FBF6EC"
INK = "#18383A"
TEAL = "#1E706C"
CORAL = "#ED7059"
GOLD = "#E9A93F"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf"
    return ImageFont.truetype(str(FONT_ROOT / name), size=size)


def render_page(pdf: Path, page: int) -> Image.Image:
    with tempfile.TemporaryDirectory(prefix="ppk-preview-") as temp:
        prefix = Path(temp) / "page"
        subprocess.run(
            [
                str(PDFTOPPM),
                "-f",
                str(page),
                "-l",
                str(page),
                "-singlefile",
                "-png",
                "-r",
                "130",
                str(pdf),
                str(prefix),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return Image.open(prefix.with_suffix(".png")).convert("RGB").copy()


def fit(image: Image.Image, width: int, height: int) -> Image.Image:
    copy = image.copy()
    copy.thumbnail((width, height), Image.Resampling.LANCZOS)
    return copy


def card(image: Image.Image, width: int, height: int, angle: float = 0) -> Image.Image:
    image = fit(image, width, height)
    pad = 18
    shadow_pad = 24
    layer = Image.new("RGBA", (image.width + 2 * shadow_pad, image.height + 2 * shadow_pad))
    shadow = Image.new("RGBA", layer.size)
    ImageDraw.Draw(shadow).rounded_rectangle(
        (shadow_pad - pad, shadow_pad - pad, shadow_pad + image.width + pad, shadow_pad + image.height + pad),
        radius=14,
        fill=(24, 56, 58, 58),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(13))
    layer.alpha_composite(shadow)
    paper = Image.new("RGBA", (image.width + 2 * pad, image.height + 2 * pad), "white")
    paper.alpha_composite(image.convert("RGBA"), (pad, pad))
    layer.alpha_composite(paper, (shadow_pad - pad, shadow_pad - pad))
    if angle:
        layer = layer.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    return layer


def paste_center(canvas: Image.Image, layer: Image.Image, x: int, y: int) -> None:
    canvas.alpha_composite(layer, (int(x - layer.width / 2), int(y - layer.height / 2)))


def base(title: str, subtitle: str, accent: str) -> Image.Image:
    image = Image.new("RGBA", (W, H), PAPER)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, W, 20), fill=accent)
    draw.text((70, 74), "FREE PRINTABLE · NO SIGN-UP", font=font(23, True), fill=accent)
    draw.text((70, 122), title, font=font(58, True), fill=INK)
    draw.text((72, 205), subtitle, font=font(27), fill=INK)
    draw.text((70, 1435), "partyprintkit.com", font=font(24, True), fill=INK)
    return image


def build_kit_preview(pages: dict[int, Image.Image]) -> Image.Image:
    image = base(
        "Birthday Party Kit",
        "Banner · hats · toppers · signs · tags",
        TEAL,
    )
    paste_center(image, card(pages[1], 420, 600, -4), 280, 610)
    paste_center(image, card(pages[14], 360, 510, 4), 715, 590)
    paste_center(image, card(pages[16], 330, 470, 2), 245, 1115)
    paste_center(image, card(pages[17], 315, 445, -2), 520, 1110)
    paste_center(image, card(pages[19], 285, 405, 3), 790, 1120)
    return image


def build_banner_preview(pages: dict[int, Image.Image]) -> Image.Image:
    image = base(
        "Happy Birthday Banner",
        "13 true-size 5 x 7 in flags · A4 and US Letter",
        CORAL,
    )
    paste_center(image, card(pages[3], 500, 710, 7), 685, 770)
    paste_center(image, card(pages[2], 520, 740, -5), 350, 785)
    paste_center(image, card(pages[1], 560, 795, 1), 510, 800)
    return image


def build_hat_preview(pages: dict[int, Image.Image]) -> Image.Image:
    image = base(
        "Printable Party Hat",
        "2 true-size cones - R95 mm sector - A4 and US Letter",
        TEAL,
    )
    paste_center(image, card(pages[2], 470, 665, 6), 640, 800)
    paste_center(image, card(pages[1], 520, 740, -4), 400, 815)
    return image


def build_alphabet_preview(pages: dict[int, Image.Image]) -> Image.Image:
    image = base(
        "Printable Banner Letters",
        "A-Z · 0-9 · punctuation · blank flag",
        GOLD,
    )
    paste_center(image, card(pages[31], 430, 610, 6), 730, 790)
    paste_center(image, card(pages[42], 430, 610, -6), 275, 790)
    paste_center(image, card(pages[1], 520, 740, 0), 505, 815)
    return image


PIECE_W, PIECE_H = 1000, 1250

# Which page of the kit PDF actually shows each piece.
PIECE_PAGES = {
    "piece-banner": ((1, 2), "Party banners", "13 flags, 5 x 7 in", CORAL),
    "piece-hat": ((14,), "Party hats", "Cut, roll, glue the tab", TEAL),
    "piece-topper": ((16,), "Cupcake toppers", "12 circles per sheet", GOLD),
    "piece-sign": ((17,), "Party signs", "5 x 7 in, frame or easel", TEAL),
    "piece-tag": ((19,), "Favor tags", "6 tags, punch and tie", CORAL),
}


def build_piece_card(pages: list[Image.Image], title: str, subtitle: str, accent: str) -> Image.Image:
    """A card showing the piece as the PDF actually draws it.

    The card image is the product, not a mood photograph of a different
    product: a visitor who arrives on the picture downloads what they saw.
    """
    image = Image.new("RGBA", (PIECE_W, PIECE_H), PAPER)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, PIECE_W, 14), fill=accent)

    if len(pages) > 1:
        paste_center(image, card(pages[1], 430, 610, 6), 620, 590)
        paste_center(image, card(pages[0], 470, 665, -4), 420, 610)
    else:
        paste_center(image, card(pages[0], 560, 790, -2), 500, 600)

    draw.text((62, 1058), title, font=font(46, True), fill=INK)
    draw.text((64, 1120), subtitle, font=font(26), fill=INK)
    draw.text((64, 1175), "partyprintkit.com", font=font(22, True), fill=accent)
    return image


def save_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(path, format="PNG", optimize=True)


def save_jpg(image: Image.Image, path: Path, accent: str) -> None:
    social = image.copy()
    draw = ImageDraw.Draw(social)
    draw.rounded_rectangle((650, 65, 930, 118), radius=26, fill=accent)
    draw.text((690, 78), "SAVE & PRINT", font=font(19, True), fill="white")
    path.parent.mkdir(parents=True, exist_ok=True)
    social.convert("RGB").save(path, format="JPEG", quality=92, optimize=True)


# Only designs with their own hung photograph are released on the site
# (PRODUCT.md section 7, level 3). Minimal has PDFs but no photo yet, so it
# gets no public asset: an unreferenced file in downloads/ is defect H.
RELEASED = ("botanical", "geometric")
# The home page features one kit, so only that design needs kit rasters.
# Anything else would land in downloads/ with no page linking to it.
HOME_DESIGN = "geometric"
LETTERS_DESIGN = "geometric"


def main() -> None:
    written = []
    for design in RELEASED:
        kit_pdf = OUTPUT / f"birthday-kit-{design}-a4.pdf"
        kit_pages = {page: render_page(kit_pdf, page) for page in (1, 2, 3, 14, 16, 17, 19)}
        kit = build_kit_preview(kit_pages)
        banner = build_banner_preview(kit_pages)

        banner_png = DOWNLOADS / f"birthday-banner-{design}-1000x1500.png"
        save_png(banner, banner_png)
        save_jpg(banner, SOCIAL / f"birthday-banner-{design}-1000x1500.jpg", CORAL)
        # The on-page vertical slot shows the sheet of this very design.
        save_png(banner, PHOTOS / f"sheet-birthday-banner-{design}.png")
        written.append(banner_png)

        hat_pdf = OUTPUT / f"party-hat-{design}-a4.pdf"
        hat_pages = {number: render_page(hat_pdf, number) for number in (1, 2)}
        hat = build_hat_preview(hat_pages)
        hat_png = DOWNLOADS / f"party-hat-{design}-1000x1500.png"
        save_png(hat, hat_png)
        save_jpg(hat, SOCIAL / f"party-hat-{design}-1000x1500.jpg", TEAL)
        save_png(hat, PHOTOS / f"sheet-party-hat-{design}.png")
        written.append(hat_png)
        if design == HOME_DESIGN:
            kit_png = DOWNLOADS / f"birthday-kit-{design}-1000x1500.png"
            save_png(kit, kit_png)
            save_jpg(kit, SOCIAL / f"birthday-kit-{design}-1000x1500.jpg", TEAL)
            written.append(kit_png)

    alphabet_pdf = OUTPUT / f"banner-letters-{LETTERS_DESIGN}-a4.pdf"
    alphabet_pages = {page: render_page(alphabet_pdf, page) for page in (1, 31, 42)}
    alphabet = build_alphabet_preview(alphabet_pages)
    alphabet_png = DOWNLOADS / f"banner-letters-{LETTERS_DESIGN}-1000x1500.png"
    save_png(alphabet, alphabet_png)
    save_jpg(alphabet, SOCIAL / f"banner-letters-{LETTERS_DESIGN}-1000x1500.jpg", GOLD)
    save_png(alphabet, PHOTOS / "letters-alphabet-sheet.png")
    written.append(alphabet_png)

    # Product cards for the five piece slots on the site.
    kit_pdf = OUTPUT / f"birthday-kit-{HOME_DESIGN}-a4.pdf"
    for slot, (numbers, title, subtitle, accent) in PIECE_PAGES.items():
        rendered = [render_page(kit_pdf, number) for number in numbers]
        save_png(build_piece_card(rendered, title, subtitle, accent), PHOTOS / f"{slot}.png")
        written.append(PHOTOS / f"{slot}.png")

    for path in written:
        print(path)


if __name__ == "__main__":
    main()
