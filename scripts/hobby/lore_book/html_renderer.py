"""HTML assembly for explicit fixed-page lore books."""
from __future__ import annotations

import html
import re
from pathlib import Path
from typing import Any

from .composer import ContentBlock, Page, SectionSpec, compose
from .css import base_css
from .publication import Book, Chapter
from .themes import build_theme_classes, css_id


def _h(value: Any) -> str:
    if value is None:
        return ""
    return html.escape(str(value))


def _para(text: str) -> list[ContentBlock]:
    blocks: list[ContentBlock] = []
    for line in text.strip().splitlines():
        stripped = line.strip()
        if stripped:
            blocks.append(ContentBlock(html=f"<p>{_h(stripped)}</p>", is_splittable=True))
    return blocks


def _pull_quote(lore: dict[str, Any]) -> ContentBlock | None:
    content = lore.get("content", "")
    if not content:
        return None
    quoted = re.search(r'"([^"]{15,200})"', content)
    text = ""
    if quoted:
        text = f"\"{quoted.group(1)}\""
    else:
        quoted = re.search(r"'([^']{15,200})'", content)
        if quoted:
            text = f"'{quoted.group(1)}'"
    if not quoted:
        return None
    return ContentBlock(html=f'<blockquote class="pull-quote"><p>{_h(text)}</p><span class="source">&mdash; {_h(lore.get("id", ""))}</span></blockquote>')


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


def _media_html(src: str, media: dict[str, Any], layout_hint: str = "", size_hint: str = "") -> str:
    title = media.get("title", "")
    caption = media.get("caption", "") or media.get("subject", "")
    provenance = media.get("rights_or_provenance") or f"Source: {media.get('id', '')}"
    layout_attr = f' data-layout="{css_id(layout_hint)}"' if layout_hint else ""
    size_attr = f' data-size="{css_id(size_hint)}"' if size_hint else ""
    return (
        f'<figure class="media-asset"{layout_attr}{size_attr}>'
        f'<img src="{_h(src)}" alt="{_h(title)}" />'
        f'<figcaption>{_h(caption)}</figcaption>'
        f'<div class="provenance">{_h(provenance)}</div>'
        f'</figure>'
    )


def _hero_html(src: str, media: dict[str, Any]) -> str:
    """Render a hero illustration for an editorial profile page; art goes in the reserved region."""
    layout = "bottom-right"
    size = media.get("lore_book_size", "standard")
    if size == "wide":
        layout = "bottom-wide"
    elif size == "dominant":
        layout = "dominant"
    # HTML data attributes are detected by the composer to pick the CSS grid layout.
    title = media.get("title", "")
    caption = media.get("caption", "") or media.get("subject", "")
    provenance = media.get("rights_or_provenance") or f"Source: {media.get('id', '')}"
    return (
        f'<figure class="hero-art" data-layout="{layout}" data-size="{css_id(size)}">'
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
            f'<tr><td class="priority-{css_id(priority)}">{_h(priority.upper())}</td>'
            f'<td>{_h(gap.get("description", ""))}</td>'
            f'<td>{_h(gap.get("media_type", ""))}</td>'
            f'<td>{_h(gap.get("section_id", ""))}</td></tr>'
        )
    return (
        '<table class="visual-gaps">'
        '<thead><tr><th>Priority</th><th>Opportunity</th><th>Type</th><th>Section</th></tr></thead>'
        '<tbody>' + "".join(rows) + '</tbody></table>'
    )


def _media_src(media: dict[str, Any]) -> str:
    return f"assets/{Path(media.get('file_path', '')).name}"


