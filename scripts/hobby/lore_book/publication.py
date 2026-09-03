"""Publication data loading and content assembly for the lore book."""
from __future__ import annotations

import re
import shutil
import struct
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


DEFAULT_PROJECT = "warhammer-40k-necron-dynasty"
DEFAULT_DOMAIN = "hobby"
DEFAULT_TRIM = (6.0, 9.0)
DEFAULT_MARGINS = (0.6, 0.5, 0.6, 0.5)
DEFAULT_BLEED = 0.0
DEFAULT_THEME = "cyan"


def parse_frontmatter(text: str) -> dict[str, Any]:
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


def load_objects(directory: Path) -> list[dict[str, Any]]:
    objects: list[dict[str, Any]] = []
    if not directory.exists():
        return objects
    for path in sorted(directory.rglob("*.md")):
        try:
            data = parse_frontmatter(path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"Warning: could not read {path}: {exc}", file=sys.stderr)
            continue
        if not data:
            continue
        data["_source_path"] = path
        objects.append(data)
    return objects


def find_object(objects: list[dict[str, Any]], **filters: Any) -> dict[str, Any] | None:
    for obj in objects:
        if all(obj.get(k) == v for k, v in filters.items()):
            return obj
    return None


def png_dimensions(path: Path) -> tuple[int, int] | None:
    try:
        with path.open("rb") as f:
            header = f.read(24)
        if not header.startswith(b"\x89PNG\r\n\x1a\n") or header[12:16] != b"IHDR":
            return None
        width, height = struct.unpack(">II", header[16:24])
        return width, height
    except Exception:
        return None


def copy_media_asset(media: dict[str, Any], project_dir: Path, assets_dir: Path) -> str | None:
    src = project_dir / media.get("file_path", "")
    if not src.exists():
        print(f"Warning: media asset not found: {src}", file=sys.stderr)
        return None
    assets_dir.mkdir(parents=True, exist_ok=True)
    dest = assets_dir / src.name
    try:
        shutil.copy2(src, dest)
    except Exception as exc:
        print(f"Warning: could not copy {src}: {exc}", file=sys.stderr)
        return None
    return f"assets/{src.name}"


def _section_keywords(title: str) -> set[str]:
    words = re.findall(r"[A-Za-z']+", title.lower())
    return set(words)


def _lore_score(section_title: str, lore_title: str) -> int:
    section_kw = _section_keywords(section_title)
    lore_kw = _section_keywords(lore_title)
    score = len(section_kw & lore_kw)
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
    if media.get("media_type") in ("page_decoration", "heraldry"):
        return 0
    section_kw = _section_keywords(section_title)
    lore_kw: set[str] = set()
    for lt in lore_titles:
        lore_kw |= _section_keywords(lt)
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


def _extract_outline_sections(content: str) -> list[tuple[str, str, str]]:
    sections: list[tuple[str, str, str]] = []
    pattern = re.compile(r"\s*(\d+)\.\s+(.+?)\s*[—–-]\s*([^\n\r]+?)(?=\s*\d+\.|\s*$)")
    for match in pattern.finditer(content):
        sections.append((match.group(1), match.group(2).strip(), match.group(3).strip()))
    return sections


@dataclass
class TrimConfig:
    width: float = DEFAULT_TRIM[0]
    height: float = DEFAULT_TRIM[1]
    margins: list[float] = field(default_factory=lambda: list(DEFAULT_MARGINS))
    bleed: float = DEFAULT_BLEED


@dataclass
class Chapter:
    number: str
    title: str
    status_note: str
    theme: str
    layout: str
    lore_entries: list[dict[str, Any]] = field(default_factory=list)
    presentation_media: list[dict[str, Any]] = field(default_factory=list)
    other_media: list[dict[str, Any]] = field(default_factory=list)
    background_url: str | None = None


@dataclass
class Book:
    title: str
    subtitle: str
    edition_year: int
    status: str
    generated_date: str
    config: TrimConfig
    heraldry_src: str | None
    visual_gaps: list[dict[str, Any]]
    front_matter: list[str]
    chapters: list[Chapter]
    assets_dir: Path
    project_dir: Path
    default_theme: str = DEFAULT_THEME
    theme_backgrounds: dict[str, str | None] = field(default_factory=dict)


