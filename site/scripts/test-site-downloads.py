#!/usr/bin/env python3
"""Link-level checks between the built site and the files it offers.

Two failures this catches, both from DEFECTS.md:

G  a download button that serves the wrong product. The banner page must serve
   the banner, not the kit: the page count behind its Download PDF button has
   to equal the number of letters in the occasion phrase.
H  a file sitting in public/downloads that no page links to. Orphans get wired
   back onto a button by accident months later.

Run after `astro build`:  python3 scripts/test-site-downloads.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / "site" / "dist"
DOWNLOADS = ROOT / "site" / "public" / "downloads"

# built page path -> (button label fragment, expected page count)
PRODUCT_EXPECTATIONS = {
    "birthday/banners": ("Download PDF", len("HAPPYBIRTHDAY")),
    # Two cones, two sheets: an R95 sector does not fit twice on one page.
    "party-hats": ("Download PDF", 2),
}
LINK = re.compile(r'href="(/downloads/[^"]+)"')
BUTTON = re.compile(r'<a class="button[^"]*" href="(/downloads/[^"]+)"[^>]*>([^<]+)</a>')


def fail(message: str) -> None:
    print(f"FAIL {message}")
    sys.exit(1)


def main() -> None:
    if not DIST.exists():
        fail(f"{DIST} is missing, run astro build first")

    linked: set[str] = set()
    for html_file in sorted(DIST.rglob("index.html")):
        text = html_file.read_text()
        page = html_file.parent.relative_to(DIST).as_posix().strip("/")
        for href in LINK.findall(text):
            linked.add(href)
            if not (DOWNLOADS / Path(href).name).exists():
                fail(f"/{page} links to {href}, which does not exist")

        expectation = PRODUCT_EXPECTATIONS.get(page)
        if not expectation:
            continue
        label_fragment, expected_pages = expectation
        hits = {href for href, label in BUTTON.findall(text) if label_fragment in label}
        if not hits:
            fail(f"/{page} has no button labelled {label_fragment!r}")
        for href in sorted(hits):
            pages = len(PdfReader(DOWNLOADS / Path(href).name).pages)
            if pages != expected_pages:
                fail(
                    f"/{page}: {label_fragment!r} serves {href} with {pages} pages, "
                    f"expected {expected_pages}"
                )
            print(f"PASS /{page}: {label_fragment} -> {Path(href).name} ({pages} pages)")

    orphans = sorted(
        p.name for p in DOWNLOADS.iterdir() if p.is_file() and f"/downloads/{p.name}" not in linked
    )
    if orphans:
        fail("files in public/downloads that no page links to: " + ", ".join(orphans))
    print(f"PASS no orphans: all {len(linked)} download files are linked")


if __name__ == "__main__":
    main()