def _lore_entry_blocks(lore: dict[str, Any], is_profile: bool, profile_media: dict[str, Any] | None) -> list[ContentBlock]:
    blocks: list[ContentBlock] = []
    blocks.append(ContentBlock(html=f'<h3 class="lore-entry">{_h(lore.get("title", ""))}</h3>'))
    if is_profile and profile_media:
        dossier = _dossier_html(profile_media)
        if dossier:
            blocks.append(ContentBlock(html=dossier))
        quote = _pull_quote(lore)
        if quote:
            blocks.append(quote)
    content = lore.get("content", "")
    if content:
        blocks.extend(_para(content))
    else:
        blocks.append(ContentBlock(html='<p class="tbd">Intentionally unresolved — TBD.</p>'))
    blocks.append(ContentBlock(html=f'<div class="provenance">Source: {_h(lore.get("id", ""))}</div>'))
    return blocks


def _chapter_blocks(ch: Chapter) -> list[ContentBlock]:
    blocks: list[ContentBlock] = []
    is_profile = ch.layout == "editorial-profile" and ch.presentation_media

    # Section heading and status are part of the first page.
    blocks.append(ContentBlock(html=f'<h2>{_h(ch.number)}. {_h(ch.title)}</h2>'))
    blocks.append(ContentBlock(html=f'<div class="status">{_h(ch.status_note)}</div>'))

    if is_profile and ch.presentation_media:
        media = ch.presentation_media[0]
        subtitle = media.get("subject") or media.get("unit_type")
        if subtitle:
            blocks.append(ContentBlock(html=f'<div class="profile-subtitle">{_h(subtitle)}</div>'))

    for i, lore in enumerate(ch.lore_entries):
        profile = is_profile and i == 0
        profile_media = ch.presentation_media[0] if profile else None
        blocks.extend(_lore_entry_blocks(lore, profile, profile_media))

    if not ch.lore_entries:
        if is_profile and ch.presentation_media:
            dossier = _dossier_html(ch.presentation_media[0])
            if dossier:
                blocks.append(ContentBlock(html=dossier))
        blocks.append(ContentBlock(html='<p class="tbd">Intentionally unresolved — TBD.</p>'))

    if is_profile and ch.presentation_media:
        src = _media_src(ch.presentation_media[0])
        if src != "assets/":
            blocks.append(ContentBlock(html=_hero_html(src, ch.presentation_media[0]), region="art"))

    for media in ch.other_media:
        src = _media_src(media)
        if src == "assets/":
            continue
        blocks.append(ContentBlock(html=_media_html(src, media)))

    for item in ch.collection_items:
        blocks.append(ContentBlock(html=_collection_item_html(item)))

    return blocks


def _collection_item_html(item: dict[str, Any]) -> str:
    title = item.get("title", "")
    meta_parts = []
    for key in ["item_type", "quantity", "purchase_status", "painting_status"]:
        value = item.get(key)
        if value:
            meta_parts.append(f"{key.replace('_', ' ')}: {value}")
    meta = " | ".join(meta_parts)
    notes = item.get("notes", "")
    return (
        f'<div class="unit-card">'
        f'<div class="unit-name">{_h(title)}</div>'
        f'<div class="unit-meta">{_h(meta)}</div>'
        f'{_h(notes)}'
        f'</div>'
    )


def _build_cover_blocks(book: Book) -> list[ContentBlock]:
    blocks: list[ContentBlock] = []
    blocks.append(ContentBlock(html=f'<div class="edition">Edition {_h(book.edition_year)}</div>'))
    blocks.append(ContentBlock(html=f'<h1>{_h(book.title)}</h1>'))
    if book.heraldry_src:
        blocks.append(ContentBlock(html=f'<div class="cover-heraldry"><img class="dynasty-logo" src="{_h(book.heraldry_src)}" alt="Dynasty heraldry" /></div>'))
    if book.subtitle:
        blocks.append(ContentBlock(html=f'<div class="subtitle">{_h(book.subtitle)}</div>'))
    blocks.append(ContentBlock(html=f'<div class="status">Status: {_h(book.status)} &nbsp;|&nbsp; Generated: {_h(book.generated_date)}</div>'))
    return blocks


