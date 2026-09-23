#!/usr/bin/env python3
"""Build one release-quality PartyPrintKit product: birthday x geometric.

The two PDFs are rendered independently for A4 and US Letter. Physical piece
dimensions stay identical; only the paper canvas changes.
"""

from __future__ import annotations

import math
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, LETTER
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "pdf"
FONT_CANDIDATES = (
    Path(__file__).resolve().parent / "fonts",
    Path(
        "/Users/denis/.cache/codex-runtimes/codex-primary-runtime/dependencies/"
        "node/node_modules/pdfjs-dist/standard_fonts"
    ),
    Path("/usr/share/fonts/truetype/liberation"),
    Path("/usr/share/fonts/truetype/liberation2"),
    Path("/Library/Fonts"),
)


def font_root() -> Path:
    for candidate in FONT_CANDIDATES:
        if (candidate / "LiberationSans-Regular.ttf").exists():
            return candidate
    raise SystemExit(
        "LiberationSans-Regular.ttf not found. Looked in:\n  "
        + "\n  ".join(str(c) for c in FONT_CANDIDATES)
    )

DISPLAY = "PPK-LiberationSans-Bold"
SERVICE = "PPK-LiberationSans-Regular"

INK = HexColor("#18383A")
TEAL = HexColor("#1E706C")
CORAL = HexColor("#ED7059")
GOLD = HexColor("#E9A93F")
CUT = HexColor("#999999")
TEAL_DEEP = HexColor("#1F5E60")
SAGE = HexColor("#7E9A6B")

# Three designs for the whole site (PRODUCT.md section 1). The palette matches
# the swatch shown by the design switcher in src/data/kits.ts, so the file a
# visitor downloads looks like the option they clicked.
DESIGNS = {
    "botanical": {"label": "Botanical", "colors": (TEAL_DEEP, CORAL, SAGE), "motif": "leaf"},
    "geometric": {"label": "Geometric", "colors": (TEAL, CORAL, GOLD), "motif": "geometric"},
    "minimal": {"label": "Minimal", "colors": (INK, CORAL, INK), "motif": "rule"},
}
ACTIVE = DESIGNS["geometric"]


def palette():
    return ACTIVE["colors"]

FLAGS = list("HAPPYBIRTHDAY")
ALPHABET_MARKS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789&!?.,'-") + [""]
KIT_PAGES = 19

PAGE_MARGIN = 15 * mm
CUT_WIDTH = 0.25
SAFE_INSET = 4 * mm


def register_fonts() -> None:
    pdfmetrics.registerFont(
        TTFont(SERVICE, str(font_root() / "LiberationSans-Regular.ttf"), subfontIndex=0)
    )
    pdfmetrics.registerFont(
        TTFont(DISPLAY, str(font_root() / "LiberationSans-Bold.ttf"), subfontIndex=0)
    )


PRODUCT_META = {
    "kit": (
        "Free Printable Birthday Party Kit",
        'Print at 100% or "Actual size". Cut on the 0.25 pt dashed lines. '
        "Birthday banner, party hats, cupcake toppers, signs and favor tags.",
        "free printable birthday party kit, happy birthday banner, {design} party decorations",
    ),
    "banner": (
        "Free Printable Happy Birthday Banner",
        'Print at 100% or "Actual size". Cut on the 0.25 pt dashed lines. '
        "Thirteen letter flags spelling HAPPY BIRTHDAY.",
        "happy birthday banner printable, free printable happy birthday banner, "
        "birthday banner printable pdf",
    ),
    "hat": (
        "Free Printable Party Hat Template",
        'Print at 100% or "Actual size". Cut the sector, roll it into a cone and '
        "glue the marked tab. Two hats, true size.",
        "printable party hat template, party hat pattern printable, "
        "free printable party hat template pdf",
    ),
    "alphabet": (
        "Printable Banner Letters",
        "Full printable banner alphabet. Print at 100% or Actual size; "
        "cut the dashed outline.",
        "printable banner letters, banner alphabet, {design} party banner",
    ),
}


def set_metadata(c: canvas.Canvas, paper_name: str, product: str) -> None:
    title, subject, keywords = PRODUCT_META[product]
    label = ACTIVE["label"]
    c.setTitle(f"{title} - {label} - {paper_name}")
    c.setSubject(subject)
    c.setCreator("partyprintkit.com")
    c.setAuthor("partyprintkit.com")
    c.setKeywords(keywords.format(design=label.lower()))


