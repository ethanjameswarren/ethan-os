"""Publication data loading and canonical content routing for the lore book."""
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
    collection_items: list[dict[str, Any]] = field(default_factory=list)
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
    warnings: list[str] = field(default_factory=list)


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


def _find_default_background(
    theme_id: str,
    assets_dir: Path,
    project_dir: Path,
) -> str | None:
    for filename in [f"{theme_id}-background.png", "background.png"]:
        candidate = assets_dir / filename
        if candidate.exists():
            return f"assets/{filename}"
    media_candidate = project_dir / "media" / "assets" / "page-decoration" / f"{theme_id}-background.png"
    if media_candidate.exists():
        assets_dir.mkdir(parents=True, exist_ok=True)
        dest = assets_dir / media_candidate.name
        shutil.copy2(media_candidate, dest)
        return f"assets/{media_candidate.name}"
    return None


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
        return None
    return copy_media_asset(media, project_dir, assets_dir)


# Canonical routing metadata. Sections without explicit source_*_ids use these rules.
# A section matches a lore entry by title keyword (first pass) or by lore_type (second pass).
SECTION_CONTENT_RULES: list[dict[str, Any]] = [
    {"number": "5", "title_keywords": ["identity", "reputation", "dynasty", "glance"], "lore_types": {"identity", "doctrine"}},
    {"number": "6", "title_keywords": ["pre-biotransference", "mortality", "biotransference", "culture"], "lore_types": {"history", "philosophy", "culture"}},
    {"number": "7", "title_keywords": ["c'tan aftermath", "great sleep", "awakening", "silent king", "aftermath"], "lore_types": {"history", "technology"}},
    {"number": "8", "title_keywords": ["philosophy", "failure", "accountability", "dominion", "indulgence", "biotransference and philosophy"], "lore_types": {"philosophy"}},
    {"number": "9", "title_keywords": ["visual"], "lore_types": {"visual_language"}},
    {"number": "11", "title_keywords": ["doctrine", "retreat", "zero-loss", "tabletop"], "lore_types": {"doctrine"}},
    {"number": "12", "title_keywords": ["jahrekt", "cyan", "ruler", "court", "arrival", "flayed"], "lore_types": {"identity", "organization", "character", "culture"}},
    {"number": "13", "title_keywords": ["destroyer", "curse", "red"], "lore_types": {"doctrine", "character", "culture"}},
    {"number": "14", "title_keywords": ["c'tan", "dominion", "purple", "void dragon"], "lore_types": {"technology", "philosophy"}},
    {"number": "15", "title_keywords": ["hierarchy", "command", "structure", "ruler", "court"], "lore_types": {"organization", "character"}},
    {"number": "16", "title_keywords": ["ruler", "lord", "court", "character"], "lore_types": {"character"}},
    {"number": "17", "title_keywords": ["unit", "formation", "warrior", "destroyer", "immortal"], "lore_types": {"unit", "doctrine"}},
    {"number": "18", "title_keywords": ["relic", "artifact", "c'tan", "void dragon", "monolith"], "lore_types": {"technology"}},
    {"number": "19", "title_keywords": ["tomb world", "territory", "world", "location"], "lore_types": {"territory"}},
    {"number": "20", "title_keywords": ["timeline", "great sleep", "awakening", "biotransference"], "lore_types": {"history"}},
    {"number": "23", "title_keywords": ["appendix", "faction", "deprecated", "relations"], "lore_types": {"faction_relations", "other", "doctrine"}},
]


def _title_matches(title: str, keywords: list[str]) -> bool:
    lower = title.lower()
    return any(kw.lower() in lower for kw in keywords)


def _route_lore(
    section_number: str,
    section_title: str,
    record: dict[str, Any] | None,
    edition: dict[str, Any],
    lore_entries: list[dict[str, Any]],
    already_assigned: set[str],
    warnings: list[str],
) -> list[dict[str, Any]]:
    explicit = (record or {}).get("source_lore_ids") or []
    if explicit:
        chosen = [find_object(lore_entries, id=lid) for lid in explicit]
        chosen = [l for l in chosen if l]
        for l in chosen:
            lid = l.get("id")
            if lid in already_assigned:
                warnings.append(f"Lore entry '{lid}' explicitly assigned to multiple sections (latest: {section_number})")
        return chosen

    edition_ids = set(edition.get("included_lore_ids") or [])
    pool = [l for l in lore_entries if not edition_ids or l.get("id") in edition_ids]

    matched: list[dict[str, Any]] = []
    assigned_here: set[str] = set()

    # First pass: assign by title keyword.
    for l in pool:
        if l.get("id") in already_assigned:
            continue
        for rule in SECTION_CONTENT_RULES:
            if rule["number"] != section_number:
                continue
            if _title_matches(str(l.get("title", "")), rule["title_keywords"]):
                matched.append(l)
                assigned_here.add(l.get("id"))
                break

    # Second pass: assign by lore_type for entries not yet placed.
    for l in pool:
        lid = l.get("id")
        if lid in already_assigned or lid in assigned_here:
            continue
        for rule in SECTION_CONTENT_RULES:
            if rule["number"] != section_number:
                continue
            if str(l.get("lore_type", "")) in rule["lore_types"]:
                matched.append(l)
                assigned_here.add(lid)
                break

    return matched


