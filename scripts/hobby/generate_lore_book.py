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


def _find_object(objects: list[dict[str, Any]], *, id: str | None = None, schema: str | None = None) -> dict[str, Any] | None:
    for obj in objects:
        if id is not None and obj.get("id") != id:
            continue
        if schema is not None and obj.get("schema") != schema:
            continue
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
    return (
        f'<figure class="media-asset">'
        f'<img src="{_h(src)}" alt="{_h(title)}" />'
        f'<figcaption>{_h(caption)}</figcaption>'
        f'<div class="provenance">{_h(provenance)}</div>'
        f'</figure>'
    )


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
      size: A4 portrait;
      margin: 15mm;
      bleed: 3mm;
      @bottom-center { content: counter(page); font-size: 9pt; color: var(--muted); }
    }
    * { box-sizing: border-box; }
    html, body {
      margin: 0;
      padding: 0;
      background: var(--bg);
      color: var(--fg);
      font-family: Georgia, "Times New Roman", serif;
      font-size: 11pt;
      line-height: 1.55;
    }
    .page {
      width: 210mm;
      min-height: 297mm;
      padding: 18mm;
      margin: 0 auto 12mm auto;
      background: var(--bg);
      border: 1px solid var(--line);
      page-break-after: always;
      position: relative;
    }
    .page:last-child { page-break-after: auto; }
    h1, h2, h3, h4 {
      color: var(--silver);
      font-weight: 400;
      letter-spacing: 0.03em;
      margin-top: 0;
    }
    h1 { font-size: 28pt; text-transform: uppercase; margin-bottom: 6mm; }
    h2 { font-size: 18pt; color: var(--cyan); border-bottom: 1px solid var(--line); padding-bottom: 2mm; margin-top: 10mm; }
    h3 { font-size: 13pt; color: var(--silver); margin-top: 8mm; }
    .cover { display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; min-height: 240mm; }
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
    .chapter-opener { page-break-before: always; }
    .spread { page-break-before: always; }
    .small-caps { font-variant: small-caps; }
    .media-asset { margin-top: 6mm; text-align: center; }
    .media-asset img { max-width: 100%; max-height: 200mm; border: 1px solid var(--line); }
    .media-asset figcaption { font-size: 10pt; color: var(--silver); margin-top: 2mm; }
    @media print {
      body { background: #fff; }
      .page { border: none; margin: 0; }
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


def _build_book(
    edition: dict[str, Any],
    outline: dict[str, Any],
    lore_entries: list[dict[str, Any]],
    media_entries: list[dict[str, Any]],
    project_dir: Path,
    output_path: Path,
) -> str:
    title = edition.get("title", "Hobby Lore Book")
    subtitle = edition.get("subtitle", "")
    edition_year = edition.get("edition_year", datetime.now().year)
    status = edition.get("edition_status", "draft")
    generated_date = edition.get("generated_date", datetime.now().strftime("%Y-%m-%d"))

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
        for media in explicit_map.get(num, []):
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

    # Prepare output asset directory
    output_dir = output_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    html_parts: list[str] = [
        "<!DOCTYPE html>",
        "<html lang=\"en\"><head>",
        "<meta charset=\"utf-8\">",
        f"<title>{_h(title)}</title>",
        "<style>",
        _css(),
        "</style>",
        "</head><body>",
    ]

    # Cover
    html_parts.append('<section class="page cover">')
    html_parts.append(f'<div class="edition">Edition {edition_year}</div>')
    html_parts.append(f'<h1>{_h(title)}</h1>')
    if subtitle:
        html_parts.append(f'<div class="subtitle">{_h(subtitle)}</div>')
    html_parts.append(f'<div class="status">Status: {_h(status)} &nbsp;|&nbsp; Generated: {_h(generated_date)}</div>')
    html_parts.append("</section>")

    # TOC
    html_parts.append('<section class="page toc">')
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
        html_parts.append('<section class="page">')
        html_parts.append(f'<h2>{_h(num)}. {_h(sec_title)}</h2>')
        html_parts.append(f'<div class="status">{status_note}</div>')
        if matched:
            for lore in matched:
                html_parts.append(f'<h3>{_h(lore.get("title", ""))}</h3>')
                content = lore.get("content", "")
                if content:
                    html_parts.append(_para(content))
                html_parts.append(f'<div class="provenance">Source: {_h(lore.get("id", ""))}</div>')
        else:
            html_parts.append('<p class="tbd">Intentionally unresolved — TBD.</p>')

        if medias:
            html_parts.append('<h3>Visual reference</h3>')
            for media in medias:
                src = _copy_media_asset(media, project_dir, output_dir)
                if src:
                    html_parts.append(_media_html(src, media))

        html_parts.append('</section>')

    # Visual opportunities
    html_parts.append('<section class="page">')
    html_parts.append('<h2>Visual Opportunities</h2>')
    html_parts.append(_render_visual_gaps(edition.get("visual_gaps", [])))
    html_parts.append('</section>')

    # Appendix
    if unassigned:
        html_parts.append('<section class="page">')
        html_parts.append('<h2>Appendix: Other Canonical Notes</h2>')
        for lore in unassigned:
            html_parts.append(f'<h3>{_h(lore.get("title", ""))}</h3>')
            content = lore.get("content", "")
            if content:
                html_parts.append(_para(content))
            html_parts.append(f'<div class="provenance">Source: {_h(lore.get("id", ""))}</div>')
        html_parts.append('</section>')

    html_parts.append("</body></html>")
    return "\n".join(html_parts)


def main():
    parser = argparse.ArgumentParser(description="Generate a print-oriented annual lore-book HTML artifact.")
    parser.add_argument("--life-dir", type=Path, help="Path to ethan-life repository root.")
    parser.add_argument("--project", default=DEFAULT_PROJECT, help="Hobby project slug.")
    parser.add_argument("--edition", type=int, default=datetime.now().year, help="Edition year.")
    parser.add_argument("--edition-id", help="Optional explicit edition object ID.")
    parser.add_argument("--output", type=Path, help="Output HTML file path.")
    parser.add_argument("--draft", action="store_true", help="Render a draft; do not finalize the edition object.")
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

    outline = _find_object(sections, schema="hobby.lore-book-section") or {}

    lore_entries = _load_objects(lore_dir)
    media_entries = _load_objects(project_dir / "media")

    if args.output:
        output_path = args.output
    else:
        output_dir = life_dir / "reports" / DOMAIN / args.project / "lore-book" / str(args.edition)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "lore-book.html"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    html_doc = _build_book(edition, outline, lore_entries, media_entries, project_dir, output_path)

    output_path.write_text(html_doc, encoding="utf-8")
    print(f"Lore book rendered: {output_path}")


if __name__ == "__main__":
    main()