def page_header(c: canvas.Canvas, page_size, text: str) -> None:
    _, height = page_size
    c.setFillColor(INK)
    c.setFont(SERVICE, 8)
    c.drawString(15.5 * mm, height - 18 * mm, text)


def page_footer(
    c: canvas.Canvas, page_size, page_num: int, total_pages: int, code: str
) -> None:
    width, _ = page_size
    c.setFillColor(INK)
    c.setFont(SERVICE, 8)
    c.drawCentredString(
        width / 2,
        17.5 * mm,
        f"partyprintkit.com  |  print at 100% (Actual size)  |  {page_num}/{total_pages}  |  {code}",
    )


def set_cut_style(c: canvas.Canvas) -> None:
    c.setStrokeColor(CUT)
    c.setLineWidth(CUT_WIDTH)
    c.setDash(3, 2)


def reset_dash(c: canvas.Canvas) -> None:
    c.setDash()


def draw_triangle(c: canvas.Canvas, x: float, y: float, size: float, color) -> None:
    p = c.beginPath()
    p.moveTo(x, y)
    p.lineTo(x + size, y)
    p.lineTo(x + size / 2, y + size * 0.86)
    p.close()
    c.setFillColor(color)
    c.drawPath(p, fill=1, stroke=0)


def draw_diamond(c: canvas.Canvas, x: float, y: float, size: float, color) -> None:
    p = c.beginPath()
    p.moveTo(x, y + size / 2)
    p.lineTo(x + size / 2, y + size)
    p.lineTo(x + size, y + size / 2)
    p.lineTo(x + size / 2, y)
    p.close()
    c.setFillColor(color)
    c.drawPath(p, fill=1, stroke=0)


def draw_leaf(c: canvas.Canvas, x: float, y: float, size: float, color, mirrored: bool) -> None:
    p = c.beginPath()
    p.moveTo(x + (size if mirrored else 0), y)
    if mirrored:
        p.curveTo(x + size * 0.9, y + size * 0.7, x + size * 0.4, y + size * 0.95, x, y + size)
        p.curveTo(x + size * 0.45, y + size * 0.4, x + size * 0.65, y + size * 0.15, x + size, y)
    else:
        p.curveTo(x + size * 0.1, y + size * 0.7, x + size * 0.6, y + size * 0.95, x + size, y + size)
        p.curveTo(x + size * 0.55, y + size * 0.4, x + size * 0.35, y + size * 0.15, x, y)
    p.close()
    c.setFillColor(color)
    c.drawPath(p, fill=1, stroke=0)


def draw_motif(c: canvas.Canvas, x: float, y: float, size: float, color, index: int) -> None:
    """One motif slot, drawn in the active design.

    Every design fills the same slots, so geometry, ink budget and page bounds
    are identical across designs and only the shape changes.
    """
    style = ACTIVE["motif"]
    if style == "geometric":
        if index % 2:
            draw_diamond(c, x, y, size, color)
        else:
            draw_triangle(c, x, y, size, color)
    elif style == "leaf":
        draw_leaf(c, x, y, size, color, mirrored=bool(index % 2))
    else:
        # Minimal carries a short rule instead of a shape. 1 pt clears the
        # 0.5 pt inkjet floor from PRODUCT.md section 5.
        c.setStrokeColor(color)
        c.setLineWidth(1)
        c.setDash()
        c.line(x, y + size / 2, x + size, y + size / 2)


def display_font_size_for_cap_height(height: float) -> float:
    face = pdfmetrics.getFont(DISPLAY).face
    cap_height = float(getattr(face, "capHeight", 700))
    return height * 1000 / cap_height


