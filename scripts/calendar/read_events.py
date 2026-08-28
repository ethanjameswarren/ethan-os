#!/usr/bin/env python3
"""
Read and display normalized Google Calendar events for a date range.

Usage:
  python read_events.py --start 2026-08-28 --end 2026-08-29
"""

import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import yaml

# client.py is in the same directory
import client


def _default_ethan_life():
    # client.py is at ethan-os/scripts/calendar/client.py
    # ethan-life is the sibling of ethan-os at D:\GIT\ethan-life
    return Path(__file__).resolve().parents[3] / "ethan-life"


def load_config():
    ethan_life = Path(os.environ.get("ETHAN_LIFE", _default_ethan_life()))
    config_path = ethan_life / "domains" / "planning" / "calendar-integration.yaml"
    if not config_path.exists():
        return {"enabled": False, "calendars": []}
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f).get("calendar_integration", {"enabled": False, "calendars": []})


def main():
    parser = argparse.ArgumentParser(description="Read normalized Google Calendar events.")
    parser.add_argument("--start", required=True, help="Start date/time (ISO 8601).")
    parser.add_argument("--end", help="End date/time (ISO 8601). Defaults to start + 1 day.")
    parser.add_argument("--calendar", help="Read a single calendar id instead of the configured list.")
    args = parser.parse_args()

    start = args.start
    end = args.end or (datetime.fromisoformat(start) + timedelta(days=1)).isoformat()

    config = load_config()
    if not config.get("enabled"):
        print("Calendar integration is not enabled. Set enabled: true in "
              "ethan-life/domains/planning/calendar-integration.yaml after setup.")
        sys.exit(0)

    try:
        token = client.get_access_token()
    except client.CalendarAuthError as e:
        print(f"Authentication error: {e}")
        sys.exit(1)

    if args.calendar:
        calendars = [{"id": args.calendar, "name": args.calendar, "planning_behavior": "fixed"}]
    else:
        calendars = [c for c in config.get("calendars", []) if c.get("planning_behavior") != "ignore"]

    all_events = []
    for cal in calendars:
        raw = client.read_events(cal["id"], start, end, access_token=token)
        for event in raw:
            if cal.get("planning_behavior") == "informational":
                event["planning_behavior"] = "informational"
            all_events.append(event)

    all_events.sort(key=lambda e: e["start"])
    print(json.dumps(all_events, indent=2))


if __name__ == "__main__":
    main()
