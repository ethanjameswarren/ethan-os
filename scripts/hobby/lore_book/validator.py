"""Preflight and postflight validation for print-ready lore books."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from pypdf import PdfReader

from .publication import Book, TrimConfig, png_dimensions


def _ratio_matches(trim: TrimConfig, assets_dir: Path, img_path: str | None, tolerance: float = 0.03) -> tuple[bool, str | None]:
    if not img_path:
        return True, None
    path = assets_dir / Path(img_path).name
    if not path.exists():
        return False, f"background image not found: {img_path}"
    dims = png_dimensions(path)
    if not dims:
        return True, None
    img_w, img_h = dims
    if img_h == 0:
        return False, f"invalid image dimensions: {img_w}x{img_h}"
    trim_ratio = trim.width / trim.height
    img_ratio = img_w / img_h
    if abs(img_ratio - trim_ratio) > tolerance:
        return False, (
            f"background aspect ratio {img_w}/{img_h}={img_ratio:.3f} "
            f"does not match trim {trim.width}/{trim.height}={trim_ratio:.3f}"
        )
    return True, None


def validate(book: Book) -> list[str]:
    """Run preflight checks and return a list of warning/error messages."""
    errors: list[str] = []

    for theme_id, bg_url in book.theme_backgrounds.items():
        ok, msg = _ratio_matches(book.config, book.assets_dir, bg_url)
        if not ok:
            errors.append(f"Theme '{theme_id}': {msg}")

    for ch in book.chapters:
        if ch.background_url:
            ok, msg = _ratio_matches(book.config, book.assets_dir, ch.background_url)
            if not ok:
                errors.append(f"Section {ch.number} background: {msg}")
        for media in ch.presentation_media + ch.other_media:
            fp = media.get("file_path", "")
            if not (book.project_dir / fp).exists():
                errors.append(f"Section {ch.number} missing asset: {fp}")

    return errors


def _pdf_dimensions_inches(pdf_path: Path) -> list[tuple[float, float]]:
    reader = PdfReader(str(pdf_path))
    dims = []
    for pg in reader.pages:
        w = float(pg.mediabox.width)
        h = float(pg.mediabox.height)
        dims.append((w / 72.0, h / 72.0))
    return dims


def validate_output(html_path: Path, pdf_path: Path, expected_size: tuple[float, float] = (6.0, 9.0)) -> dict[str, Any]:
    """Browser- and PDF-based postflight validation."""
    from playwright.sync_api import sync_playwright

    results: dict[str, Any] = {
        "html_page_count": 0,
        "pdf_page_count": 0,
        "overflows": [],
        "image_overruns": [],
        "missing_backgrounds": [],
        "invalid_templates": [],
        "pdf_dimensions": [],
        "size_ok": False,
        "page_count_match": False,
    }

    # HTML / browser checks.
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(html_path.resolve().as_uri(), wait_until="networkidle", timeout=120000)
        data = page.evaluate(r"""() => {
            const pages = Array.from(document.querySelectorAll('.book-page'));
            const overflows = [];
            const imageOverruns = [];
            const missingBg = [];
            const invalidTemplates = [];
            pages.forEach((pg, idx) => {
                const pageNum = pg.id ? pg.id.replace('page-', '') : String(idx + 1);
                const bg = pg.querySelector('.page-background');
                if (!bg) missingBg.push({ page: pageNum, reason: 'no .page-background' });
                const safe = pg.querySelector('.page-safe-area');
                if (safe && safe.scrollHeight > safe.clientHeight + 1) {
                    overflows.push({ page: pageNum, scrollHeight: safe.scrollHeight, maxHeight: safe.clientHeight });
                }
                const textRegion = pg.querySelector('.region-text');
                if (textRegion && textRegion.scrollHeight > textRegion.clientHeight + 1) {
                    overflows.push({ page: pageNum, region: 'text', scrollHeight: textRegion.scrollHeight, maxHeight: textRegion.clientHeight });
                }
                const artRegion = pg.querySelector('.region-art');
                if (artRegion && artRegion.scrollHeight > artRegion.clientHeight + 1) {
                    overflows.push({ page: pageNum, region: 'art', scrollHeight: artRegion.scrollHeight, maxHeight: artRegion.clientHeight });
                }
                const artImgs = pg.querySelectorAll('.region-art img');
                artImgs.forEach(img => {
                    const imgRect = img.getBoundingClientRect();
                    const artRect = artRegion.getBoundingClientRect();
                    if (imgRect.bottom > artRect.bottom + 1 || imgRect.right > artRect.right + 1 || imgRect.left < artRect.left - 1 || imgRect.top < artRect.top - 1) {
                        imageOverruns.push({ page: pageNum, imgSrc: img.src });
                    }
                });
                const classes = pg.className.split(/\s+/);
                const templateClass = classes.find(c => c.startsWith('template-'));
                if (!templateClass) {
                    invalidTemplates.push({ page: pageNum, reason: 'no template class' });
                }
            });
            return {
                htmlPageCount: pages.length,
                overflows,
                imageOverruns,
                missingBg,
                invalidTemplates,
            };
        }""")
        browser.close()

    results["html_page_count"] = int(data.get("htmlPageCount", 0))
    results["overflows"] = data.get("overflows", [])
    results["image_overruns"] = data.get("imageOverruns", [])
    results["missing_backgrounds"] = data.get("missingBg", [])
    results["invalid_templates"] = data.get("invalidTemplates", [])

    # PDF checks.
    if pdf_path.exists():
        results["pdf_dimensions"] = _pdf_dimensions_inches(pdf_path)
        reader = PdfReader(str(pdf_path))
        results["pdf_page_count"] = len(reader.pages)
        results["page_count_match"] = results["html_page_count"] == results["pdf_page_count"]
        width, height = expected_size
        tol = 0.02
        results["size_ok"] = all(
            abs(w - width) <= tol and abs(h - height) <= tol
            for w, h in results["pdf_dimensions"]
        )

    return results