def _resolve_config(edition: dict[str, Any]) -> TrimConfig:
    return TrimConfig(
        width=float(edition.get("trim_width_in", DEFAULT_TRIM[0])),
        height=float(edition.get("trim_height_in", DEFAULT_TRIM[1])),
        margins=[float(x) for x in edition.get("safe_margins_in", DEFAULT_MARGINS)],
        bleed=float(edition.get("bleed_in", DEFAULT_BLEED)),
    )


def _resolve_visual_themes(edition: dict[str, Any]) -> dict[str, dict[str, Any]]:
    declared = edition.get("visual_themes") or {}
    if not declared:
        return {DEFAULT_THEME: {"background_media_id": None}}
    return {str(k): v or {} for k, v in declared.items()}


def _resolve_theme_background(
    theme_id: str,
    theme_config: dict[str, Any],
    record: dict[str, Any] | None,
    media_entries: list[dict[str, Any]],
    project_dir: Path,
    assets_dir: Path,
) -> str | None:
    media_id = record.get("background_media_id") if record else None
    if not media_id:
        media_id = (theme_config or {}).get("background_media_id")
    if not media_id:
        return None
    media = find_object(media_entries, id=media_id)
    if not media:
        print(f"Warning: background media {media_id} not found for theme {theme_id}", file=sys.stderr)
        return None
    return copy_media_asset(media, project_dir, assets_dir)


