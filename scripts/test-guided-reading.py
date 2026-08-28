#!/usr/bin/env python3
"""
Guided Reading deterministic tests for Ethan OS.

Checks:
- reading-state.yaml is well-formed and matches its declared version
- each active book resolves to an existing knowledge.source
- current_page is authoritative only in reading-state.yaml, not duplicated in source
- spoiler_boundary matches current_page (the highest explicitly completed page)
- last_completed_range end equals current_page
- last_session_id resolves to an existing knowledge.reading-session
- reading-profiles resolve to existing sources and are unique per source
- spoiler_policy is explicit and not inferred solely from familiarity
- source_access/page_alignment are consistent
- retention-state.yaml is well-formed
- retention items reference existing session insights or ideas
- spaced-review interval_index is within the declared schedule
- archived/paused items are not scheduled with a due date unless explicitly retained
"""

import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "config" / "demo-personality" / "fixtures"
ETHAN_LIFE = ROOT.parent / "ethan-life"
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, text
    return yaml.safe_load(match.group(1)), text


def load_objects(folder: Path):
    objects = {}
    if not folder.exists():
        return objects
    for path in folder.rglob("*.md"):
        if path.name == "README.md":
            continue
        fm, _ = parse_frontmatter(path)
        if fm and "id" in fm:
            objects[fm["id"]] = fm
    return objects


def load_reading_state(path: Path):
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


VALID_STATUSES = {"unread", "reading", "paused", "finished", "abandoned", "reference"}
VALID_OWNERSHIP = {"owned_physical", "owned_digital", "borrowed", "wishlist", "not_owned", "unknown"}
VALID_FORMATS = {"hardcover", "paperback", "ebook", "audiobook", "pdf", "epub", "other"}


def validate_library(sources: dict, label: str, broken: list):
    for sid, source in sources.items():
        if source.get("source_type") != "book":
            continue
        prefix = f"{label} source {sid}"
        status = source.get("status")
        if status and status not in VALID_STATUSES:
            broken.append(f"{prefix}: invalid status '{status}'")
        ownership = source.get("ownership_status")
        if ownership and ownership not in VALID_OWNERSHIP:
            broken.append(f"{prefix}: invalid ownership_status '{ownership}'")
        fmt = source.get("format")
        if fmt and fmt not in VALID_FORMATS:
            broken.append(f"{prefix}: invalid format '{fmt}'")
        tags = source.get("tags")
        if tags is not None and not isinstance(tags, list):
            broken.append(f"{prefix}: tags is not a list")
        year = source.get("publication_year")
        if year is not None and not isinstance(year, int):
            broken.append(f"{prefix}: publication_year must be an integer")
        notes = source.get("user_interest_notes")
        if notes is not None and not isinstance(notes, list):
            broken.append(f"{prefix}: user_interest_notes is not a list")


def validate_reading_state(state: dict, sources: dict, sessions: dict, label: str, broken: list):
    if not isinstance(state, dict):
        broken.append(f"{label}: reading-state.yaml is not a mapping")
        return

    version = state.get("version")
    if version != 1:
        broken.append(f"{label}: expected version 1, got {version}")

    active_books = state.get("active_books", [])
    if not isinstance(active_books, list):
        broken.append(f"{label}: active_books is not a list")
        return

    for idx, entry in enumerate(active_books):
        prefix = f"{label} active_books[{idx}]"
        source_id = entry.get("source_id")
        if not source_id:
            broken.append(f"{prefix}: missing source_id")
            continue
        if source_id not in sources:
            broken.append(f"{prefix}: source_id '{source_id}' not found")
            continue

        source = sources[source_id]
        # Authoritative current_page lives in reading-state only
        if "current_page" in source:
            broken.append(
                f"{prefix}: source '{source_id}' contains current_page; authority belongs to reading-state.yaml"
            )

        current_page = entry.get("current_page")
        last_range = entry.get("last_completed_range") or {}
        if isinstance(last_range, dict):
            range_end = last_range.get("end")
            if range_end is not None and current_page is not None and range_end != current_page:
                broken.append(
                    f"{prefix}: current_page ({current_page}) does not match last_completed_range.end ({range_end})"
                )

        spoiler_boundary = entry.get("spoiler_boundary")
        if spoiler_boundary is not None and current_page is not None and spoiler_boundary != current_page:
            broken.append(
                f"{prefix}: spoiler_boundary ({spoiler_boundary}) should equal current_page ({current_page})"
            )

        last_session_id = entry.get("last_session_id")
        if last_session_id and last_session_id not in sessions:
            broken.append(f"{prefix}: last_session_id '{last_session_id}' not found")

        session = sessions.get(last_session_id) if last_session_id else None
        if session:
            pages = session.get("pages") or {}
            session_end = pages.get("end")
            if session_end is not None and current_page is not None and session_end != current_page:
                broken.append(
                    f"{prefix}: current_page ({current_page}) does not match last session pages.end ({session_end})"
                )

    queue = state.get("reading_queue", [])
    if not isinstance(queue, list):
        broken.append(f"{label}: reading_queue is not a list")
    else:
        seen_positions = set()
        for idx, entry in enumerate(queue):
            prefix = f"{label} reading_queue[{idx}]"
            source_id = entry.get("source_id")
            if not source_id:
                broken.append(f"{prefix}: missing source_id")
                continue
            if source_id not in sources:
                broken.append(f"{prefix}: source_id '{source_id}' not found")
                continue
            pos = entry.get("queue_position")
            if pos is None or not isinstance(pos, int) or pos < 1:
                broken.append(f"{prefix}: queue_position must be a positive integer")
            elif pos in seen_positions:
                broken.append(f"{prefix}: duplicate queue_position {pos}")
            else:
                seen_positions.add(pos)
            status = entry.get("status")
            if status and status not in {"queued", "next_up", "recommended", "removed"}:
                broken.append(f"{prefix}: invalid queue status '{status}'")