def draw_flag(
    c: canvas.Canvas,
    page_size,
    page_num: int,
    total_pages: int,
    mark: str,
    index: int,
    item_count: int,
    section_name: str = "BANNER",
) -> None:
    width, height = page_size
    flag_w = 127 * mm
    flag_h = 178 * mm
    side_h = 152 * mm
    notch_h = 26 * mm
    x = (width - flag_w) / 2
    y = (height - flag_h) / 2

    page_header(
        c,
        page_size,
        f"{section_name} - flag {index + 1} of {item_count} - cut the outline and punch both holes",
    )

    p = c.beginPath()
    p.moveTo(x, y + flag_h)
    p.lineTo(x + flag_w, y + flag_h)
    p.lineTo(x + flag_w, y + notch_h)
    p.lineTo(x + flag_w / 2, y)
    p.lineTo(x, y + notch_h)
    p.close()
    set_cut_style(c)
    c.drawPath(p, fill=0, stroke=1)
    reset_dash(c)

    hole_y = y + flag_h - 12 * mm
    for hole_x in (x + 14 * mm, x + flag_w - 14 * mm):
        set_cut_style(c)
        c.circle(hole_x, hole_y, 2.5 * mm, fill=0, stroke=1)
        reset_dash(c)

    # The cap height is exactly 90 mm; the slight upward shift is optical.
    if mark:
        font_size = display_font_size_for_cap_height(90 * mm)
        baseline = y + 95 * mm - 45 * mm
        if mark in ".,":
            font_size *= 0.68
            baseline = y + 91 * mm
        elif mark == "-":
            font_size *= 0.72
            baseline = y + 67 * mm
        elif mark == "'":
            font_size *= 0.72
            baseline = y + 50 * mm
        max_width = flag_w - 2 * (SAFE_INSET + 6 * mm)
        glyph_width = pdfmetrics.stringWidth(mark, DISPLAY, font_size)
        horizontal_scale = min(1.0, max_width / glyph_width)
        c.setFont(DISPLAY, font_size)
        c.setFillColor(palette()[index % 3])
        c.saveState()
        c.translate(x + flag_w / 2, 0)
        c.scale(horizontal_scale, 1)
        c.drawCentredString(0, baseline, mark)
        c.restoreState()

    motif_y = y + notch_h + SAFE_INSET + 5 * mm
    for col in range(5):
        motif_x = x + 22 * mm + col * 20 * mm
        color = palette()[(index + col + 1) % 3]
        draw_motif(c, motif_x, motif_y, 5 * mm, color, col)

    page_footer(c, page_size, page_num, total_pages, mark or "BLANK")
    c.showPage()


def polar(cx: float, cy: float, radius: float, degrees: float) -> tuple[float, float]:
    angle = math.radians(degrees)
    return cx + radius * math.cos(angle), cy + radius * math.sin(angle)


def draw_hat(
    c: canvas.Canvas, page_size, page_num: int, total_pages: int, copy_num: int
) -> None:
    width, height = page_size
    radius = 95 * mm
    # A 270-degree R95 sector cannot occur twice on either safe print area.
    # Each of the two required hats therefore gets its own sheet at true size.
    cx = width / 2 - 8.5 * mm
    cy = height / 2
    start_angle = -135
    extent = 270
    start = polar(cx, cy, radius, start_angle)
    end = polar(cx, cy, radius, start_angle + extent)

    vx = math.cos(math.radians(start_angle))
    vy = math.sin(math.radians(start_angle))
    nx, ny = vy, -vx
    tab_start = 12 * mm
    tab_end = 85 * mm
    tab_width = 15 * mm
    a1 = (cx + vx * tab_start, cy + vy * tab_start)
    a2 = (cx + vx * tab_end, cy + vy * tab_end)
    b1 = (a1[0] + nx * tab_width, a1[1] + ny * tab_width)
    b2 = (a2[0] + nx * tab_width, a2[1] + ny * tab_width)

    page_header(c, page_size, f"PARTY HAT {copy_num} OF 2 - cut, roll into a cone and glue the tab")

    p = c.beginPath()
    p.moveTo(cx, cy)
    p.lineTo(a1[0], a1[1])
    p.lineTo(b1[0], b1[1])
    p.lineTo(b2[0], b2[1])
    p.lineTo(start[0], start[1])
    p.arcTo(cx - radius, cy - radius, cx + radius, cy + radius, start_angle, extent)
    p.lineTo(cx, cy)
    p.close()
    set_cut_style(c)
    c.drawPath(p, fill=0, stroke=1)
    reset_dash(c)

    c.setStrokeColor(CORAL)
    c.setLineWidth(0.5)
    c.setDash(2, 2)
    c.line(a1[0], a1[1], a2[0], a2[1])
    reset_dash(c)
    c.setFillColor(CORAL)
    c.setFont(SERVICE, 8)
    c.saveState()
    c.translate((b1[0] + b2[0]) / 2, (b1[1] + b2[1]) / 2)
    c.rotate(start_angle + 180)
    c.drawCentredString(0, 3 * mm, "GLUE TAB")
    c.restoreState()

    # A polar grid repeats the flag's triangle/diamond rhythm around the cone.
    # It covers both radial edges, so the assembled hat has no blank side.
    motif_index = 0
    for ring, angles in (
        (31 * mm, (-105, -52.5, 0, 52.5, 105)),
        (57 * mm, (-115, -76.5, -38, 0, 38, 76.5, 115)),
        (80 * mm, (-115, -82, -49, -16, 16, 49, 82, 115)),
    ):
        for angle in angles:
            px, py = polar(cx, cy, ring, angle)
            color = palette()[(motif_index + copy_num) % 3]
            draw_motif(c, px - 2.5 * mm, py - 2.5 * mm, 5 * mm, color, motif_index)
            motif_index += 1

    page_footer(c, page_size, page_num, total_pages, f"HAT {copy_num}/2")
    c.showPage()