def _route_media(
    section_number: str,
    section_title: str,
    record: dict[str, Any] | None,
    media_entries: list[dict[str, Any]],
    already_assigned: set[str],
    warnings: list[str],
) -> list[dict[str, Any]]:
    explicit = (record or {}).get("source_media_ids") or []
    if explicit:
        chosen = [find_object(media_entries, id=mid) for mid in explicit]
        chosen = [m for m in chosen if m]
        for m in chosen:
            mid = m.get("id")
            if mid in already_assigned:
                warnings.append(f"Media '{mid}' explicitly assigned to multiple sections (latest: {section_number})")
        return chosen

    chosen: list[dict[str, Any]] = []
    for m in media_entries:
        mid = m.get("id")
        if mid in already_assigned:
            continue
        if str(m.get("lore_book_section_id")) == section_number:
            chosen.append(m)
            continue
        if str(m.get("media_type")) == "heraldry" and section_number == "10":
            chosen.append(m)
            continue
        if str(m.get("media_type")) in ("reference_image", "concept_art", "generated_art") and section_number == "22":
            chosen.append(m)
            continue
    return chosen


def _route_collection_items(
    section_number: str,
    record: dict[str, Any] | None,
    collection_items: list[dict[str, Any]],
    already_assigned: set[str],
    warnings: list[str],
) -> list[dict[str, Any]]:
    explicit = (record or {}).get("source_collection_item_ids") or []
    if explicit:
        chosen = [c for c in collection_items if c.get("id") in explicit]
        for c in chosen:
            cid = c.get("id")
            if cid in already_assigned:
                warnings.append(f"Collection item '{cid}' explicitly assigned to multiple sections (latest: {section_number})")
        return chosen

    if section_number != "17":
        return []

    chosen = []
    for c in collection_items:
        cid = c.get("id")
        if cid in already_assigned:
            continue
        if str(c.get("item_type")) in ("unit", "miniature"):
            chosen.append(c)
    return chosen


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

    collection_items = load_objects(project_dir / "collection")

    heraldry = find_object(media_entries, media_type="heraldry", canon_status="canonical")
    heraldry_src = copy_media_asset(heraldry, project_dir, assets_dir) if heraldry else None

    theme_backgrounds: dict[str, str | None] = {}
    for theme_id, theme_config in visual_themes.items():
        theme_backgrounds[theme_id] = _resolve_theme_background(
            theme_id, theme_config, None, media_entries, project_dir, assets_dir
        ) or _find_default_background(theme_id, assets_dir, project_dir)

    outline_items = _extract_outline_sections(outline.get("content", ""))
    included_ids = set(edition.get("included_section_ids") or [])
    chapters: list[Chapter] = []
    warnings: list[str] = []
    assigned_lore: set[str] = set()
    assigned_media: set[str] = set()
    assigned_collection: set[str] = set()

    for num, sec_title, status_note in outline_items:
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

        source_lore = _route_lore(num, sec_title, record, edition, lore_entries, assigned_lore, warnings)
        source_media = _route_media(num, sec_title, record, media_entries, assigned_media, warnings)
        source_collection = _route_collection_items(num, record, collection_items, assigned_collection, warnings)

        for l in source_lore:
            assigned_lore.add(l.get("id"))
        for m in source_media:
            assigned_media.add(m.get("id"))
        for c in source_collection:
            assigned_collection.add(c.get("id"))

        presentation, other = _prepare_media(source_media, project_dir, assets_dir)
        section_bg = _resolve_theme_background(
            theme, visual_themes.get(theme, {}), record, media_entries, project_dir, assets_dir
        )
        background_url = section_bg or theme_backgrounds.get(theme) or _find_default_background(theme, assets_dir, project_dir)

        if layout in ("full_bleed_image", "two_page_spread", "image_left", "image_right", "diagram", "comic", "gallery"):
            pass
        elif record and record.get("page_layout") == "editorial-profile":
            layout = "editorial-profile"
        elif presentation:
            layout = "editorial-profile"

        chapters.append(Chapter(
            number=num,
            title=sec_title,
            status_note=status_note,
            theme=theme,
            layout=layout,
            lore_entries=source_lore,
            presentation_media=presentation,
            other_media=other,
            collection_items=source_collection,
            background_url=background_url,
        ))

    # Detect entries that should be in a section but were not routed because no section matched.
    edition_lore_ids = set(edition.get("included_lore_ids") or [l.get("id") for l in lore_entries])
    for l in lore_entries:
        if l.get("id") in edition_lore_ids and l.get("id") not in assigned_lore:
            warnings.append(f"Lore entry '{l.get('id')}' ({l.get('title')}) was not assigned to any section")

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
        warnings=warnings,
    )
