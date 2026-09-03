"""HTML assembly for the lore book."""
from __future__ import annotations

import html
import re
from pathlib import Path
from typing import Any

from .css import base_css
from .publication import Book, Chapter
from .themes import build_page_rules, build_theme_classes, css_id


def _h(value: Any) -> str:
    if value is None:
        return ""
    return html.escape(str(value))


def _para(text: str) -> str:
    out = []
    for line in text.strip().splitlines():
        stripped = line.strip()
        if stripped:
            out.append(f"<p>{_h(stripped)}</p>")
    return "\n".join(out)


def _pull_quote(lore: dict[str, Any]) -> str | None:
    content = lore.get("content", "")
    if not content:
        return None
    quoted = re.search(r'"([^"]{15,200})"', content)
    if quoted:
        text = f"\"{quoted.group(1)}\""
    else:
        quoted = re.search(r"'([^']{15,200})'", content)
        if quoted:
            text = f"'{quoted.group(1)}'"
    if not quoted:
        return None
    return f'<blockquote class="pull-quote"><p>{_h(text)}</p><span class="source">&mdash; {_h(lore.get("id", ""))}</span></blockquote>'


def _dossier_html(media: dict[str, Any]) -> str:
    rows = []
    for label, key in [
        ("Subject", "subject"),
        ("Type", "unit_type"),
        ("Faction", "faction"),
        ("Energy", "energy_color"),
        ("Canon", "canon_status"),
        ("Status", "status"),
    ]:
        value = media.get(key)
        if value:
            rows.append(f"<dt>{_h(label)}</dt><dd>{_h(value)}</dd>")
    if not rows:
        return ""
    return '<dl class="dossier">' + "".join(rows) + "</dl>"


def _media_html(src: str, media: dict[str, Any]) -> str:
    title = media.get("title", "")
    caption = media.get("caption", "") or media.get("subject", "")
    provenance = media.get("rights_or_provenance") or f"Source: {media.get('id', '')}"
    if media.get("lore_book_presentation"):
        size = media.get("lore_book_size", "standard")
        layout = media.get("lore_book_layout", "floating-bottom-right")
        if layout == "editorial-profile":
            figure_class = f"illustration hero hero-{_h(size)}"
        else:
            figure_class = f"illustration illustration-size-{_h(size)} illustration-layout-{_h(layout)}"
    else:
        figure_class = "media-asset"
    return (
        f'<figure class="{_h(figure_class)}">'
        f'<img src="{_h(src)}" alt="{_h(title)}" />'
        f'<figcaption>{_h(caption)}</figcaption>'
        f'<div class="provenance">{_h(provenance)}</div>'
        f'</figure>'
    )


def _render_visual_gaps(gaps: list[dict[str, Any]]) -> str:
    if not gaps:
        return '<p class="tbd">No visual gaps recorded.</p>'
    rows = []
    for gap in gaps:
        priority = gap.get("priority", "optional")
        rows.append(
            f'<tr><td class="priority-{_h(priority)}">{_h(priority.upper())}</td>'
            f'<td>{_h(gap.get("description", ""))}</td>'
            f'<td>{_h(gap.get("media_type", ""))}</td>'
            f'<td>{_h(gap.get("section_id", ""))}</td></tr>'
        )
    return (
        '<table class="visual-gaps">'
        '<thead><tr><th>Priority</th><th>Opportunity</th><th>Type</th><th>Section</th></tr></thead>'
        '<tbody>' + "".join(rows) + '</tbody></table>'
    )


def _build_cover(book: Book, default_theme: str) -> str:
    parts = [f'<section class="cover page-theme-{css_id(default_theme)}">']
    parts.append(f'<div class="edition">Edition {book.edition_year}</div>')
    parts.append(f'<h1>{_h(book.title)}</h1>')
    if book.heraldry_src:
        parts.append(f'<div class="cover-heraldry"><img class="dynasty-logo" src="{_h(book.heraldry_src)}" alt="Dynasty heraldry" /></div>')
    if book.subtitle:
        parts.append(f'<div class="subtitle">{_h(book.subtitle)}</div>')
    parts.append(f'<div class="status">Status: {_h(book.status)} &nbsp;|&nbsp; Generated: {_h(book.generated_date)}</div>')
    parts.append('</section>')
    return "\n".join(parts)


