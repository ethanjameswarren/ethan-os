#!/usr/bin/env python3
"""
Deterministic tests for Google Calendar read integration.

Uses fake fixtures only -- no real credentials or calendar data are required.
"""

import json
import os
import re
import sys
from copy import deepcopy
from datetime import datetime
from pathlib import Path

import yaml

# Allow importing scripts/calendar/client.py.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "calendar"))
import client

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "config" / "demo-personality" / "fixtures" / "domains" / "planning"
BASELINE = FIXTURES / "baseline-schedule.md"
CALENDAR_EVENTS = FIXTURES / "calendar-events.json"
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, text
    return yaml.safe_load(match.group(1)), text


def load_baseline():
    fm, _ = parse_frontmatter(BASELINE)
    return fm


def load_fixture_events():
    with open(CALENDAR_EVENTS, encoding="utf-8") as f:
        return json.load(f)["items"]


def iso_to_minutes(value):
    """Convert an ISO 8601 dateTime or a 'HH:MM' string to minutes since midnight."""
    if isinstance(value, str) and "T" in value:
        dt = datetime.fromisoformat(value)
        return dt.hour * 60 + dt.minute
    if isinstance(value, str) and len(value) == 5 and ":" in value:
        h, m = map(int, value.split(":"))
        return h * 60 + m
    raise ValueError(f"Unexpected time value: {value}")


def minutes_to_time(m):
    m = m % (24 * 60)
    return f"{m // 60:02d}:{m % 60:02d}"


def blocks_for_day(baseline, day):
    return [b for b in baseline["recurring_blocks"] if b["day_of_week"] == day]


def build_day(baseline, day, external_events, date="2026-01-08"):
    """Minimal daily planner: place external fixed events, then resolve flexible baseline blocks."""
    day_blocks = deepcopy(blocks_for_day(baseline, day))
    for ev in external_events:
        if ev.get("planning_behavior") in ("cancelled", "ignore"):
            continue
        # Calendar fixed events become fixed; informational events are noted but not scheduled.
        if ev.get("planning_behavior") == "informational":
            continue
        category = "fixed" if ev.get("planning_behavior") == "fixed" else "flexible"
        day_blocks.append({
            "label": ev["title"],
            "start_time": minutes_to_time(iso_to_minutes(ev["start"])),
            "end_time": minutes_to_time(iso_to_minutes(ev["end"])),
            "category": category,
            "source": "calendar",
        })

    # Sort by start, then by category so fixed blocks win in overlap resolution.
    day_blocks.sort(key=lambda b: (time_to_minutes(b["start_time"]), 0 if b["category"] == "fixed" else 1))

    fixed = [b for b in day_blocks if b["category"] == "fixed"]
    flexible = [b for b in day_blocks if b["category"] != "fixed"]

    # Detect fixed/fixed overlaps.
    conflicts = []
    for i in range(len(fixed) - 1):
        a, b = fixed[i], fixed[i + 1]
        if time_to_minutes(a["end_time"]) > time_to_minutes(b["start_time"]):
            conflicts.append(f"Fixed overlap on {date}: {a['label']} and {b['label']}")

    # Move flexible blocks to the next available slot.
    new_flexible = []
    for b in flexible:
        start = time_to_minutes(b["start_time"])
        end = time_to_minutes(b["end_time"])
        duration = end - start

        # Find the latest ending fixed block that overlaps this flexible block.
        while True:
            shift = 0
            for f in fixed + new_flexible:
                f_start = time_to_minutes(f["start_time"])
                f_end = time_to_minutes(f["end_time"])
                if start < f_end and end > f_start:
                    shift = max(shift, f_end - start)
            if shift == 0:
                break
            start += shift
            end = start + duration
            if end > 24 * 60:
                # Drops if it cannot fit in the day.
                break

        if end <= 24 * 60:
            new_flexible.append({
                **b,
                "start_time": minutes_to_time(start),
                "end_time": minutes_to_time(end),
                "status": "moved" if start != time_to_minutes(b["start_time"]) else "scheduled",
            })

    return {
        "date": date,
        "blocks": fixed + new_flexible,
        "conflicts": conflicts,
    }


def time_to_minutes(t):
    h, m = map(int, t.split(":"))
    return h * 60 + m


def test_normalize_and_classify():
    print("A. Read events: normalize and classify fixture")
    raw = load_fixture_events()
    events = [client.normalize_event("primary", item) for item in raw]

    fixed, informational, ignored = client.classify_for_planning(events)

    fixed_titles = {e["title"] for e in fixed}
    informational_titles = {e["title"] for e in informational}

    assert "Work meeting" in fixed_titles
    assert "Dentist" in fixed_titles
    assert "Friend's birthday" in informational_titles
    assert any(e["title"] == "Cancelled sync" and e["planning_behavior"] == "cancelled" for e in events)
    assert any(e["title"] == "Declined meeting" and e["planning_behavior"] == "cancelled" for e in events)
    assert any(e["title"] == "Tentative 1:1" and e["planning_behavior"] == "tentative" for e in events)
    print("  PASS")


