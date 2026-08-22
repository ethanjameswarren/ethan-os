#!/usr/bin/env python3
r"""
Apply Ethan's decision from review-spotify-matches to spotify_track_mappings.csv. This is the
only script that writes match_status: rejected or manually overrides a match -- everything else
(match_tracks.py, export_playlist.py) only ever proposes matches or reuses existing ones.

Usage:
  python apply_review_decision.py --track-id RYCL016-A1 --decision approve
  python apply_review_decision.py --track-id RYCL016-A1 --decision reject
  python apply_review_decision.py --track-id RYCL016-A1 --decision unavailable
  python apply_review_decision.py --track-id RYCL016-A1 --decision manual --spotify-track-id 3n3Ppam7vgaVa1iaRUc9Lp

Environment:
  ETHAN_LIFE_DIR - defaults to D:\GIT\ethan-life
  SPOTIFY_CLIENT_ID / SPOTIFY_CLIENT_SECRET / SPOTIFY_REFRESH_TOKEN - required only for --decision manual
"""

import argparse
import csv
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import client as spotify_client  # noqa: E402
from match_tracks import MAPPING_FIELDS  # noqa: E402

ETHAN_LIFE = Path(os.environ.get("ETHAN_LIFE_DIR", "D:\\GIT\\ethan-life"))
MAPPINGS_CSV = ETHAN_LIFE / "data" / "music" / "record-collection" / "spotify_track_mappings.csv"


def read_csv(path):
    with open(path, "r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path, header, rows):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=header, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in header})


def main():
    parser = argparse.ArgumentParser(description="Apply a review decision to a Spotify mapping")
    parser.add_argument("--track-id", required=True)
    parser.add_argument("--decision", required=True, choices=["approve", "reject", "unavailable", "manual"])
    parser.add_argument("--spotify-track-id", help="Required for --decision manual")
    args = parser.parse_args()

    mappings = read_csv(MAPPINGS_CSV) if MAPPINGS_CSV.exists() else []
    by_id = {m["track_id"]: m for m in mappings}
    row = by_id.get(args.track_id, {"track_id": args.track_id})
    now = datetime.now().isoformat(timespec="seconds")

    if args.decision == "approve":
        if row.get("match_status") not in ("likely_match", "ambiguous", "needs_review", "matched"):
            raise SystemExit(f"Track {args.track_id} has no pending candidate to approve.")
        row["match_status"] = "matched"
        row["verified"] = "true"

    elif args.decision == "reject":
        row["match_status"] = "rejected"
        row["verified"] = ""

    elif args.decision == "unavailable":
        row["match_status"] = "unavailable"
        row["verified"] = ""

    elif args.decision == "manual":
        if not args.spotify_track_id:
            raise SystemExit("--spotify-track-id is required for --decision manual.")
        token = spotify_client.get_access_token()
        track = spotify_client.request("GET", f"/tracks/{args.spotify_track_id}", token)
        row.update({
            "spotify_track_id": track["id"],
            "spotify_uri": track["uri"],
            "spotify_artist": ", ".join(a["name"] for a in track["artists"]),
            "spotify_title": track["name"],
            "spotify_album": track["album"]["name"],
            "match_status": "matched",
            "match_confidence": "high",
            "match_method": "manual",
            "verified": "true",
        })

    row["matched_at"] = now
    by_id[args.track_id] = row
    write_csv(MAPPINGS_CSV, MAPPING_FIELDS, list(by_id.values()))
    print(f"Recorded '{args.decision}' for {args.track_id} -> match_status={row['match_status']}")


if __name__ == "__main__":
    main()