def validate_reading_profiles(profiles: dict, sources: dict, label: str, broken: list):
    seen_sources = set()
    for pid, profile in profiles.items():
        prefix = f"{label} profile {pid}"
        source_id = profile.get("source_id")
        if not source_id:
            broken.append(f"{prefix}: missing source_id")
            continue
        if source_id not in sources:
            broken.append(f"{prefix}: source_id '{source_id}' not found")
            continue
        if source_id in seen_sources:
            broken.append(f"{prefix}: duplicate reading profile for source '{source_id}'")
        seen_sources.add(source_id)

        spoiler_policy = profile.get("spoiler_policy")
        # A profile should explicitly state spoiler_policy; if missing, flag it.
        if not spoiler_policy:
            broken.append(
                f"{prefix}: spoiler_policy must be explicit (familiarity does not imply spoiler permission)"
            )

        source_access = profile.get("source_access")
        if not source_access:
            broken.append(f"{prefix}: source_access must be set")
            continue

        if source_access == "full_text_available":
            if profile.get("ingestion_status") != "complete":
                broken.append(
                    f"{prefix}: full_text_available requires ingestion_status=complete"
                )
            if not profile.get("content_locator"):
                broken.append(
                    f"{prefix}: full_text_available requires content_locator"
                )
            if not profile.get("page_alignment"):
                broken.append(
                    f"{prefix}: full_text_available requires page_alignment"
                )
            if not profile.get("source_provenance"):
                broken.append(
                    f"{prefix}: full_text_available requires source_provenance"
                )
        elif source_access in ("metadata_only", "model_knowledge"):
            # page_alignment should be unknown when no digital text is aligned
            alignment = profile.get("page_alignment")
            if alignment and alignment not in ("unknown", "approximate"):
                broken.append(
                    f"{prefix}: source_access={source_access} should have page_alignment=unknown/approximate, got {alignment}"
                )


