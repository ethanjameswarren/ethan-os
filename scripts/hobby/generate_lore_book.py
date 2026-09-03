#!/usr/bin/env python3
"""
Generate a print-oriented HTML annual lore book from Ethan Life hobby data.

Reads:
- hobby.lore-book-edition objects
- hobby.lore-book-section objects
- hobby.lore-canon objects

Does NOT include raw battle reports, collection status, points, or session logs.
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


DEFAULT_PROJECT = "warhammer-40k-necron-dynasty"
DOMAIN = "hobby"


def _parse_frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as exc:
        print(f"Warning: failed to parse frontmatter: {exc}", file=sys.stderr)
        return {}


def _load_objects(directory: Path) -> list[dict[str, Any]]:
    objects: list[dict[str, Any]] = []
    if not directory.exists():
        return objects
    for path in directory.rglob("*.md"):
        try:
            data = _parse_frontmatter(path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"Warning: could not read {path}: {exc}", file=sys.stderr)
            continue
        if not data:
            continue
        data["_source_path"] = path
        objects.append(data)
    return objects


def _find_object(objects: list[dict[str, Any]], **filters: Any) -> dict[str, Any] | None:
    for obj in objects:
        if all(obj.get(k) == v for k, v in filters.items()):
            return obj
    return None


def _section_keywords(title: str) -> set[str]:
    """Extract simple keywords from a section title."""
    words = re.findall(r"[A-Za-z']+", title.lower())
    return set(words)


def _lore_score(section_title: str, lore_title: str) -> int:
    """Rough relevance score between a book section and a lore entry."""
    section_kw = _section_keywords(section_title)
    lore_kw = _section_keywords(lore_title)
    score = len(section_kw & lore_kw)
    # Boost for key substrings
    sl = section_title.lower()
    ll = lore_title.lower()
    if "destroyer" in sl and "destroyer" in ll:
        score += 3
    if "ctan" in sl or "c'tan" in sl:
        if "ctan" in ll or "c'tan" in ll:
            score += 3
    if "visual" in sl and "visual" in ll:
        score += 3
    if "philosophy" in sl and ("philosophy" in ll or "doctrine" in ll or "hierarchy" in ll):
        score += 2
    if "origins" in sl or "history" in sl:
        if any(x in ll for x in ["pre-biotransference", "biotransference", "great sleep", "awakening", "mortality", "aftermath"]):
            score += 2
    return score


def _media_score(section_title: str, lore_titles: list[str], media: dict[str, Any]) -> int:
    """Rough relevance score between a book section and a media asset."""
    if media.get("media_type") in ("page_decoration", "heraldry"):
        return 0
    section_kw = _section_keywords(section_title)
    lore_kw: set[str] = set()
    for lt in lore_titles:
        lore_kw |= _section_keywords(lt)

    # Gather tokens from the media record
    media_text = " ".join([
        str(media.get("subject", "")),
        str(media.get("unit_type", "")),
        str(media.get("associated_lore_concept", "")),
        str(media.get("color_scheme", "")),
        str(media.get("energy_color", "")),
        " ".join(str(t) for t in media.get("tags", [])),
    ])
    media_kw = _section_keywords(media_text)

    score = 0
    for kw in (media_kw & section_kw):
        score += 3
    for kw in (media_kw & lore_kw):
        score += 2
    return score


def _copy_media_asset(media: dict[str, Any], project_dir: Path, output_dir: Path) -> str | None:
    """Copy a media asset into the report output and return a relative HTML src path."""
    src = project_dir / media.get("file_path", "")
    if not src.exists():
        print(f"Warning: media asset not found: {src}", file=sys.stderr)
        return None
    assets_dir = output_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    dest = assets_dir / src.name
    try:
        shutil.copy2(src, dest)
    except Exception as exc:
        print(f"Warning: could not copy {src}: {exc}", file=sys.stderr)
        return None
    return f"assets/{_h(src.name)}"


def _media_html(src: str, media: dict[str, Any]) -> str:
    """HTML for a single embedded media asset."""
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


def _dossier_html(media: dict[str, Any]) -> str:
    """Compact fact/dossier box from available media metadata."""
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


def _pull_quote(lore: dict[str, Any]) -> str | None:
    """Extract a short canon quotation from lore for a pull quote, if one exists."""
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


def _extract_outline_sections(content: str) -> list[tuple[str, str, str]]:
    """Return list of (number, title, status_note) from outline content.

    YAML folded scalars (`>`) may join list entries into a single line, so we
    scan the whole content rather than splitting by line.
    """
    sections: list[tuple[str, str, str]] = []
    for match in re.finditer(r"\s*(\d+)\.\s+(.+?)\s*[—–-]\s*([^\n\r]+?)(?=\s*\d+\.|\s*$)", content):
        sections.append((match.group(1), match.group(2).strip(), match.group(3).strip()))
    return sections


def _css() -> str:
    return r"""
    :root {
      --bg: #0b0c0e;
      --fg: #d8dde6;
      --muted: #8a93a3;
      --cyan: #2dd4bf;
      --red: #ef4444;
      --purple: #a855f7;
      --silver: #c7cdd6;
      --line: #2a2d33;
    }
    @page {
      size: 6in 9in;
      margin: 0.6in 0.5in 0.6in 0.6in;
      @bottom-center {
        content: counter(page);
        font-size: 7pt;
        color: var(--muted);
      }
    }
    __PAGE_RULES__
    * { box-sizing: border-box; print-color-adjust: exact; -webkit-print-color-adjust: exact; }
    html, body {
      margin: 0;
      padding: 0;
      background: var(--bg);
      color: var(--fg);
      font-family: Georgia, "Times New Roman", serif;
      font-size: 11pt;
      line-height: 1.55;
    }
    h1, h2, h3, h4 {
      color: var(--silver);
      font-weight: 400;
      letter-spacing: 0.03em;
      margin-top: 0;
    }
    h1 { font-size: 28pt; text-transform: uppercase; margin-bottom: 6mm; }
    h2 { font-size: 18pt; color: var(--cyan); border-bottom: 1px solid var(--line); padding-bottom: 2mm; margin-top: 10mm; break-after: avoid; }
    h3 { font-size: 13pt; color: var(--silver); margin-top: 8mm; break-after: avoid; }
    p { orphans: 2; widows: 2; }
    section { break-before: always; display: flow-root; }
    section.cover { break-before: auto; display: flex; }
    .lore-section { page-break-before: always; break-before: always; page-break-after: always; break-after: page; }
    .lore-section:last-of-type { page-break-after: auto; break-after: auto; }
    .lore-section:first-of-type { break-before: auto; }
    .cover {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      min-height: 7.8in;
    }
    .cover h1 { font-size: 36pt; margin-bottom: 12mm; }
    .cover .subtitle { font-size: 14pt; color: var(--muted); margin-bottom: 8mm; }
    .cover .edition { font-size: 11pt; color: var(--cyan); text-transform: uppercase; letter-spacing: 0.15em; }
    .toc ul { list-style: none; padding: 0; }
    .toc li { display: flex; justify-content: space-between; border-bottom: 1px dotted var(--line); padding: 2mm 0; }
    .toc .status { color: var(--muted); font-size: 9pt; }
    .tbd { color: var(--muted); font-style: italic; }
    .status { font-size: 9pt; color: var(--muted); }
    .visual-gaps { width: 100%; border-collapse: collapse; margin-top: 6mm; }
    .visual-gaps th, .visual-gaps td { border-bottom: 1px solid var(--line); padding: 2mm 1mm; text-align: left; }
    .visual-gaps th { color: var(--cyan); font-weight: 400; }
    .priority-required { color: var(--red); }
    .priority-recommended { color: var(--purple); }
    .priority-optional { color: var(--muted); }
    .provenance { font-size: 8pt; color: var(--muted); margin-top: 4mm; }
    .small-caps { font-variant: small-caps; }
    .media-asset { margin-top: 6mm; text-align: center; break-inside: avoid; }
    .media-asset img { max-width: 100%; max-height: 140mm; border: 1px solid var(--line); }
    .media-asset figcaption { font-size: 10pt; color: var(--silver); margin-top: 2mm; }
    figure.illustration { float: right; clear: right; margin: 0; text-align: right; border: none; background: transparent; }
    figure.illustration img { width: 100%; height: 100%; object-fit: contain; border: none; background: transparent; }
    figure.illustration figcaption, figure.illustration .provenance { display: none; }
    figure.illustration.illustration-size-standard { width: 2.1in; height: 5.5in; margin-top: 2.15in; margin-left: 0.35in; }
    figure.illustration.illustration-size-dominant { width: 2.7in; height: 5.5in; margin-top: 2.15in; margin-left: 0.35in; }
    figure.illustration.illustration-layout-floating-bottom-wide { width: 3.3in; height: 4in; margin-top: 3.65in; margin-left: 0.35in; }
    @media (max-width: 600px) {
      figure.illustration { float: none; width: 80%; height: auto; margin: 0 auto 0.2in auto; text-align: center; }
      .illustration-size-standard, .illustration-size-dominant, .illustration-layout-floating-bottom-wide { width: 80%; height: auto; margin-top: 0.2in; }
    }
    .dynasty-logo { display: block; max-width: 100%; height: auto; border: none; background: transparent; }
    .cover-heraldry { width: 1.8in; margin: 0.3in auto 0 auto; }
    .editorial-profile { display: flow-root; }
    .editorial-profile .profile-subtitle {
      font-size: 9pt;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.12em;
      margin-top: -4mm;
      margin-bottom: 4mm;
    }
    .editorial-profile figure.hero {
      float: right;
      clear: right;
      margin: 0;
      text-align: right;
      border: none;
      background: transparent;
    }
    .editorial-profile figure.hero img { width: 100%; height: 100%; object-fit: contain; border: none; background: transparent; }
    .editorial-profile figure.hero figcaption, .editorial-profile figure.hero .provenance { display: none; }
    .editorial-profile figure.hero.hero-standard { width: 1.9in; height: 3.5in; margin-top: 1.0in; margin-left: 0.35in; }
    .editorial-profile figure.hero.hero-dominant { width: 2.5in; height: 3.0in; margin-top: 1.0in; margin-left: 0.35in; }
    .editorial-profile figure.hero.hero-wide { width: 3.1in; height: 2.5in; margin-top: 1.0in; margin-left: 0.35in; }
    .pull-quote {
      float: left;
      clear: left;
      width: 2.0in;
      margin: 4mm 0.3in 4mm 0;
      padding: 4mm 4mm 4mm 3mm;
      border-left: 2pt solid var(--cyan);
      color: var(--silver);
      font-size: 12pt;
      font-style: italic;
      line-height: 1.35;
      break-inside: avoid;
    }
    .pull-quote .source { display: block; font-size: 7pt; color: var(--muted); font-style: normal; margin-top: 2mm; }
    .dossier {
      float: right;
      clear: right;
      width: 1.9in;
      margin: 4mm 0 4mm 0.3in;
      border: 1px solid var(--line);
      padding: 3mm;
      font-size: 8pt;
      break-inside: avoid;
    }
    .dossier dt { color: var(--cyan); text-transform: uppercase; font-size: 6.5pt; letter-spacing: 0.05em; margin-top: 2mm; }
    .dossier dd { margin: 0; color: var(--silver); }
    .lore-callout { border-left: 1pt solid var(--line); padding-left: 3mm; margin: 4mm 0; color: var(--muted); font-style: italic; }
    .detail-callout { break-inside: avoid; margin: 4mm 0; text-align: center; }
    .detail-callout img { max-width: 100%; max-height: 25mm; border: 1px solid var(--line); }
    .secondary-image { float: right; clear: right; width: 1.2in; margin: 0.2in 0 0.2in 0.2in; }
    .facing-spread { break-before: left; page: spread; }
    .theme-cyan .pull-quote { border-left-color: var(--cyan); }
    .theme-cyan .dossier dt { color: var(--cyan); }
    .theme-cyan h2, .theme-cyan h3 { color: var(--cyan); }
    .theme-red .pull-quote { border-left-color: var(--red); }
    .theme-red .dossier dt { color: var(--red); }
    .theme-red h2, .theme-red h3 { color: var(--red); }
    .theme-purple .pull-quote { border-left-color: var(--purple); }
    .theme-purple .dossier dt { color: var(--purple); }
    .theme-purple h2, .theme-purple h3 { color: var(--purple); }
    @media (max-width: 600px) {
      .editorial-profile figure.hero, .pull-quote, .dossier, .secondary-image { float: none; width: 80%; margin: 0.2in auto; }
    }
