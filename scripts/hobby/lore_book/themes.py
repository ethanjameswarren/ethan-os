"""Theme resolution and named-page CSS for the lore book."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .publication import TrimConfig


def css_id(value: str) -> str:
    ident = re.sub(r"[^A-Za-z0-9_-]", "-", str(value))
    if not ident or not ident[0].isalpha():
        ident = "t-" + ident
    return ident


def _page_rule(theme_id: str, bg_url: str | None, config: TrimConfig) -> str:
    margin = " ".join(f"{m}in" for m in config.margins)
    size = f"{config.width}in {config.height}in"
    bg = f"url({bg_url})" if bg_url else "none"
    return (
        f"    @page {css_id(theme_id)} {{\n"
        f"      size: {size};\n"
        f"      margin: {margin};\n"
        f"      background-color: var(--bg);\n"
        f"      background-image: {bg};\n"
        "      background-size: cover;\n"
        "      background-repeat: no-repeat;\n"
        "      background-position: center;\n"
        "      @bottom-center {\n"
        "        content: counter(page);\n"
        "        font-size: 7pt;\n"
        "        color: var(--muted);\n"
        "      }\n"
        "    }"
    )


def build_page_rules(theme_ids: set[str], theme_bgs: dict[str, str | None], config: TrimConfig) -> str:
    rules = []
    for theme_id in sorted(theme_ids):
        rules.append(_page_rule(theme_id, theme_bgs.get(theme_id), config))
    return "\n".join(rules)


def build_theme_classes(theme_ids: set[str]) -> str:
    lines = ["    /* named page classes — Paged.js discovers these from the stylesheet */"]
    for theme_id in sorted(theme_ids):
        lines.append(f"    .page-theme-{css_id(theme_id)} {{ page: {css_id(theme_id)}; }}")
    return "\n".join(lines)