def _build_title_blocks(book: Book) -> list[ContentBlock]:
    blocks: list[ContentBlock] = []
    blocks.append(ContentBlock(html=f'<h1>{_h(book.title)}</h1>'))
    if book.subtitle:
        blocks.append(ContentBlock(html=f'<div class="subtitle">{_h(book.subtitle)}</div>'))
    blocks.append(ContentBlock(html=f'<div class="edition">Edition {_h(book.edition_year)}</div>'))
    blocks.append(ContentBlock(html=f'<div class="status">Status: {_h(book.status)} &nbsp;|&nbsp; Generated: {_h(book.generated_date)}</div>'))
    if book.heraldry_src:
        blocks.append(ContentBlock(html=f'<div class="cover-heraldry"><img class="dynasty-logo" src="{_h(book.heraldry_src)}" alt="Dynasty heraldry" /></div>'))
    return blocks


def _build_toc_placeholder() -> SectionSpec:
    return SectionSpec(number="toc", title="Contents", status_note="", theme="neutral", layout="toc", background_url=None, blocks=[])


def _build_visual_gaps_section(book: Book) -> SectionSpec | None:
    if not book.visual_gaps:
        return None
    blocks = [ContentBlock(html='<h2>Visual Opportunities</h2>'), ContentBlock(html=_render_visual_gaps(book.visual_gaps))]
    return SectionSpec(number="visual_gaps", title="Visual Opportunities", status_note="", theme=book.default_theme, layout="text", background_url=None, blocks=blocks)


def _build_appendix_section(book: Book, unassigned_lore: list[dict[str, Any]] | None = None) -> SectionSpec | None:
    if not unassigned_lore:
        return None
    blocks = [ContentBlock(html='<h2>Appendix: Other Canonical Notes</h2>')]
    for lore in unassigned_lore:
        blocks.extend(_lore_entry_blocks(lore, False, None))
    return SectionSpec(number="appendix", title="Appendix", status_note="", theme=book.default_theme, layout="text", background_url=None, blocks=blocks)


def _chapter_to_section(ch: Chapter, default_theme: str, default_background: str | None) -> SectionSpec:
    theme = ch.theme or default_theme
    background = ch.background_url or default_background
    layout = ch.layout or "text"
    return SectionSpec(
        number=ch.number,
        title=ch.title,
        status_note=ch.status_note,
        theme=theme,
        layout=layout,
        background_url=background,
        blocks=_chapter_blocks(ch),
    )


def _section_background(book: Book, section: SectionSpec) -> str | None:
    if section.number == "cover":
        return None
    if section.number == "title":
        return book.theme_backgrounds.get(book.default_theme) or _find_default_background(book, book.default_theme)
    return section.background_url


def _find_default_background(book: Book, theme_id: str) -> str | None:
    # Reuse the publication helper by copying its logic locally to avoid circular import.
    for filename in [f"{theme_id}-background.png", "background.png"]:
        candidate = book.assets_dir / filename
        if candidate.exists():
            return f"assets/{filename}"
    media_candidate = book.project_dir / "media" / "assets" / "page-decoration" / f"{theme_id}-background.png"
    if media_candidate.exists():
        book.assets_dir.mkdir(parents=True, exist_ok=True)
        import shutil
        dest = book.assets_dir / media_candidate.name
        shutil.copy2(media_candidate, dest)
        return f"assets/{media_candidate.name}"
    return None


def _build_css(book: Book) -> str:
    page_theme_ids = {book.default_theme, "cover", "neutral"}
    for ch in book.chapters:
        page_theme_ids.add(ch.theme)
    theme_classes = build_theme_classes(page_theme_ids)
    return base_css().replace("__THEME_CLASSES__", theme_classes)