def _build_title_page(book: Book, default_theme: str) -> str:
    parts = [f'<section class="title-page page-theme-{css_id(default_theme)}">']
    parts.append(f'<h1>{_h(book.title)}</h1>')
    if book.subtitle:
        parts.append(f'<div class="subtitle">{_h(book.subtitle)}</div>')
    parts.append(f'<div class="edition">Edition {book.edition_year}</div>')
    parts.append(f'<div class="status">Status: {_h(book.status)} &nbsp;|&nbsp; Generated: {_h(book.generated_date)}</div>')
    if book.heraldry_src:
        parts.append(f'<div class="cover-heraldry"><img class="dynasty-logo" src="{_h(book.heraldry_src)}" alt="Dynasty heraldry" /></div>')
    parts.append('</section>')
    return "\n".join(parts)


def _build_toc(book: Book, default_theme: str) -> str:
    parts = [f'<section class="toc page-theme-{css_id(default_theme)}">']
    parts.append('<h2>Contents</h2>')
    parts.append('<ul>')
    for ch in book.chapters:
        parts.append(
            f'<li><span>{_h(ch.number)}. {_h(ch.title)}</span> <span class="status">{_h(ch.status_note)}</span></li>'
        )
    parts.append('</ul>')
    parts.append('</section>')
    return "\n".join(parts)


def _build_chapter(ch: Chapter, page_theme: str) -> str:
    classes = ["lore-section", f"page-theme-{css_id(page_theme)}", f"theme-{css_id(ch.theme)}", f"layout-{css_id(ch.layout)}"]
    if ch.presentation_media:
        classes.append("editorial-profile")
    class_attr = " ".join(classes)

    parts = [f'<section class="{_h(class_attr)}">']
    hero = ""
    for media in ch.presentation_media:
        src = f"assets/{Path(media.get('file_path', '')).name}"
        if src == "assets/":
            continue
        hero = _media_html(src, media)
        break

    is_profile = ch.layout == "editorial-profile" and ch.presentation_media
    if ch.layout == "full-art" and ch.presentation_media:
        media = ch.presentation_media[0]
        src = f"assets/{Path(media.get('file_path', '')).name}"
        parts.append(f'<div class="full-art"><img src="{_h(src)}" alt="{_h(media.get("title", ""))}" /></div>')
        parts.append('</section>')
        return "\n".join(parts)

    if ch.layout == "chapter-opener" and ch.presentation_media:
        media = ch.presentation_media[0]
        src = f"assets/{Path(media.get('file_path', '')).name}"
        parts.append(f'<div class="opener-art"><img src="{_h(src)}" alt="{_h(media.get("title", ""))}" /></div>')

    parts.append(f'<h2>{_h(ch.number)}. {_h(ch.title)}</h2>')
    parts.append(f'<div class="status">{_h(ch.status_note)}</div>')

    if is_profile:
        media = ch.presentation_media[0]
        subtitle = media.get("subject") or media.get("unit_type")
        if subtitle:
            parts.append(f'<div class="profile-subtitle">{_h(subtitle)}</div>')

    if ch.lore_entries:
        for i, lore in enumerate(ch.lore_entries):
            parts.append(f'<h3>{_h(lore.get("title", ""))}</h3>')
            if i == 0 and is_profile:
                dossier = _dossier_html(ch.presentation_media[0])
                if dossier:
                    parts.append(dossier)
                quote = _pull_quote(lore)
                if quote:
                    parts.append(quote)
                if hero:
                    parts.append(hero)
                    hero = ""
            content = lore.get("content", "")
            if content:
                parts.append(_para(content))
            else:
                parts.append('<p class="tbd">Intentionally unresolved — TBD.</p>')
            parts.append(f'<div class="provenance">Source: {_h(lore.get("id", ""))}</div>')
    else:
        if is_profile:
            dossier = _dossier_html(ch.presentation_media[0]) if ch.presentation_media else ""
            if dossier:
                parts.append(dossier)
            if hero:
                parts.append(hero)
                hero = ""
        parts.append('<p class="tbd">Intentionally unresolved — TBD.</p>')

    if hero:
        parts.append(hero)

    if ch.other_media:
        parts.append('<h3>Visual reference</h3>')
        for media in ch.other_media:
            src = f"assets/{Path(media.get('file_path', '')).name}"
            if src == "assets/":
                continue
            parts.append(_media_html(src, media))

    parts.append('</section>')
    return "\n".join(parts)


