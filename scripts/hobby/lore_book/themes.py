"""Theme helpers for explicit page CSS classes."""
from __future__ import annotations

import re


def css_id(value: str) -> str:
    ident = re.sub(r"[^A-Za-z0-9_-]", "-", str(value))
    if not ident or not ident[0].isalpha():
        ident = "t-" + ident
    return ident


def build_theme_classes(theme_ids: set[str]) -> str:
    """Generate CSS classes that apply accent colours to each page theme."""
    lines = ["    /* theme classes applied to each .book-page */"]
    for theme_id in sorted(theme_ids):
        lines.append(f"    .page-theme-{css_id(theme_id)} {{ }}")
    return "\n".join(lines)