def _choose_lore(
    section_title: str,
    record: dict[str, Any] | None,
    edition: dict[str, Any],
    lore_entries: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ids = (record or {}).get("source_lore_ids") or []
    if source_ids:
        chosen = [find_object(lore_entries, id=lid) for lid in source_ids]
        return [l for l in chosen if l]

    edition_ids = edition.get("included_lore_ids") or []
    if edition_ids:
        pool = [l for l in lore_entries if l.get("id") in edition_ids]
    else:
        pool = list(lore_entries)

    scored = [(score, l) for l in lore_entries if (score := _lore_score(section_title, l.get("title", ""))) > 0]
    scored.sort(key=lambda x: x[0], reverse=True)
    matched: list[dict[str, Any]] = []
    for _, l in scored[:4]:
        matched.append(l)
    if not matched:
        print(f"Warning: no lore assigned to section '{section_title}' (inference fallback)", file=sys.stderr)
    return matched


def _choose_media(
    section_title: str,
    record: dict[str, Any] | None,
    edition: dict[str, Any],
    media_entries: list[dict[str, Any]],
    lore_entries: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ids = (record or {}).get("source_media_ids") or []
    if source_ids:
        chosen = [find_object(media_entries, id=mid) for mid in source_ids]
        return [m for m in chosen if m]

    edition_ids = edition.get("included_media_ids") or []
    if edition_ids:
        pool = [m for m in media_entries if m.get("id") in edition_ids]
    else:
        pool = list(media_entries)

    lore_titles = [l.get("title", "") for l in lore_entries]
    scored = []
    for m in pool:
        score = _media_score(section_title, lore_titles, m)
        if score > 0:
            scored.append((score, m))
    scored.sort(key=lambda x: x[0], reverse=True)
    if not scored:
        print(f"Warning: no media assigned to section '{section_title}' (inference fallback)", file=sys.stderr)
        return []
    return [m for _, m in scored[:1]]


def _prepare_media(
    chosen: list[dict[str, Any]],
    project_dir: Path,
    assets_dir: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    presentation = []
    other = []
    for media in chosen:
        if media.get("lore_book_presentation"):
            presentation.append(media)
        else:
            other.append(media)
    for media in presentation + other:
        copy_media_asset(media, project_dir, assets_dir)
    return presentation, other


def load_project(
    life_dir: Path,
    project: str = DEFAULT_PROJECT,
    edition_year: int | None = None,
    edition_id: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[str, Any]]]:
    project_dir = life_dir / "domains" / DEFAULT_DOMAIN / project
    book_dir = project_dir / "lore-book"

    # Load the master outline and all section records from the lore-book tree.
    # Edition-specific records (e.g. 2026/lore-book-section-13.md) are found
    # recursively under the project lore-book directory.
    section_records = load_objects(book_dir)
    editions = [s for s in section_records if s.get("schema") == "hobby.lore-book-edition"]

    edition: dict[str, Any] | None = None
    if edition_id:
        edition = find_object(editions, id=edition_id)
    if not edition and edition_year:
        edition = find_object(editions, id=f"lb-edition-{edition_year}")
    if not edition and editions:
        edition = editions[0]
    if not edition:
        from datetime import datetime
        edition = {
            "id": f"lb-edition-{edition_year or datetime.now().year}",
            "title": f"{project} Lore Book",
            "edition_year": edition_year or datetime.now().year,
            "subtitle": "Draft",
            "edition_status": "draft",
            "generated_date": datetime.now().strftime("%Y-%m-%d"),
            "visual_gaps": [],
        }

    outline = find_object(section_records, schema="hobby.lore-book-section", section_number="0") or {}
    section_map = {s.get("section_number"): s for s in section_records if s.get("schema") == "hobby.lore-book-section"}

    lore_entries = load_objects(project_dir / "lore")
    media_entries = load_objects(project_dir / "media")

    return edition, outline, lore_entries, media_entries, section_map


def assemble_book(
    edition: dict[str, Any],
    outline: dict[str, Any],
    lore_entries: list[dict[str, Any]],
    media_entries: list[dict[str, Any]],
    section_map: dict[str, dict[str, Any]],
    project_dir: Path,
    assets_dir: Path,
) -> Book:
    from datetime import datetime

    title = edition.get("title", "Hobby Lore Book")
    subtitle = edition.get("subtitle", "")
    edition_year = edition.get("edition_year", datetime.now().year)
    status = edition.get("edition_status", "draft")
    generated_date = edition.get("generated_date", datetime.now().strftime("%Y-%m-%d"))
    config = _resolve_config(edition)
    front_matter = list(edition.get("front_matter_order", ["cover", "title", "toc"]))
    visual_gaps = edition.get("visual_gaps") or []
    visual_themes = _resolve_visual_themes(edition)
    default_theme = edition.get("default_visual_theme", DEFAULT_THEME)

    assets_dir.mkdir(parents=True, exist_ok=True)

    heraldry = find_object(media_entries, media_type="heraldry", canon_status="canonical")
    heraldry_src = copy_media_asset(heraldry, project_dir, assets_dir) if heraldry else None

    # resolve theme backgrounds deterministically from manifest
    theme_backgrounds: dict[str, str | None] = {}
    for theme_id, theme_config in visual_themes.items():
        theme_backgrounds[theme_id] = _resolve_theme_background(
            theme_id, theme_config, None, media_entries, project_dir, assets_dir
        )

    outline_items = _extract_outline_sections(outline.get("content", ""))
    included_ids = set(edition.get("included_section_ids") or [])
    chapters: list[Chapter] = []
    assigned_lore: set[str] = set()
    assigned_media: set[str] = set()

    for num, sec_title, status_note in outline_items:
        # Front matter numbers 1-4 are not body sections.
        try:
            n = int(num)
        except ValueError:
            n = 0
        if n < 5:
            continue

        record = section_map.get(num)
        if record and included_ids and record.get("id") not in included_ids:
            continue

        theme = (record or {}).get("theme", default_theme)
        layout = (record or {}).get("page_layout", "text")
        if theme not in visual_themes:
            theme = default_theme

        if record and record.get("source_lore_ids"):
            source_lore = _choose_lore(sec_title, record, edition, lore_entries)
        else:
            source_lore = _choose_lore(sec_title, None, edition, lore_entries)

        if record and record.get("source_media_ids"):
            source_media = [find_object(media_entries, id=mid) for mid in record["source_media_ids"]]
            source_media = [m for m in source_media if m]
            if not source_media:
                source_media = _choose_media(sec_title, record, edition, media_entries, source_lore)
        else:
            source_media = _choose_media(sec_title, None, edition, media_entries, source_lore)

        for l in source_lore:
            assigned_lore.add(l.get("id"))
        for m in source_media:
            assigned_media.add(m.get("id"))

        presentation, other = _prepare_media(source_media, project_dir, assets_dir)
        background_url = _resolve_theme_background(
            theme, visual_themes.get(theme, {}), record, media_entries, project_dir, assets_dir
        )

        chapters.append(Chapter(
            number=num,
            title=sec_title,
            status_note=status_note,
            theme=theme,
            layout=layout,
            lore_entries=source_lore,
            presentation_media=presentation,
            other_media=other,
            background_url=background_url,
        ))

    return Book(
        title=title,
        subtitle=subtitle,
        edition_year=edition_year,
        status=status,
        generated_date=generated_date,
        config=config,
        heraldry_src=heraldry_src,
        visual_gaps=visual_gaps,
        front_matter=front_matter,
        chapters=chapters,
        assets_dir=assets_dir,
        project_dir=project_dir,
        default_theme=default_theme,
        theme_backgrounds=theme_backgrounds,
    )