def validate_retention_state(state: dict, sessions: dict, ideas: dict, label: str, broken: list):
    if not isinstance(state, dict):
        broken.append(f"{label}: retention-state.yaml is not a mapping")
        return

    version = state.get("version")
    if version != 1:
        broken.append(f"{label}: expected retention-state version 1, got {version}")

    intervals = [1, 3, 7, 14, 30, 60, 120]
    max_index = len(intervals) - 1
    seen_item_ids = set()

    items = state.get("retention_items", [])
    if not isinstance(items, list):
        broken.append(f"{label}: retention_items is not a list")
        return

    for idx, item in enumerate(items):
        prefix = f"{label} retention_items[{idx}]"
        item_id = item.get("item_id")
        if not item_id:
            broken.append(f"{prefix}: missing item_id")
            continue
        if item_id in seen_item_ids:
            broken.append(f"{prefix}: duplicate item_id '{item_id}'")
        seen_item_ids.add(item_id)

        source_type = item.get("source_type")
        source_id = item.get("source_id")
        insight_id = item.get("insight_id")
        if source_type == "session_insight":
            if source_id not in sessions:
                broken.append(f"{prefix}: session source_id '{source_id}' not found")
            elif insight_id:
                session = sessions[source_id]
                insight_ids = {
                    i.get("insight_id")
                    for i in session.get("extracted_insights", [])
                    if i.get("insight_id")
                }
                if insight_id not in insight_ids:
                    broken.append(
                        f"{prefix}: insight_id '{insight_id}' not found in session '{source_id}'"
                    )
        elif source_type == "idea":
            if source_id not in ideas:
                broken.append(f"{prefix}: idea source_id '{source_id}' not found")
        else:
            broken.append(f"{prefix}: unknown source_type '{source_type}'")

        interval_index = item.get("interval_index")
        if interval_index is not None and (not isinstance(interval_index, int) or interval_index < 0 or interval_index > max_index):
            broken.append(
                f"{prefix}: interval_index {interval_index} out of range [0, {max_index}]"
            )

        status = item.get("status")
        if status == "archived" and item.get("next_review_due_at"):
            broken.append(
                f"{prefix}: archived item should not have a next_review_due_at"
            )


def main():
    print("Guided Reading deterministic tests")
    print("=" * 40)

    broken = []

    # Demo fixtures
    demo_sources = load_objects(FIXTURES / "domains" / "knowledge" / "sources")
    demo_sessions = load_objects(FIXTURES / "domains" / "knowledge" / "reading-sessions")
    demo_ideas = load_objects(FIXTURES / "domains" / "knowledge" / "ideas")
    demo_profiles = load_objects(FIXTURES / "domains" / "knowledge" / "reading-profiles")
    demo_state_path = FIXTURES / "domains" / "knowledge" / "reading-state.yaml"
    demo_state = load_reading_state(demo_state_path)
    if demo_state is None:
        broken.append(f"Demo reading-state not found: {demo_state_path}")
    else:
        validate_reading_state(demo_state, demo_sources, demo_sessions, "demo", broken)
    validate_reading_profiles(demo_profiles, demo_sources, "demo", broken)
    validate_library(demo_sources, "demo", broken)
    demo_retention_path = FIXTURES / "domains" / "knowledge" / "retention-state.yaml"
    demo_retention = load_reading_state(demo_retention_path)
    if demo_retention is None:
        broken.append(f"Demo retention-state not found: {demo_retention_path}")
    else:
        validate_retention_state(demo_retention, demo_sessions, demo_ideas, "demo", broken)

    # Canonical ethan-life state (may be empty)
    life_sources = load_objects(ETHAN_LIFE / "domains" / "knowledge" / "sources")
    life_sessions = load_objects(ETHAN_LIFE / "domains" / "knowledge" / "reading-sessions")
    life_ideas = load_objects(ETHAN_LIFE / "domains" / "knowledge" / "ideas")
    life_profiles = load_objects(ETHAN_LIFE / "domains" / "knowledge" / "reading-profiles")
    life_state_path = ETHAN_LIFE / "domains" / "knowledge" / "reading-state.yaml"
    life_state = load_reading_state(life_state_path)
    if life_state is None:
        broken.append(f"Canonical reading-state not found: {life_state_path}")
    else:
        validate_reading_state(life_state, life_sources, life_sessions, "ethan-life", broken)
    validate_reading_profiles(life_profiles, life_sources, "ethan-life", broken)
    validate_library(life_sources, "ethan-life", broken)
    life_retention_path = ETHAN_LIFE / "domains" / "knowledge" / "retention-state.yaml"
    life_retention = load_reading_state(life_retention_path)
    if life_retention is None:
        broken.append(f"Canonical retention-state not found: {life_retention_path}")
    else:
        validate_retention_state(life_retention, life_sessions, life_ideas, "ethan-life", broken)

    print(f"Checked {len(demo_sources) + len(life_sources)} sources, "
          f"{len(demo_sessions) + len(life_sessions)} sessions, "
          f"{len(demo_ideas) + len(life_ideas)} ideas, "
          f"{len(demo_profiles) + len(life_profiles)} profiles, "
          f"2 reading states, 2 retention states")

    if broken:
        print(f"\nFAILURES ({len(broken)}):")
        for item in broken:
            print(f"  - {item}")
        sys.exit(1)
    else:
        print("\nAll Guided Reading checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
