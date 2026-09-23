#!/usr/bin/env python3
"""Automated product checks for every generated birthday product PDF."""

from __future__ import annotations

import hashlib
import subprocess
import tempfile
from pathlib import Path

import pdfplumber
from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]
DESIGNS = ("botanical", "geometric", "minimal")
PAPERS = {"a4": (210.0, 297.0), "letter": (215.9, 279.4)}


def matrix(stem: str) -> dict[str, tuple[Path, tuple[float, float]]]:
    return {
        f"{design}-{paper}": (ROOT / f"output/pdf/{stem}-{design}-{paper}.pdf", size)
        for design in DESIGNS
        for paper, size in PAPERS.items()
    }


PDFS = matrix("birthday-kit")
BANNER_PDFS = matrix("birthday-banner")
HAT_PDFS = matrix("party-hat")
ALPHABET_PDFS = matrix("banner-letters")
FLAGS = list("HAPPYBIRTHDAY")
ALPHABET_MARKS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789&!?.,'-") + [""]
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

MM_PER_PT = 25.4 / 72
PT_PER_MM = 72 / 25.4
TOL_MM = 0.5
PAGE_MARGIN_MM = 15
KIT_PAGES = 19


def mm(value: float) -> float:
    return value * MM_PER_PT


def close(actual: float, expected: float, tolerance: float = TOL_MM) -> bool:
    return abs(actual - expected) <= tolerance


def font_descriptors(page):
    resources = page.get("/Resources") or {}
    fonts = resources.get("/Font") or {}
    for ref in fonts.values():
        font = ref.get_object()
        descriptor = font.get("/FontDescriptor")
        if descriptor:
            yield font, descriptor.get_object()
            continue
        for descendant_ref in font.get("/DescendantFonts") or []:
            descendant = descendant_ref.get_object()
            descriptor = descendant.get("/FontDescriptor")
            if descriptor:
                yield font, descriptor.get_object()


def assert_fonts(reader: PdfReader, path: Path, expected_subsets: int = 2) -> None:
    seen = set()
    for page in reader.pages:
        for font, descriptor in font_descriptors(page):
            base = str(font.get("/BaseFont", ""))
            seen.add(base)
            assert "Helvetica" not in base and "Arial" not in base and "Times" not in base, (
                path,
                base,
            )
            assert any(key in descriptor for key in ("/FontFile", "/FontFile2", "/FontFile3")), (
                path,
                base,
                "font is not embedded",
            )
            assert "+" in base, (path, base, "font is not subset")
    assert len(seen) == expected_subsets, (path, seen, "unexpected number of font subsets")


def assert_page_bounds(pdf: pdfplumber.PDF, path: Path) -> None:
    margin = PAGE_MARGIN_MM * PT_PER_MM
    tolerance = 0.8
    for page in pdf.pages:
        objects = page.chars + page.lines + page.curves + page.rects
        for obj in objects:
            assert obj["x0"] >= margin - tolerance, (path, page.page_number, "left", obj)
            assert obj["x1"] <= page.width - margin + tolerance, (
                path,
                page.page_number,
                "right",
                obj,
            )
            assert obj["top"] >= margin - tolerance, (path, page.page_number, "top", obj)
            assert obj["bottom"] <= page.height - margin + tolerance, (
                path,
                page.page_number,
                "bottom",
                obj,
            )
        visible_chars = [char for char in page.chars if not char["text"].isspace()]
        assert min(char["size"] for char in visible_chars) >= 7.99, (
            path,
            page.page_number,
            "text below 8 pt",
        )