def draw_toppers(c: canvas.Canvas, page_size, page_num: int, total_pages: int) -> None:
    width, height = page_size
    diameter = 50.8 * mm
    gap = 8 * mm
    grid_w = 3 * diameter + 2 * gap
    grid_h = 4 * diameter + 3 * gap
    left = (width - grid_w) / 2
    bottom = (height - grid_h) / 2
    labels = ("YAY!", "HOORAY", "PARTY", "HAPPY")

    page_header(c, page_size, "CUPCAKE TOPPERS - 12 pieces - cut the circles and tape to picks")
    for row in range(4):
        for col in range(3):
            cx = left + diameter / 2 + col * (diameter + gap)
            cy = bottom + grid_h - diameter / 2 - row * (diameter + gap)
            set_cut_style(c)
            c.circle(cx, cy, diameter / 2, fill=0, stroke=1)
            reset_dash(c)
            c.setStrokeColor(palette()[(row + col) % 3])
            c.setLineWidth(1.2)
            c.circle(cx, cy, diameter / 2 - SAFE_INSET, fill=0, stroke=1)
            c.setFillColor(INK)
            c.setFont(DISPLAY, 16)
            c.drawCentredString(cx, cy - 5, labels[(row + col) % len(labels)])

    page_footer(c, page_size, page_num, total_pages, "TOPPERS 12")
    c.showPage()


def draw_sign(
    c: canvas.Canvas, page_size, page_num: int, total_pages: int, copy_num: int
) -> None:
    width, height = page_size
    sign_w = 178 * mm
    sign_h = 127 * mm
    x = (width - sign_w) / 2
    y = (height - sign_h) / 2
    messages = (("CAKE", "THIS WAY"), ("GIFTS", "& CARDS"))

    page_header(c, page_size, f"PARTY SIGN {copy_num} OF 2 - 5 x 7 in - cut and place in a frame")
    set_cut_style(c)
    c.rect(x, y, sign_w, sign_h, fill=0, stroke=1)
    reset_dash(c)

    inset = 8 * mm
    c.setStrokeColor(palette()[copy_num - 1])
    c.setLineWidth(2)
    c.rect(x + inset, y + inset, sign_w - 2 * inset, sign_h - 2 * inset, fill=0, stroke=1)
    c.setFillColor(INK)
    c.setFont(DISPLAY, 31)
    c.drawCentredString(width / 2, y + 72 * mm, messages[copy_num - 1][0])
    c.setFillColor(palette()[copy_num])
    c.setFont(DISPLAY, 25)
    c.drawCentredString(width / 2, y + 51 * mm, messages[copy_num - 1][1])
    for col in range(7):
        color = palette()[(copy_num + col) % 3]
        draw_motif(c, x + 25 * mm + col * 20 * mm, y + 23 * mm, 5 * mm, color, col)

    page_footer(c, page_size, page_num, total_pages, f"SIGN {copy_num}/2")
    c.showPage()


def draw_tags(c: canvas.Canvas, page_size, page_num: int, total_pages: int) -> None:
    width, height = page_size
    tag_w = 45 * mm
    tag_h = 90 * mm
    gap = 10 * mm
    # 2 x 3 does not fit either safe print area at the required dimensions.
    # The same six tags are arranged 3 x 2 without scaling.
    cols, rows = 3, 2
    grid_w = cols * tag_w + (cols - 1) * gap
    grid_h = rows * tag_h + (rows - 1) * gap
    left = (width - grid_w) / 2
    bottom = (height - grid_h) / 2

    page_header(c, page_size, "FAVOR TAGS - 6 pieces - cut, punch the marked hole and tie with string")
    for row in range(rows):
        for col in range(cols):
            x = left + col * (tag_w + gap)
            y = bottom + (rows - 1 - row) * (tag_h + gap)
            set_cut_style(c)
            c.roundRect(x, y, tag_w, tag_h, 4 * mm, fill=0, stroke=1)
            reset_dash(c)
            hole_x = x + tag_w / 2
            hole_y = y + tag_h - 8 * mm
            set_cut_style(c)
            c.circle(hole_x, hole_y, 2 * mm, fill=0, stroke=1)
            reset_dash(c)
            c.setStrokeColor(palette()[(row + col) % 3])
            c.setLineWidth(1.2)
            c.roundRect(
                x + SAFE_INSET,
                y + SAFE_INSET,
                tag_w - 2 * SAFE_INSET,
                tag_h - 19 * mm,
                2 * mm,
                fill=0,
                stroke=1,
            )
            c.setFillColor(INK)
            c.setFont(DISPLAY, 14)
            c.drawCentredString(x + tag_w / 2, y + 45 * mm, "THANK YOU")
            c.setFillColor(CORAL)
            c.setFont(SERVICE, 8)
            c.drawCentredString(x + tag_w / 2, y + 35 * mm, "for celebrating")

    page_footer(c, page_size, page_num, total_pages, "TAGS 6")
    c.showPage()