def _render_page(page: Page) -> str:
    classes = f"book-page template-{css_id(page.template)} page-theme-{css_id(page.theme)}"
    if page.layout_class:
        classes += f" {page.layout_class}"
    if page.is_continuation:
        classes += " continuation"
    parts = [f'<div class="{classes}" id="page-{page.page_number}">']
    bg_style = f"background-image: url({page.background_url});" if page.background_url else ""
    parts.append(f'<div class="page-background" style="{bg_style}"></div>')

    if page.template == "toc":
        content = '<ul class="toc">' + "".join(b.html for b in page.blocks) + "</ul>"
        parts.append(f'<div class="page-safe-area">{content}</div>')
    elif page.template == "editorial-profile":
        text_html = "".join(b.html for b in page.blocks if b.region == "text")
        art_html = "".join(b.html for b in page.blocks if b.region == "art")
        parts.append(f'<div class="page-safe-area"><div class="region-text">{text_html}</div><div class="region-art">{art_html}</div></div>')
    else:
        content = "".join(b.html for b in page.blocks)
        parts.append(f'<div class="page-safe-area">{content}</div>')

    if page.template == "cover":
        parts.append('<div class="page-number"></div>')
    else:
        parts.append(f'<div class="page-number">{page.page_number}</div>')
    parts.append("</div>")
    return "\n".join(parts)


def render_html(book: Book) -> tuple[str, list[str]]:
    """Compose explicit physical pages and render the full HTML document."""
    warnings = list(book.warnings)
    css = _build_css(book)

    # Identify unassigned lore for an appendix.
    assigned_ids = set()
    for ch in book.chapters:
        for l in ch.lore_entries:
            assigned_ids.add(l.get("id"))
    unassigned_lore = [l for l in load_lore(book) if l.get("id") not in assigned_ids]

    # Build sections in canonical order.
    front_sections: list[SectionSpec] = []
    body_sections: list[SectionSpec] = []
    back_sections: list[SectionSpec] = []

    order = book.front_matter or ["cover", "title", "toc", "body", "visual_gaps", "appendix"]
    for item in order:
        if item == "cover":
            front_sections.append(SectionSpec(number="cover", title="Cover", status_note="", theme="cover", layout="cover", background_url=None, blocks=_build_cover_blocks(book)))
        elif item == "title":
            bg = _find_default_background(book, book.default_theme)
            front_sections.append(SectionSpec(number="title", title="Title", status_note="", theme=book.default_theme, layout="title", background_url=bg, blocks=_build_title_blocks(book)))
        elif item == "toc":
            front_sections.append(_build_toc_placeholder())
        elif item == "body":
            for ch in book.chapters:
                body_sections.append(_chapter_to_section(ch, book.default_theme, _find_default_background(book, ch.theme)))
        elif item == "visual_gaps":
            sec = _build_visual_gaps_section(book)
            if sec:
                back_sections.append(sec)
        elif item == "appendix":
            sec = _build_appendix_section(book, unassigned_lore)
            if sec:
                back_sections.append(sec)
        else:
            warnings.append(f"Unknown front_matter_order item: {item}")

    # Ensure a neutral theme exists for cover/toc pages without art backgrounds.
    for sec in front_sections + back_sections:
        if not sec.background_url and sec.number != "cover":
            sec.background_url = _find_default_background(book, book.default_theme)

    output_dir = book.assets_dir.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    pages, compose_warnings = compose(front_sections, body_sections, back_sections, css, output_dir)
    warnings.extend(compose_warnings)

    html_parts = [
        "<!DOCTYPE html>",
        '<html lang="en"><head>',
        '<meta charset="utf-8">',
        f"<title>{_h(book.title)}</title>",
        "<style>",
        css,
        "</style>",
        "</head><body>",
    ]
    for pg in pages:
        html_parts.append(_render_page(pg))
    html_parts.append("</body></html>")
    return "\n".join(html_parts), warnings


def load_lore(book: Book) -> list[dict[str, Any]]:
    """Load all canonical lore entries from the project directory."""
    from .publication import load_objects
    return load_objects(book.project_dir / "lore")