def assert_flag_page(
    page: pdfplumber.page.Page, path: Path, index: int, check_display_size: bool
) -> None:
    expected_display_size = 90 * PT_PER_MM * 1000 / 688
    dashed = [curve for curve in page.curves if curve.get("dash", ([], 0))[0]]
    outline = max(dashed, key=lambda curve: curve["width"] * curve["height"])
    assert close(mm(outline["width"]), 127), (path, index + 1, mm(outline["width"]))
    assert close(mm(outline["height"]), 178), (path, index + 1, mm(outline["height"]))

    holes = sorted(
        [curve for curve in dashed if close(mm(curve["width"]), 5)],
        key=lambda curve: curve["x0"],
    )
    assert len(holes) == 2, (path, index + 1, "hole count")
    left_center = (holes[0]["x0"] + holes[0]["x1"]) / 2
    right_center = (holes[1]["x0"] + holes[1]["x1"]) / 2
    hole_top_center = (holes[0]["top"] + holes[0]["bottom"]) / 2
    assert close(mm(left_center - outline["x0"]), 14)
    assert close(mm(outline["x1"] - right_center), 14)
    assert close(mm(hole_top_center - outline["top"]), 12)

    if check_display_size:
        display_chars = [char for char in page.chars if char["size"] > 100]
        assert len(display_chars) == 1
        assert abs(display_chars[0]["size"] - expected_display_size) <= 0.2


def assert_flag_geometry(pdf: pdfplumber.PDF, path: Path) -> None:
    for index, page in enumerate(pdf.pages[:13]):
        assert_flag_page(page, path, index, check_display_size=True)


def assert_hat_pages(pdf: pdfplumber.PDF, path: Path, indices: tuple[int, ...]) -> None:
    """Two true-size hats, one per sheet because two cannot fit on either paper."""
    for index in indices:
        page = pdf.pages[index]
        text = page.extract_text() or ""
        rotated = [char for char in page.chars if abs(char["matrix"][1]) > 0.1]
        assert "PARTY HAT" in text
        assert "".join(char["text"] for char in rotated) == "GLUE TAB"
        assert all(char["matrix"][0] > 0 and char["matrix"][1] > 0 for char in rotated)
        assert any(curve.get("dash", ([], 0))[0] for curve in page.curves)


def assert_piece_geometry(pdf: pdfplumber.PDF, path: Path) -> None:
    assert_hat_pages(pdf, path, (13, 14))

    # Page 16: 12 toppers, diameter 50.8 mm, 3 x 4, 8 mm gaps.
    topper_page = pdf.pages[15]
    topper_text_lines = (topper_page.extract_text() or "").splitlines()
    assert not any(line.strip() == "8" for line in topper_text_lines)
    assert any("HOORAY" in line for line in topper_text_lines)
    topper_cuts = [
        curve
        for curve in topper_page.curves
        if curve.get("dash", ([], 0))[0] and close(mm(curve["width"]), 50.8)
    ]
    assert len(topper_cuts) == 12, (path, "topper count", len(topper_cuts))
    xs = sorted({round(curve["x0"], 2) for curve in topper_cuts})
    ys = sorted({round(curve["top"], 2) for curve in topper_cuts})
    assert len(xs) == 3 and len(ys) == 4
    assert close(mm(xs[1] - xs[0] - 50.8 * PT_PER_MM), 8)
    assert close(mm(ys[1] - ys[0] - 50.8 * PT_PER_MM), 8)

    # Pages 17-18: two 127 x 178 mm signs, one per sheet at real size.
    for page in pdf.pages[16:18]:
        cut_rects = [rect for rect in page.rects if rect.get("dash", ([], 0))[0]]
        assert len(cut_rects) == 1
        assert close(mm(cut_rects[0]["width"]), 178)
        assert close(mm(cut_rects[0]["height"]), 127)

    # Page 19: six 45 x 90 mm tags and six 4 mm holes.
    tag_page = pdf.pages[18]
    dashed = [curve for curve in tag_page.curves if curve.get("dash", ([], 0))[0]]
    tags = [curve for curve in dashed if close(mm(curve["width"]), 45)]
    holes = [curve for curve in dashed if close(mm(curve["width"]), 4)]
    assert len(tags) == 6, (path, "tag count", len(tags))
    assert len(holes) == 6, (path, "tag hole count", len(holes))


