"""Playwright PDF renderer for explicit fixed-page lore books.

Paged.js is no longer used because each `.book-page` is an explicit physical 6in x 9in element.
Playwright/Chromium directly prints the composed pages to a PDF with the exact trim size.
"""
from __future__ import annotations

from pathlib import Path

import pymupdf as fitz
from playwright.sync_api import sync_playwright


def render_pdf(html_path: Path, pdf_path: Path, timeout: int = 120) -> None:
    """Render composed HTML to a 6in x 9in PDF."""
    html_uri = html_path.resolve().as_uri()
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(html_uri, wait_until="networkidle", timeout=timeout * 1000)
        page.pdf(
            path=str(pdf_path),
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            print_background=True,
            prefer_css_page_size=True,
        )
        browser.close()
    print(f"PDF rendered: {pdf_path}")


def render_pdf_pages_to_png(pdf_path: Path, png_dir: Path, dpi: int = 150) -> list[Path]:
    """Render every page of a PDF to a PNG for inspection."""
    png_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    with fitz.open(str(pdf_path)) as doc:
        for i, page in enumerate(doc):
            mat = fitz.Matrix(dpi / 72.0, dpi / 72.0)
            pix = page.get_pixmap(matrix=mat)
            out = png_dir / f"page-{i + 1:03d}.png"
            pix.save(str(out))
            paths.append(out)
    print(f"Rendered {len(paths)} PNGs to {png_dir}")
    return paths
