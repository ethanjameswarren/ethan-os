"""Preflight validation for print-ready lore books."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .publication import Book, TrimConfig, png_dimensions


def _ratio_matches(trim: TrimConfig, assets_dir: Path, img_path: str | None, tolerance: float = 0.03) -> tuple[bool, str | None]:
    if not img_path:
        return True, None
    path = assets_dir / Path(img_path).name
    if not path.exists():
        return False, f"background image not found: {img_path}"
    dims = png_dimensions(path)
    if not dims:
        return True, None  # cannot validate non-PNG assets here
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

    # Validate theme background images.
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