def _build_visual_gaps(book: Book, default_theme: str) -> str:
    parts = [f'<section class="lore-section page-theme-{css_id(default_theme)}">']
    parts.append('<h2>Visual Opportunities</h2>')
    parts.append(_render_visual_gaps(book.visual_gaps))
    parts.append('</section>')
    return "\n".join(parts)


def _build_appendix(book: Book, default_theme: str, unassigned_lore: list[dict[str, Any]] | None = None) -> str:
    if not unassigned_lore:
        return ""
    parts = [f'<section class="lore-section page-theme-{css_id(default_theme)}">']
    parts.append('<h2>Appendix: Other Canonical Notes</h2>')
    for lore in unassigned_lore:
        parts.append(f'<h3>{_h(lore.get("title", ""))}</h3>')
        content = lore.get("content", "")
        if content:
            parts.append(_para(content))
        else:
            parts.append('<p class="tbd">Intentionally unresolved — TBD.</p>')
        parts.append(f'<div class="provenance">Source: {_h(lore.get("id", ""))}</div>')
    parts.append('</section>')
    return "\n".join(parts)


def render_html(book: Book) -> tuple[str, list[str]]:
    default_page_theme = book.default_theme
    # map each chapter to a named page theme; if a record overrides the theme
    # background, give it a unique page theme so @page rules remain canonical.
    page_theme_bgs: dict[str, str | None] = {default_page_theme: book.theme_backgrounds.get(default_page_theme)}
    chapter_page_theme: dict[str, str] = {}
    for ch in book.chapters:
        expected_bg = book.theme_backgrounds.get(ch.theme)
        if ch.background_url == expected_bg:
            page_theme = ch.theme
        else:
            page_theme = f"{ch.theme}-{ch.number}"
        chapter_page_theme[ch.number] = page_theme
        page_theme_bgs[page_theme] = ch.background_url

    page_theme_ids = set(page_theme_bgs.keys())
    page_rules = build_page_rules(page_theme_ids, page_theme_bgs, book.config)
    theme_classes = build_theme_classes(page_theme_ids)
    css = base_css().replace("__PAGE_RULES__", page_rules).replace("__THEME_CLASSES__", theme_classes)

    warnings: list[str] = []

    html_parts = [
        "<!DOCTYPE html>",
        '<html lang="en"><head>',
        '<meta charset="utf-8">',
        f'<title>{_h(book.title)}</title>',
        '<style>',
        css,
        '</style>',
        '</head><body>',
    ]

    order = book.front_matter or ["cover", "title", "toc", "body", "visual_gaps", "appendix"]
    for item in order:
        if item == "cover":
            html_parts.append(_build_cover(book, default_page_theme))
        elif item == "title":
            html_parts.append(_build_title_page(book, default_page_theme))
        elif item == "toc":
            html_parts.append(_build_toc(book, default_page_theme))
        elif item == "body":
            for ch in book.chapters:
                html_parts.append(_build_chapter(ch, chapter_page_theme[ch.number]))
        elif item == "visual_gaps":
            html_parts.append(_build_visual_gaps(book, default_page_theme))
        elif item == "appendix":
            html_parts.append(_build_appendix(book, default_page_theme))
        else:
            warnings.append(f"Unknown front_matter_order item: {item}")

    html_parts.append("</body></html>")
    return "\n".join(html_parts), warnings
