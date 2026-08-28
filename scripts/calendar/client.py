#!/usr/bin/env python3
"""
Minimal Google Calendar API client for Ethan OS.

No third-party dependencies (same convention as scripts/spotify/).
Reads credentials from the environment only; never writes tokens to disk.

Secrets (read from the environment only; never written to disk or logged):
  GOOGLE_CLIENT_ID
  GOOGLE_CLIENT_SECRET
  GOOGLE_REFRESH_TOKEN  (obtained once via scripts/calendar/auth.py)

Scopes requested by auth.py: https://www.googleapis.com/auth/calendar.readonly
"""

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

TOKEN_URL = "https://oauth2.googleapis.com/token"
API_BASE = "https://www.googleapis.com/calendar/v3"

READONLY_SCOPE = "https://www.googleapis.com/auth/calendar.readonly"


class CalendarAuthError(RuntimeError):
    """Raised when credentials are missing or the refresh token is invalid/revoked."""


class CalendarAPIError(RuntimeError):
    def __init__(self, status, message):
        super().__init__(f"Google Calendar API error {status}: {message}")
        self.status = status


def _require_env(name):
    value = os.environ.get(name)
    if not value:
        raise CalendarAuthError(
            f"{name} is not set. Run scripts/calendar/auth.py once to complete "
            "Google Calendar setup (see docs/integrations/google-calendar.md)."
        )
    return value


def _rfc3339(dt):
    """Return an RFC 3339 string in UTC."""
    if isinstance(dt, str):
        # Accept ISO strings; naive strings are treated as local time and converted to UTC.
        if dt.endswith("Z"):
            return dt
        try:
            parsed = datetime.fromisoformat(dt)
        except ValueError:
            parsed = datetime.strptime(dt, "%Y-%m-%d")
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=datetime.now().astimezone().tzinfo)
        return parsed.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.now().astimezone().tzinfo)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _date_only(value):
    """True if the value is a date string without time."""
    return "T" not in value and len(value) == 10


def get_access_token():
    """Exchange the long-lived refresh token for a short-lived access token."""
    client_id = _require_env("GOOGLE_CLIENT_ID")
    client_secret = _require_env("GOOGLE_CLIENT_SECRET")
    refresh_token = _require_env("GOOGLE_REFRESH_TOKEN")

    body = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
    }).encode("utf-8")

    req = urllib.request.Request(TOKEN_URL, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        text = e.read().decode()
        raise CalendarAuthError(
            f"Refresh token exchange failed ({e.code}): {text}. "
            "The refresh token may have been revoked -- re-run scripts/calendar/auth.py."
        ) from e
    return payload["access_token"]


def request(access_token, method, path, params=None, json_body=None, retries=3):
    """Call the Google Calendar API, handling 401 retry after a fresh token fetch."""
    url = f"{API_BASE}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    body = json.dumps(json_body).encode("utf-8") if json_body is not None else None
    attempt = 0
    while True:
        attempt += 1
        req = urllib.request.Request(url, data=body, method=method)
        req.add_header("Authorization", f"Bearer {access_token}")
        if body is not None:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                text = resp.read().decode()
                return json.loads(text) if text else None
        except urllib.error.HTTPError as e:
            if e.code == 401 and attempt <= 1:
                access_token = get_access_token()
                continue
            if e.code == 429 and attempt <= retries:
                retry_after = int(e.headers.get("Retry-After", "1"))
                time.sleep(retry_after)
                continue
            raise CalendarAPIError(e.code, e.read().decode()) from e


def list_calendars(access_token=None):
    """Return the list of calendars the user can access."""
    if access_token is None:
        access_token = get_access_token()
    return request(access_token, "GET", "/users/me/calendarList")


def read_events(calendar_id, time_min, time_max, access_token=None, params=None):
    """Return normalized events for a calendar and time range."""
    if access_token is None:
        access_token = get_access_token()

    path_params = {
        "singleEvents": "true",
        "orderBy": "startTime",
        "timeMin": _rfc3339(time_min),
        "timeMax": _rfc3339(time_max),
    }
    if params:
        path_params.update(params)

    encoded_id = urllib.parse.quote(calendar_id, safe="@")
    response = request(access_token, "GET", f"/calendars/{encoded_id}/events", params=path_params)
    return [normalize_event(calendar_id, item) for item in response.get("items", [])]


def _declined(item):
    """Return True if the user's response status is declined."""
    for attendee in item.get("attendees", []):
        if attendee.get("self"):
            return attendee.get("responseStatus") == "declined"
    return False


def normalize_event(calendar_id, raw):
    """Convert a Google Calendar event item into the Ethan OS planning representation."""
    start = raw.get("start", {})
    end = raw.get("end", {})

    if "dateTime" in start:
        start_value = start["dateTime"]
        end_value = end.get("dateTime", start_value)
        all_day = False
    else:
        start_value = start.get("date")
        end_value = end.get("date", start_value)
        all_day = True

    transparency = raw.get("transparency", "opaque")
    status = raw.get("status", "confirmed")
    declined = _declined(raw)

    if status == "cancelled" or declined:
        planning_behavior = "cancelled"
    elif all_day or transparency == "transparent":
        planning_behavior = "informational"
    elif status == "tentative":
        planning_behavior = "tentative"
    else:
        planning_behavior = "fixed"

    return {
        "provider": "google",
        "external_event_id": raw.get("id"),
        "calendar_id": calendar_id,
        "title": raw.get("summary", "Untitled event"),
        "start": start_value,
        "end": end_value,
        "all_day": all_day,
        "location": raw.get("location", ""),
        "status": status,
        "transparency": transparency,
        "recurrence_context": raw.get("recurringEventId"),
        "planning_behavior": planning_behavior,
        "provenance": {
            "provider": "google",
            "external_event_id": raw.get("id"),
            "calendar_id": calendar_id,
            "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        },
    }


def classify_for_planning(events):
    """Split normalized events into fixed, informational, and cancelled lists."""
    fixed = []
    informational = []
    ignored = []
    for event in events:
        behavior = event.get("planning_behavior")
        if behavior == "fixed":
            fixed.append(event)
        elif behavior == "tentative":
            # Treat tentative as flexible; planning logic can decide whether to honor it.
            fixed.append({**event, "planning_behavior": "flexible"})
        elif behavior == "informational":
            informational.append(event)
        else:
            ignored.append(event)
    return fixed, informational, ignored