def test_daily_plan_around_fixed_events():
    print("B. Daily plan: flexible blocks move around fixed calendar events")
    baseline = load_baseline()
    raw = load_fixture_events()
    events = [client.normalize_event("primary", item) for item in raw]
    fixed, _, _ = client.classify_for_planning(events)
    plan = build_day(baseline, "Thursday", fixed)

    labels = {b["label"] for b in plan["blocks"]}
    assert "Dentist" in labels
    reading = next((b for b in plan["blocks"] if b["label"] == "reading"), None)
    assert reading, "reading block should still exist"
    assert time_to_minutes(reading["start_time"]) >= 19 * 60 + 45, "reading should start after dentist"
    print("  PASS")


def test_all_day_birthday_informational():
    print("C. All-day birthday is informational, not fixed")
    raw = load_fixture_events()
    birthday = next(client.normalize_event("primary", item) for item in raw if item["summary"] == "Friend's birthday")
    assert birthday["all_day"]
    assert birthday["planning_behavior"] == "informational"
    print("  PASS")


def test_cancelled_event_ignored():
    print("D. Cancelled event is ignored")
    raw = load_fixture_events()
    events = [client.normalize_event("primary", item) for item in raw]
    cancelled = next(e for e in events if e["title"] == "Cancelled sync")
    assert cancelled["planning_behavior"] == "cancelled"
    assert cancelled["title"] not in {b["label"] for b in build_day(load_baseline(), "Thursday", events)["blocks"]}
    print("  PASS")


def test_conflict_detected():
    print("E. Calendar/baseline conflict is surfaced")
    baseline = load_baseline()
    raw = load_fixture_events()
    events = [client.normalize_event("primary", item) for item in raw]
    fixed, _, _ = client.classify_for_planning(events)
    plan = build_day(baseline, "Monday", fixed)

    assert any("commute" in c and "Work meeting" in c for c in plan["conflicts"]), plan["conflicts"]
    print("  PASS")


def test_replan_after_meeting_moves():
    print("F. Replan after calendar change: moved meeting")
    baseline = load_baseline()
    raw = load_fixture_events()
    base_event = next(item for item in raw if item["summary"] == "Moved meeting")

    before = deepcopy(base_event)
    after = deepcopy(base_event)
    after["start"] = { "dateTime": "2026-01-08T16:00:00-05:00" }
    after["end"] = { "dateTime": "2026-01-08T17:00:00-05:00" }

    before_plan = build_day(baseline, "Monday", [client.normalize_event("primary", before)])
    after_plan = build_day(baseline, "Monday", [client.normalize_event("primary", after)])

    assert any(b["label"] == "Moved meeting" and b["start_time"] == "14:00" for b in before_plan["blocks"])
    assert any(b["label"] == "Moved meeting" and b["start_time"] == "16:00" for b in after_plan["blocks"])
    print("  PASS")


def test_privacy_no_secrets_in_public_files():
    print("G. Privacy: no real credentials or secrets in public fixtures")
    fixture_text = CALENDAR_EVENTS.read_text(encoding="utf-8")
    forbidden = ["client_id", "client_secret", "refresh_token", "GOOGLE_REFRESH_TOKEN"]
    for token in forbidden:
        assert token not in fixture_text, f"{token} found in public fixture"

    gitignore = ROOT / ".gitignore"
    gitignore_text = gitignore.read_text(encoding="utf-8")
    assert ".env" in gitignore_text
    print("  PASS")


def test_offline_no_env():
    print("H. Offline/unavailable provider: graceful auth error")
    # Save and remove any env that might already be present.
    saved = {}
    for name in ["GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN"]:
        saved[name] = os.environ.pop(name, None)
    try:
        try:
            client.get_access_token()
            raise AssertionError("Expected CalendarAuthError")
        except client.CalendarAuthError as e:
            assert "GOOGLE_CLIENT_ID" in str(e)
    finally:
        for name, value in saved.items():
            if value is not None:
                os.environ[name] = value
    print("  PASS")


def main():
    print("Google Calendar integration deterministic tests")
    print("=" * 50)
    test_normalize_and_classify()
    test_daily_plan_around_fixed_events()
    test_all_day_birthday_informational()
    test_cancelled_event_ignored()
    test_conflict_detected()
    test_replan_after_meeting_moves()
    test_privacy_no_secrets_in_public_files()
    test_offline_no_env()
    print("\nAll Google Calendar integration tests passed.")


if __name__ == "__main__":
    main()
