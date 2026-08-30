#!/usr/bin/env python3
"""
Export Ethan OS weekly-plan career/goal blocks to an importable .ics calendar file.

Usage:
  python export_weekly_plan_to_ics.py path/to/weekly-plan-YYYY-MM-DD.md

Output:
  path/to/weekly-plan-YYYY-MM-DD.ics

Only blocks that are sourced from a goal or have a label containing "Career"
or "Wealth" are exported. Fixed work/commute/sleep blocks are skipped.
"""

import argparse
import re
import uuid
from datetime import datetime
from pathlib import Path

import yaml


def _extract_frontmatter(text: str) -> dict:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        raise ValueError("No YAML frontmatter found in weekly plan.")
    return yaml.safe_load(match.group(1))


def _to_ics_datetime(date_str: str, time_str: str) -> str:
    """Return a local (floating) ICS datetime string."""
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    return dt.strftime("%Y%m%dT%H%M%S")


def _escape_ics_text(value: str) -> str:
    return value.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def _should_export(block: dict) -> bool:
    source = block.get("source", "")
    label = block.get("label", "")
    return (
        source == "goal"
        or "Career" in label
        or "Wealth" in label
        or "review" in label.lower()
    )


def _build_event(block: dict, plan_id: str) -> str:
    start = _to_ics_datetime(block["date"], block["start_time"])
    end = _to_ics_datetime(block["date"], block["end_time"])
    summary = _escape_ics_text(block["label"])
    notes = block.get("notes", "")
    description = _escape_ics_text(f"{notes}\n\nPlan: {plan_id}").strip()
    uid = f"{plan_id}-{block['date']}-{block['start_time'].replace(':', '')}@ethan-os"
    return (
        "BEGIN:VEVENT\n"
        f"DTSTART:{start}\n"
        f"DTEND:{end}\n"
        f"SUMMARY:{summary}\n"
        f"DESCRIPTION:{description}\n"
        f"UID:{uid}\n"
        "END:VEVENT"
    )


def main():
    parser = argparse.ArgumentParser(description="Export weekly plan blocks to .ics")
    parser.add_argument("weekly_plan", type=Path, help="Path to weekly-plan markdown file")
    args = parser.parse_args()

    text = args.weekly_plan.read_text(encoding="utf-8")
    front = _extract_frontmatter(text)
    plan_id = front.get("id", args.weekly_plan.stem)
    blocks = front.get("blocks", [])

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        f"PRODID:-//Ethan OS//Weekly Plan {plan_id}//EN",
    ]

    exported = 0
    for block in blocks:
        if _should_export(block):
            lines.append(_build_event(block, plan_id))
            exported += 1

    lines.append("END:VCALENDAR")

    out_path = args.weekly_plan.with_suffix(".ics")
    # Standard .ics uses CRLF line endings; newline='\r\n' handles that portably.
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\r\n")
    print(f"Exported {exported} events to {out_path}")


if __name__ == "__main__":
    main()
