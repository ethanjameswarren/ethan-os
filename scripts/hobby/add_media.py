#!/usr/bin/env python3
"""
Ingest an image into a Necron (or general hobby) project as a `hobby.media` record.

Copies the original file into the project's assets directory without modifying it,
then writes a `hobby.media` Markdown metadata record in the project's media/ folder.
"""

from __future__ import annotations

import argparse
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^\w\s-]", "", value)
    return re.sub(r"[-\s]+", "-", value).strip("-")


def _comma_list(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def main():
    parser = argparse.ArgumentParser(description="Ingest a hobby image into the media system.")
    parser.add_argument("--life-dir", type=Path, help="Path to ethan-life repository root.")
    parser.add_argument("--project", default="warhammer-40k-necron-dynasty", help="Hobby project slug.")
    parser.add_argument("--image", required=True, type=Path, help="Path to the image file to ingest.")
    parser.add_argument("--media-type", default="reference_image", help="hobby.media media_type value.")
    parser.add_argument("--title", help="Media record title; defaults to filename base.")
    parser.add_argument("--subject", help="Subject/unit/character/location.")
    parser.add_argument("--caption", help="Image caption.")
    parser.add_argument("--creator", help="Artist, photographer, or generator tool.")
    parser.add_argument("--generated-by", help="Model/tool used if generated.")
    parser.add_argument("--is-generated", action="store_true", help="Flag if image is AI/generated.")
    parser.add_argument("--tags", help="Comma-separated tags (e.g., concept-art,destroyer-cult).")
    parser.add_argument("--faction", default="pale-crown", help="Faction/dynasty shown.")
    parser.add_argument("--unit-type", help="Unit or model type shown.")
    parser.add_argument("--color-scheme", help="Dominant color scheme (e.g., black-silver-cyan).")
    parser.add_argument("--energy-color", help="Glow/energy color (e.g., cyan, red, purple).")
    parser.add_argument("--associated-lore-concept", help="Short lore concept label.")
    parser.add_argument("--canon-status", default="reference", choices=["canonical", "candidate", "reference", "unverified"])
    parser.add_argument("--related-lore-ids", help="Comma-separated lore IDs.")
    parser.add_argument("--related-collection-ids", help="Comma-separated collection item IDs.")
    parser.add_argument("--related-narrative-ids", help="Comma-separated narrative IDs.")
    parser.add_argument("--print-suitability", default="not_print_ready", help="print_suitability value.")
    parser.add_argument("--orientation", choices=["landscape", "portrait", "square"])
    parser.add_argument("--rights", help="Rights/provenance note.")
    parser.add_argument("--dry-run", action="store_true", help="Preview actions without writing files.")
    args = parser.parse_args()

    life_dir = args.life_dir
    if not life_dir:
        life_dir = Path(__file__).resolve().parents[3] / "ethan-life"
    life_dir = Path(life_dir)

    project_dir = life_dir / "domains" / "hobby" / args.project
    media_dir = project_dir / "media"
    assets_type_dir = media_dir / "assets" / args.media_type.replace("_", "-")

    image_path = Path(args.image).resolve()
    if not image_path.exists():
        raise SystemExit(f"Image not found: {image_path}")

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    title = args.title or image_path.stem.replace("_", " ").replace("-", " ").title()
    media_id = f"media-{timestamp}-{_slugify(title)}"
    ext = image_path.suffix.lower()
    dest_filename = f"{media_id}{ext}"
    dest_path = assets_type_dir / dest_filename
    relative_asset_path = dest_path.relative_to(project_dir).as_posix()

    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    frontmatter: dict[str, Any] = {
        "id": media_id,
        "schema": "hobby.media",
        "schema_version": 1,
        "title": title,
        "created_at": created_at,
        "updated_at": created_at,
        "provenance": {
            "type": "user_action",
            "source": str(image_path),
            "description": f"Ingested from {image_path.name} by add_media.py",
        },
        "media_type": args.media_type,
        "status": "available",
        "file_path": relative_asset_path,
        "subject": args.subject or title,
        "caption": args.caption or "",
        "tags": _comma_list(args.tags),
        "faction": args.faction,
        "unit_type": args.unit_type,
        "color_scheme": args.color_scheme,
        "energy_color": args.energy_color,
        "associated_lore_concept": args.associated_lore_concept,
        "canon_status": args.canon_status,
        "related_lore_ids": _comma_list(args.related_lore_ids),
        "related_collection_item_ids": _comma_list(args.related_collection_ids),
        "related_narrative_ids": _comma_list(args.related_narrative_ids),
        "creator": args.creator or "unknown",
        "is_generated": args.is_generated,
        "print_suitability": args.print_suitability,
        "orientation": args.orientation or "portrait",
        "rights_or_provenance": args.rights or f"Original file: {image_path.name}",
    }

    if args.generated_by:
        frontmatter["generated_by"] = args.generated_by

    # Remove empty optional fields to keep records tidy
    for key in list(frontmatter.keys()):
        if frontmatter[key] in (None, "", [], {}):
            frontmatter.pop(key)

    md_path = media_dir / f"{media_id}.md"

    if args.dry_run:
        print("[dry-run] Would copy:")
        print(f"  {image_path} -> {dest_path}")
        print(f"[dry-run] Would write: {md_path}")
        print(f"[dry-run] Media ID: {media_id}")
        return

    assets_type_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(image_path, dest_path)

    import yaml

    body = f"""# {title}

![{title}]({relative_asset_path})

{args.caption or ""}

**Source file:** `{image_path.name}`
**Ingested:** {created_at}
"""

    md_content = "---\n" + yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True) + "---\n\n" + body
    md_path.write_text(md_content, encoding="utf-8")

    print(f"Ingested media: {media_id}")
    print(f"  Asset: {dest_path}")
    print(f"  Record: {md_path}")


if __name__ == "__main__":
    main()
