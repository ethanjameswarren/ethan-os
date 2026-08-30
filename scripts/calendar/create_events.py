#!/usr/bin/env python3
"""
Create Google Calendar events from an Ethan OS weekly plan.

Usage:
  python create_events.py path/to/weekly-plan-YYYY-MM-DD.md [--calendar primary]

Requires GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, and GOOGLE_REFRESH_TOKEN to be
set in the environment. Obtain the refresh token by running scripts/calendar/auth.py
once after creating a Google Cloud OAuth client.

By default, only blocks sourced from a goal or with labels containing "Career" or
"Wealth" are exported. Set --all to export every block (work/commute/sleep are
usually redundant with an existing calendar).
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml

import client


def _extract_frontmatter(text: str) -> dict:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        raise ValueError("No YAML frontmatter found in weekly plan.")
    return yaml.safe_load(match.group(1))


def _to_iso_datetime(date_str: str, time_str: str):
    """Return an ISO 8601 string in the local system timezone."""
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    # Attach local timezone offset so Google Calendar displays the intended wall-clock time.
    local_tz = datetime.now().astimezone().tzinfo
    return dt.replace(tzinfo=local_tz).isoformat()


def _should_export(block: dict, all_blocks: bool) -> bool:
    if all_blocks:
        return True
    source = block.get("source", "")
    label = block.get("label", "")
    return (
        source == "goal"
        or "Career" in label
        or "Wealth" in label
        or "review" in label.lower()
    )


def main():
    parser = argparse.ArgumentParser(description="Create Google Calendar events from a weekly plan.")
    parser.add_argument("weekly_plan", type=Path, help="Path to weekly-plan markdown file")
    parser.add_argument(
        "--calendar",
        default="primary",
        help="Google Calendar ID to create events in (default: primary calendar of the authenticated user)",
    )
    parser.add_argument("--all", action="store_true", help="Export all blocks, not just career/wealth/goal blocks")
    args = parser.parse_args()

    try:
        token = client.get_access_token()
    except client.CalendarAuthError as e:
        print(f"Authentication error: {e}", file=sys.stderr)
        sys.exit(1)

    text = args.weekly_plan.read_text(encoding="utf-8")
    front = _extract_frontmatter(text)
    plan_id = front.get("id", args.weekly_plan.stem)
    blocks = front.get("blocks", [])

    created = 0
    skipped = 0
    for block in blocks:
        if not _should_export(block, args.all):
            skipped += 1
            continue

        summary = block["label"]
        start = _to_iso_datetime(block["date"], block["start_time"])
        end = _to_iso_datetime(block["date"], block["end_time"])
        description = block.get("notes", "")
        description = f"{description}\n\nPlan: {plan_id}".strip()

        try:
            client.create_event(
                args.calendar,
                summary,
                start,
                end,
                description=description,
                access_token=token,
            )
            print(f"Created: {summary} ({block['date']} {block['start_time']}-{block['end_time']})")
            created += 1
        except client.CalendarAPIError as e:
            print(f"Failed to create '{summary}': {e}", file=sys.stderr)

    print(f"\nDone: {created} events created, {skipped} blocks skipped.")


if __name__ == "__main__":
    main()