def ink_coverage(path: Path) -> list[float]:
    with tempfile.TemporaryDirectory(prefix="ppk-ink-") as temp:
        prefix = Path(temp) / "page"
        subprocess.run(
            [str(PDFTOPPM), "-png", "-r", "72", str(path), str(prefix)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        coverage = []
        for image_path in sorted(Path(temp).glob("page-*.png")):
            image = Image.open(image_path).convert("RGB")
            colored = sum(
                1
                for red, green, blue in image.get_flattened_data()
                if min(red, green, blue) < 245
            )
            coverage.append(colored / (image.width * image.height))
        return coverage


def assert_page_sizes(reader: PdfReader, path: Path, expected_size_mm) -> None:
    width_mm = mm(float(reader.pages[0].mediabox.width))
    height_mm = mm(float(reader.pages[0].mediabox.height))
    assert close(width_mm, expected_size_mm[0]) and close(height_mm, expected_size_mm[1])
    for page in reader.pages:
        assert close(mm(float(page.mediabox.width)), expected_size_mm[0])
        assert close(mm(float(page.mediabox.height)), expected_size_mm[1])


def test_kit_pdf(path: Path, expected_size_mm: tuple[float, float]) -> None:
    reader = PdfReader(path)
    assert len(reader.pages) == KIT_PAGES, (path, len(reader.pages))
    assert_page_sizes(reader, path, expected_size_mm)

    metadata = reader.metadata
    assert "Free Printable Birthday Party Kit" in metadata.title
    assert metadata.creator == "partyprintkit.com"
    assert "Actual size" in metadata.subject
    assert_fonts(reader, path)

    with pdfplumber.open(path) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        assert "THIS PAGE DOES NOT NEED TO BE PRINTED" not in text
        assert text.count("partyprintkit.com") == KIT_PAGES
        assert text.count("print at 100% (Actual size)") == KIT_PAGES
        assert_page_bounds(pdf, path)
        assert_flag_geometry(pdf, path)
        assert_piece_geometry(pdf, path)

    coverage = ink_coverage(path)
    assert len(coverage) == KIT_PAGES
    assert max(coverage) <= 0.40, (path, max(coverage))
    print(f"PASS {path.name}: {KIT_PAGES} pages, max ink coverage {max(coverage):.1%}")


def test_banner_pdf(path: Path, expected_size_mm: tuple[float, float]) -> None:
    """The banner product is the banner and nothing else.

    Defect G was the Download PDF button on /birthday/banners/ serving the
    19-page kit. The page count here is the same number the site-level test
    asserts behind that button.
    """
    reader = PdfReader(path)
    assert len(reader.pages) == len(FLAGS), (path, len(reader.pages))
    assert_page_sizes(reader, path, expected_size_mm)
    assert "Free Printable Happy Birthday Banner" in reader.metadata.title
    assert reader.metadata.creator == "partyprintkit.com"
    assert "Actual size" in reader.metadata.subject
    assert_fonts(reader, path)

    with pdfplumber.open(path) as pdf:
        assert_page_bounds(pdf, path)
        assert_flag_geometry(pdf, path)
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        for piece in ("PARTY HAT", "CUPCAKE TOPPERS", "PARTY SIGN", "FAVOR TAGS"):
            assert piece not in text, (path, f"{piece} must not be in the banner-only PDF")
        assert text.count("partyprintkit.com") == len(FLAGS)
        for index, (page, letter) in enumerate(zip(pdf.pages, FLAGS)):
            assert letter in (page.extract_text() or ""), (path, index + 1, letter)

    coverage = ink_coverage(path)
    assert len(coverage) == len(FLAGS)
    assert max(coverage) <= 0.40, (path, max(coverage))
    print(f"PASS {path.name}: {len(FLAGS)} flags, banner only, max ink {max(coverage):.1%}")


def test_hat_pdf(path: Path, expected_size_mm: tuple[float, float]) -> None:
    """The hat template on its own: two cones, nothing else.

    Only the service font appears here: the sheet carries no display type, so
    one embedded subset is correct rather than two.
    """
    reader = PdfReader(path)
    assert len(reader.pages) == 2, (path, len(reader.pages))
    assert_page_sizes(reader, path, expected_size_mm)
    assert "Free Printable Party Hat Template" in reader.metadata.title
    assert reader.metadata.creator == "partyprintkit.com"
    assert "Actual size" in reader.metadata.subject
    assert_fonts(reader, path, expected_subsets=1)

    with pdfplumber.open(path) as pdf:
        assert_page_bounds(pdf, path)
        assert_hat_pages(pdf, path, (0, 1))
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        for piece in ("BANNER", "CUPCAKE TOPPERS", "PARTY SIGN", "FAVOR TAGS"):
            assert piece not in text, (path, f"{piece} must not be in the hat-only PDF")
        assert text.count("partyprintkit.com") == 2

    coverage = ink_coverage(path)
    assert len(coverage) == 2
    assert max(coverage) <= 0.40, (path, max(coverage))
    print(f"PASS {path.name}: 2 cones, hat only, max ink {max(coverage):.1%}")


def test_alphabet_pdf(path: Path, expected_size_mm: tuple[float, float]) -> None:
    reader = PdfReader(path)
    total = len(ALPHABET_MARKS)
    assert len(reader.pages) == total, (path, len(reader.pages))
    assert_page_sizes(reader, path, expected_size_mm)
    assert "Printable Banner Letters" in reader.metadata.title
    assert reader.metadata.creator == "partyprintkit.com"
    assert_fonts(reader, path)

    with pdfplumber.open(path) as pdf:
        assert_page_bounds(pdf, path)
        for index, (page, mark) in enumerate(zip(pdf.pages, ALPHABET_MARKS)):
            assert_flag_page(
                page,
                path,
                index,
                check_display_size=mark.isalnum(),
            )
            text = page.extract_text() or ""
            assert "partyprintkit.com" in text
            assert "print at 100% (Actual size)" in text
            if mark:
                assert mark in text, (path, index + 1, mark)
            else:
                assert "BLANK" in text

    available = set(ALPHABET_MARKS)
    for fixture in (
        "HAPPY BIRTHDAY",
        "HAPPY 100TH BIRTHDAY",
        "IT'S A BOY",
        "CONGRATS GRAD",
        "X",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMN",
    ):
        assert len(fixture) <= 40
        assert all(char == " " or char in available for char in fixture)

    coverage = ink_coverage(path)
    assert len(coverage) == total
    assert max(coverage) <= 0.40, (path, max(coverage))
    print(f"PASS {path.name}: {total} flags, complete alphabet and symbols")


def assert_unique_public_assets() -> None:
    files = sorted((ROOT / "site/public/downloads").glob("*")) + sorted(
        (ROOT / "site/public/social").glob("*")
    )
    by_hash: dict[str, list[Path]] = {}
    for path in files:
        if path.is_file():
            digest = hashlib.md5(path.read_bytes()).hexdigest()
            by_hash.setdefault(digest, []).append(path)
    duplicates = [paths for paths in by_hash.values() if len(paths) > 1]
    assert not duplicates, duplicates
    print(f"PASS public asset uniqueness: {len(files)} distinct files")


def main() -> None:
    for path, expected_size in PDFS.values():
        test_kit_pdf(path, expected_size)
    for path, expected_size in BANNER_PDFS.values():
        test_banner_pdf(path, expected_size)
    for path, expected_size in HAT_PDFS.values():
        test_hat_pdf(path, expected_size)
    for path, expected_size in ALPHABET_PDFS.values():
        test_alphabet_pdf(path, expected_size)

    all_pdfs = [
        path
        for path, _ in (
            *PDFS.values(),
            *BANNER_PDFS.values(),
            *HAT_PDFS.values(),
            *ALPHABET_PDFS.values(),
        )
    ]
    hashes = {hashlib.md5(path.read_bytes()).hexdigest() for path in all_pdfs}
    assert len(hashes) == len(all_pdfs), "Every PDF must be a unique file"
    assert_unique_public_assets()
    print("PASS all product PDF checks")


if __name__ == "__main__":
    main()