"""


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


def _render_visual_gaps(gaps: list[dict[str, Any]]) -> str:
    if not gaps:
        return "<p class=\"tbd\">No visual gaps recorded.</p>"
    rows = []
    for gap in gaps:
        priority = gap.get("priority", "optional")
        rows.append(
            f"<tr><td class=\"priority-{_h(priority)}\">{_h(priority.upper())}</td>"
            f"<td>{_h(gap.get('description', ''))}</td>"
            f"<td>{_h(gap.get('media_type', ''))}</td>"
            f"<td>{_h(gap.get('section_id', ''))}</td></tr>"
        )
    return (
        "<table class=\"visual-gaps\">"
        "<thead><tr><th>Priority</th><th>Opportunity</th><th>Type</th><th>Section</th></tr></thead>"
        "<tbody>" + "".join(rows) + "</tbody></table>"
    )


def _css_id(value: str) -> str:
    ident = re.sub(r"[^A-Za-z0-9_-]", "-", value)
    if not ident or not ident[0].isalpha():
        ident = "t-" + ident
    return ident


def _build_page_rules(theme_to_bg: dict[str, str]) -> str:
    rules = []
    for name, bg in theme_to_bg.items():
        bg = bg if bg and bg != "none" else "none"
        rules.append(
            f"    @page {name} {{\n"
            "      size: 6in 9in;\n"
            "      margin: 0.6in 0.5in 0.6in 0.6in;\n"
            "      background-color: var(--bg);\n"
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
    return "\n".join(rules)


def _build_book(
    edition: dict[str, Any],
    outline: dict[str, Any],
    lore_entries: list[dict[str, Any]],
    media_entries: list[dict[str, Any]],
    project_dir: Path,
    output_path: Path,
    page_background: Path | None = None,
    section_map: dict[str, Any] | None = None,
) -> str:
    title = edition.get("title", "Hobby Lore Book")
    subtitle = edition.get("subtitle", "")
    edition_year = edition.get("edition_year", datetime.now().year)
    status = edition.get("edition_status", "draft")
    generated_date = edition.get("generated_date", datetime.now().strftime("%Y-%m-%d"))

    output_dir = output_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    page_bg_url = None
    if page_background and page_background.exists():
        assets_dir = output_dir / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(page_background, assets_dir / "background.png")
        page_bg_url = "url(assets/background.png)"
    if not page_bg_url:
        for media in media_entries:
            if media.get("media_type") == "page_decoration" and media.get("status") == "available":
                src = _copy_media_asset(media, project_dir, output_dir)
                if src:
                    page_bg_url = f"url({_h(src)})"
                    break
    default_theme = _css_id("default")
    default_bg = page_bg_url or "none"

    # Load canonical dynasty heraldry for publication furniture
    heraldry_media = next(
        (m for m in media_entries if m.get("media_type") == "heraldry" and m.get("canon_status") == "canonical"),
        None,
    )
    heraldry_src = _copy_media_asset(heraldry_media, project_dir, output_dir) if heraldry_media else None

    section_map = section_map or {}

    # Build named page themes so continuation pages inherit the same background.
    theme_to_bg: dict[str, str] = {default_theme: default_bg}
    section_themes: dict[str, str] = {}
    for num in section_map:
        bg_id = section_map[num].get("background_media_id")
        if bg_id:
            bg_media = _find_object(media_entries, id=bg_id)
            if bg_media:
                bg_src = _copy_media_asset(bg_media, project_dir, output_dir)
                if bg_src:
                    theme = _css_id(f"bg-{_h(bg_src)}")
                    section_themes[num] = theme
                    theme_to_bg[theme] = f"url({_h(bg_src)})"
    css = _css().replace("__PAGE_RULES__", _build_page_rules(theme_to_bg))

    sections = _extract_outline_sections(outline.get("content", ""))
    # Assign lore to sections
    assigned_lore: set[str] = set()
    raw_blocks: list[tuple[str, str, str, list[dict[str, Any]]]] = []
    for num, sec_title, status_note in sections:
        matched = []
        scored = []
        for lore in lore_entries:
            score = _lore_score(sec_title, lore.get("title", ""))
            if score > 0:
                scored.append((score, lore))
        scored.sort(key=lambda x: x[0], reverse=True)
        for score, lore in scored:
            if len(matched) >= 4:
                break
            lid = lore.get("id")
            if lid in assigned_lore:
                continue
            matched.append(lore)
            assigned_lore.add(lid)
        raw_blocks.append((num, sec_title, status_note, matched))

    # Assign media to sections
    # Precedence:
    # 1. explicit lore_book_section_id / lore_book_section_ids
    # 2. explicit related_lore_ids
    # 3. keyword inference (only for media with no explicit section assignment)
    reserved_explicit: set[str] = set()
    for media in media_entries:
        mid = media.get("id")
        if not mid:
            continue
        if media.get("lore_book_section_id") or media.get("lore_book_section_ids"):
            reserved_explicit.add(mid)

    assigned_media: set[str] = set()
    explicit_map: dict[str, list[dict[str, Any]]] = {}
    for media in media_entries:
        mid = media.get("id")
        if not mid:
            continue
        if media.get("lore_book_section_id"):
            explicit_map.setdefault(str(media.get("lore_book_section_id")), []).append(media)
        for sid in media.get("lore_book_section_ids", []) or []:
            explicit_map.setdefault(str(sid), []).append(media)

    section_blocks: list[tuple[str, str, str, list[dict[str, Any]], list[dict[str, Any]]]] = []
    for num, sec_title, status_note, matched in raw_blocks:
        lore_titles = [lore.get("title", "") for lore in matched]
        lore_ids = {lore.get("id") for lore in matched}

        chosen: list[dict[str, Any]] = []

        # 1. explicit section assignment
        # Prefer lore_book_presentation media if present; otherwise use all explicit assets.
        explicit_candidates = explicit_map.get(num, [])
        presentation = [m for m in explicit_candidates if m.get("lore_book_presentation")]
        chosen_media = presentation if presentation else explicit_candidates
        for media in chosen_media:
            mid = media.get("id")
            if mid and mid not in assigned_media:
                chosen.append(media)
                assigned_media.add(mid)

        # 2. related lore ids
        if not chosen:
            for media in media_entries:
                mid = media.get("id")
                if not mid or mid in assigned_media or mid in reserved_explicit:
                    continue
                related = set(media.get("related_lore_ids", []) or [])
                if related & lore_ids:
                    chosen.append(media)
                    assigned_media.add(mid)
                    break

        # 3. keyword inference for remaining
        if not chosen:
            media_scored = []
            for media in media_entries:
                mid = media.get("id")
                if not mid or mid in assigned_media or mid in reserved_explicit:
                    continue
                score = _media_score(sec_title, lore_titles, media)
                if score > 0:
                    media_scored.append((score, media))
            media_scored.sort(key=lambda x: x[0], reverse=True)
            for _, media in media_scored:
                if len(chosen) >= 1:
                    break
                mid = media.get("id")
                if mid in assigned_media:
                    continue
                chosen.append(media)
                assigned_media.add(mid)

        section_blocks.append((num, sec_title, status_note, matched, chosen))

    # Unassigned lore goes to appendix
    unassigned = [l for l in lore_entries if l.get("id") not in assigned_lore]

    html_parts: list[str] = [
        "<!DOCTYPE html>",
        "<html lang=\"en\"><head>",
        "<meta charset=\"utf-8\">",
        f"<title>{_h(title)}</title>",
        "<style>",
        css,
        "</style>",
        "</head><body>",
    ]

    # Cover
    html_parts.append(f'<section class="cover" style="page: {default_theme};">')
    html_parts.append(f'<div class="edition">Edition {edition_year}</div>')
    html_parts.append(f'<h1>{_h(title)}</h1>')
    if heraldry_src:
        html_parts.append(f'<div class="cover-heraldry"><img class="dynasty-logo" src="{_h(heraldry_src)}" alt="Dynasty heraldry" /></div>')
    if subtitle:
        html_parts.append(f'<div class="subtitle">{_h(subtitle)}</div>')
    html_parts.append(f'<div class="status">Status: {_h(status)} &nbsp;|&nbsp; Generated: {_h(generated_date)}</div>')
    html_parts.append('</section>')

    # TOC
    html_parts.append(f'<section class="lore-section toc" style="page: {default_theme};">')
    html_parts.append('<h2>Contents</h2>')
    html_parts.append('<ul>')
    for num, sec_title, status_note, _, _ in section_blocks:
        html_parts.append(
            f'<li><span>{_h(num)}. {_h(sec_title)}</span> <span class="status">{_h(status_note)}</span></li>'
        )
    html_parts.append('</ul>')
    html_parts.append('</section>')

    # Sections
    for num, sec_title, status_note, matched, medias in section_blocks:
        theme = section_themes.get(num, default_theme)
        presentation_medias = [m for m in medias if m.get("lore_book_presentation")]
        other_medias = [m for m in medias if not m.get("lore_book_presentation")]

        is_profile = False
        is_spread = False
        energy_color = "cyan"
        hero_size = "standard"
        if presentation_medias:
            layout = presentation_medias[0].get("lore_book_layout", "floating-bottom-right")
            if layout == "editorial-profile":
                is_profile = True
                energy_color = presentation_medias[0].get("energy_color", "cyan") or "cyan"
                hero_size = presentation_medias[0].get("lore_book_size", "standard") or "standard"
            elif layout == "facing-spread":
                is_spread = True
                energy_color = presentation_medias[0].get("energy_color", "cyan") or "cyan"

        section_classes = ["lore-section"]
        if is_profile:
            section_classes.append("editorial-profile")
        if is_spread:
            section_classes.append("facing-spread")
        section_classes.append(f"theme-{_h(energy_color)}")
        class_attr = " ".join(section_classes)

        html_parts.append(f'<section class="{_h(class_attr)}" style="page: {theme};">')
        hero_html = ""
        for media in presentation_medias:
            src = _copy_media_asset(media, project_dir, output_dir)
            if src:
                if is_profile and not hero_html:
                    hero_html = _media_html(src, media)
                elif not is_profile:
                    html_parts.append(_media_html(src, media))

        html_parts.append(f'<h2>{_h(num)}. {_h(sec_title)}</h2>')
        html_parts.append(f'<div class="status">{_h(status_note)}</div>')

        if is_profile and presentation_medias:
            subtitle = presentation_medias[0].get("subject") or presentation_medias[0].get("unit_type")
            if subtitle:
                html_parts.append(f'<div class="profile-subtitle">{_h(subtitle)}</div>')

        dossier = ""
        if is_profile and presentation_medias and hero_size != "wide":
            dossier = _dossier_html(presentation_medias[0])

        if matched:
            for i, lore in enumerate(matched):
                html_parts.append(f'<h3>{_h(lore.get("title", ""))}</h3>')
                if i == 0 and is_profile:
                    if dossier:
                        html_parts.append(dossier)
                    quote = _pull_quote(lore)
                    if quote:
                        html_parts.append(quote)
                    if hero_html:
                        html_parts.append(hero_html)
                        hero_html = ""
                content = lore.get("content", "")
                if content:
                    html_parts.append(_para(content))
                else:
                    html_parts.append('<p class="tbd">Intentionally unresolved — TBD.</p>')
                html_parts.append(f'<div class="provenance">Source: {_h(lore.get("id", ""))}</div>')
        else:
            if is_profile:
                if dossier:
                    html_parts.append(dossier)
                if hero_html:
                    html_parts.append(hero_html)
            html_parts.append('<p class="tbd">Intentionally unresolved — TBD.</p>')

        if other_medias:
            html_parts.append('<h3>Visual reference</h3>')
            for media in other_medias:
                src = _copy_media_asset(media, project_dir, output_dir)
                if src:
                    html_parts.append(_media_html(src, media))

        html_parts.append('</section>')

    # Visual opportunities
    html_parts.append(f'<section class="lore-section" style="page: {default_theme};">')
    html_parts.append('<h2>Visual Opportunities</h2>')
    html_parts.append(_render_visual_gaps(edition.get("visual_gaps", [])))
    html_parts.append('</section>')

    # Appendix
    if unassigned:
        html_parts.append(f'<section class="lore-section" style="page: {default_theme};">')
        html_parts.append('<h2>Appendix: Other Canonical Notes</h2>')
        for lore in unassigned:
            html_parts.append(f'<h3>{_h(lore.get("title", ""))}</h3>')
            content = lore.get("content", "")
            if content:
                html_parts.append(_para(content))
            else:
                html_parts.append('<p class="tbd">Intentionally unresolved — TBD.</p>')
            html_parts.append(f'<div class="provenance">Source: {_h(lore.get("id", ""))}</div>')
        html_parts.append('</section>')

    html_parts.append("</body></html>")
    return "\n".join(html_parts)


def _render_pdf(html_path: Path, pdf_path: Path) -> None:
    """Render the HTML to a print-ready PDF using Paged.js CLI."""
    html_uri = html_path.resolve().as_uri()
    cmd = ["npx", "-y", "pagedjs-cli", "--inputs", html_uri, "--output", str(pdf_path)]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=600, shell=True)
    except FileNotFoundError as exc:
        raise RuntimeError(
            "Paged.js CLI (pagedjs-cli) is not available. "
            "Install Node and run: npm install -g pagedjs-cli"
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"PDF render failed: {exc.stderr or exc.stdout}") from exc
    print(f"PDF rendered: {pdf_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate a print-ready annual lore-book HTML preview and PDF.")
    parser.add_argument("--life-dir", type=Path, help="Path to ethan-life repository root.")
    parser.add_argument("--project", default=DEFAULT_PROJECT, help="Hobby project slug.")
    parser.add_argument("--edition", type=int, default=datetime.now().year, help="Edition year.")
    parser.add_argument("--edition-id", help="Optional explicit edition object ID.")
    parser.add_argument("--output", type=Path, help="Output HTML file path.")
    parser.add_argument("--draft", action="store_true", help="Render a draft; do not finalize the edition object.")
    parser.add_argument("--page-background", type=Path, help="Path to an image to use as the background for every page.")
    args = parser.parse_args()

    life_dir = args.life_dir
    if not life_dir:
        life_dir = Path(__file__).resolve().parents[3] / "ethan-life"
    life_dir = Path(life_dir)

    project_dir = life_dir / "domains" / DOMAIN / args.project
    lore_dir = project_dir / "lore"
    book_dir = project_dir / "lore-book"
    edition_dir = book_dir / str(args.edition)

    # Load edition and outline
    sections = _load_objects(book_dir)
    editions = [s for s in sections if s.get("schema") == "hobby.lore-book-edition"]
    edition: dict[str, Any] | None = None
    if args.edition_id:
        edition = _find_object(editions, id=args.edition_id)
    if not edition:
        edition = _find_object(editions, id=f"lb-edition-{args.edition}")
    if not edition and editions:
        edition = editions[0]
    if not edition:
        edition = {
            "id": f"lb-edition-{args.edition}",
            "title": f"{args.project} Lore Book",
            "edition_year": args.edition,
            "subtitle": "Draft",
            "edition_status": "draft",
            "generated_date": datetime.now().strftime("%Y-%m-%d"),
            "visual_gaps": [],
        }

    outline = _find_object(sections, schema="hobby.lore-book-section", section_number="0") or {}
    section_map = {s.get("section_number"): s for s in sections if s.get("schema") == "hobby.lore-book-section"}

    lore_entries = _load_objects(lore_dir)
    media_entries = _load_objects(project_dir / "media")

    if args.output:
        output_path = args.output
    else:
        output_dir = life_dir / "reports" / DOMAIN / args.project / "lore-book" / str(args.edition)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "lore-book.html"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    html_doc = _build_book(edition, outline, lore_entries, media_entries, project_dir, output_path, page_background=args.page_background, section_map=section_map)

    output_path.write_text(html_doc, encoding="utf-8")
    print(f"Lore book rendered: {output_path}")

    pdf_path = output_path.with_suffix(".pdf")
    _render_pdf(output_path, pdf_path)


if __name__ == "__main__":
    main()