def new_canvas(path: Path, page_size, paper_name: str, product: str) -> canvas.Canvas:
    path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(
        str(path),
        pagesize=page_size,
        pageCompression=1,
        pdfVersion=(1, 4),
        enforceColorSpace="RGB",
        initialFontName=SERVICE,
        initialFontSize=8,
        initialLeading=10,
    )
    set_metadata(c, paper_name, product)
    return c


def build(path: Path, page_size, paper_name: str) -> None:
    """The complete kit: banner plus every other piece."""
    c = new_canvas(path, page_size, paper_name, "kit")

    page_num = 1
    for index, letter in enumerate(FLAGS):
        draw_flag(
            c,
            page_size,
            page_num,
            KIT_PAGES,
            letter,
            index,
            len(FLAGS),
        )
        page_num += 1
    for copy_num in (1, 2):
        draw_hat(c, page_size, page_num, KIT_PAGES, copy_num)
        page_num += 1
    draw_toppers(c, page_size, page_num, KIT_PAGES)
    page_num += 1
    for copy_num in (1, 2):
        draw_sign(c, page_size, page_num, KIT_PAGES, copy_num)
        page_num += 1
    draw_tags(c, page_size, page_num, KIT_PAGES)
    page_num += 1
    assert page_num - 1 == KIT_PAGES
    c.save()


def build_banner(path: Path, page_size, paper_name: str) -> None:
    """The banner on its own: thirteen flags, nothing else.

    This is what the Download PDF button on /birthday/banners/ must serve.
    A visitor who arrived on `free printable happy birthday banner` and got the
    19-page kit instead was defect G.
    """
    c = new_canvas(path, page_size, paper_name, "banner")
    total = len(FLAGS)
    for index, letter in enumerate(FLAGS):
        draw_flag(c, page_size, index + 1, total, letter, index, total)
    c.save()


def build_hat(path: Path, page_size, paper_name: str) -> None:
    """The hat template on its own: two sheets, one cone each.

    A 270-degree R95 sector does not fit twice on either paper, so the two hats
    a kit needs are two pages rather than one scaled-down sheet.
    """
    c = new_canvas(path, page_size, paper_name, "hat")
    for copy_num in (1, 2):
        draw_hat(c, page_size, copy_num, 2, copy_num)
    c.save()


def build_alphabet(path: Path, page_size, paper_name: str) -> None:
    c = new_canvas(path, page_size, paper_name, "alphabet")
    total = len(ALPHABET_MARKS)
    for index, mark in enumerate(ALPHABET_MARKS):
        draw_flag(
            c,
            page_size,
            index + 1,
            total,
            mark,
            index,
            total,
            section_name="BANNER ALPHABET",
        )
    c.save()


PAPERS = (
    ("a4", A4, "A4 210 x 297 mm"),
    ("letter", LETTER, "US Letter 8.5 x 11 in"),
)


def main() -> None:
    global ACTIVE
    register_fonts()
    written = []
    for design_key, design in DESIGNS.items():
        ACTIVE = design
        for suffix, page_size, paper_name in PAPERS:
            for product, builder in (
                (f"birthday-kit-{design_key}", build),
                (f"birthday-banner-{design_key}", build_banner),
                # Occasion-neutral artefacts keep the site-wide naming from
                # PRODUCT.md section 6, like banner-letters.
                (f"party-hat-{design_key}", build_hat),
                (f"banner-letters-{design_key}", build_alphabet),
            ):
                path = OUT / f"{product}-{suffix}.pdf"
                builder(path, page_size, paper_name)
                written.append(path)
    for path in written:
        print(path)


if __name__ == "__main__":
    main()
