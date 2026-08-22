#!/usr/bin/env python3
r"""
Create-or-sync a Spotify playlist from an ethan-life DJ set (idempotent: safe to call repeatedly,
e.g. for both "export" and "sync" -- it creates the playlist only if one doesn't already exist for
this (set_id, playlist_type), otherwise it updates the existing one in place).

Direction is always ethan-life -> Spotify. Canonical set order/roles/ratings are never modified by
this script; a manual edit Ethan makes in Spotify is not read back in.

Usage:
  python export_playlist.py --set-id set-20260822-001 --type dj_set
  python export_playlist.py --set-id set-20260822-001 --type candidates --track-ids-file candidates.txt
  python export_playlist.py --set-id set-20260822-001 --type candidates --pool-size 40   # simple fallback heuristic

For `candidates`, prefer --track-ids-file (one Track ID per line) populated by the
build-dj-set-candidates skill's own curated pool. The --pool-size heuristic below is a simple
BPM/style/rating filter, useful for a quick standalone run but not a substitute for the skill's
evidence-weighted selection.

Environment:
  SPOTIFY_CLIENT_ID / SPOTIFY_CLIENT_SECRET / SPOTIFY_REFRESH_TOKEN - required
  ETHAN_LIFE_DIR - defaults to D:\GIT\ethan-life
  SPOTIFY_MARKET - optional
"""

import argparse
import csv
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import client as spotify_client  # noqa: E402
import match_tracks  # noqa: E402

ETHAN_LIFE = Path(os.environ.get("ETHAN_LIFE_DIR", "D:\\GIT\\ethan-life"))
SETS_CSV = ETHAN_LIFE / "data" / "music" / "dj-sets" / "sets.csv"
SET_TRACKS_CSV = ETHAN_LIFE / "data" / "music" / "dj-sets" / "set_tracks.csv"
PLAYLISTS_CSV = ETHAN_LIFE / "data" / "music" / "dj-sets" / "spotify_playlists.csv"
MAPPINGS_CSV = ETHAN_LIFE / "data" / "music" / "record-collection" / "spotify_track_mappings.csv"
TRACKS_CSV = ETHAN_LIFE / "data" / "music" / "record-collection" / "tracks.csv"
ALBUMS_CSV = ETHAN_LIFE / "data" / "music" / "record-collection" / "albums.csv"

PLAYLIST_FIELDS = [
    "set_id", "playlist_type", "spotify_playlist_id", "spotify_playlist_url",
    "created_at", "last_synced_at",
]

INCLUDABLE_STATUSES = {"matched", "likely_match"}


def read_csv(path):
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path, header, rows):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=header, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in header})


def ordered_set_track_ids(set_id):
    rows = [
        r for r in read_csv(SET_TRACKS_CSV)
        if r["set_id"] == set_id and r["status"] in ("proposed", "confirmed")
    ]
    rows.sort(key=lambda r: int(r["position"]))
    return [r["track_id"] for r in rows]


def heuristic_candidate_pool(set_row, pool_size):
    tracks = read_csv(TRACKS_CSV)
    bpm_start = float(set_row["bpm_start"]) if set_row.get("bpm_start") else None
    bpm_end = float(set_row["bpm_end"]) if set_row.get("bpm_end") else None

    def in_range(t):
        if not t["BPM"]:
            return bpm_start is None and bpm_end is None
        bpm = float(t["BPM"])
        lo = (bpm_start - 5) if bpm_start else None
        hi = (bpm_end + 5) if bpm_end else None
        return (lo is None or bpm >= lo) and (hi is None or bpm <= hi)

    def sort_key(t):
        rating = float(t["Rating"]) if t["Rating"] else 0
        energy = float(t["Energy"]) if t["Energy"] else 0
        return (rating, energy)

    pool = [t for t in tracks if in_range(t)]
    pool.sort(key=sort_key, reverse=True)
    return [t["Track ID"] for t in pool[:pool_size]]


def playlist_name_and_description(set_row, playlist_type):
    label = set_row.get("name") or set_row["set_id"]
    if playlist_type == "dj_set":
        name = f"EJ OS — {label}"
        status = set_row.get("status", "candidate")
        adjective = "Confirmed" if status in ("confirmed", "played") else "Candidate"
        description = f"{adjective} DJ set generated from Ethan's vinyl collection by EJ OS."
    else:
        name = f"EJ OS — {label} — Candidates"
        description = f"Audition pool for {label}. Canonical track data and ordering live in EJ OS."
    return name, description[:300]


def resolve_uris(track_ids, token, market):
    mappings = read_csv(MAPPINGS_CSV)
    mappings_by_id = {m["track_id"]: m for m in mappings}
    tracks = {t["Track ID"]: t for t in read_csv(TRACKS_CSV)}
    albums = {a["Release"]: a for a in read_csv(ALBUMS_CSV)}

    uris, report = [], {"matched": 0, "likely_match": 0, "not_found": 0, "unavailable": 0,
                         "ambiguous": 0, "needs_review": 0, "rejected": 0, "missing_track": 0}
    changed = False
    for tid in track_ids:
        mapping = mappings_by_id.get(tid)
        if mapping is None:
            track_row = tracks.get(tid)
            if not track_row:
                report["missing_track"] += 1
                continue
            album_row = albums.get(track_row["Release"])
            result = match_tracks.match_one(token, track_row, album_row, market=market)
            result["track_id"] = tid
            result["matched_at"] = datetime.now().isoformat(timespec="seconds")
            mapping = result
            mappings_by_id[tid] = mapping
            changed = True
        status = mapping.get("match_status", "not_found")
        report[status] = report.get(status, 0) + 1
        if status in INCLUDABLE_STATUSES and mapping.get("spotify_uri"):
            uris.append(mapping["spotify_uri"])

    if changed:
        write_csv(MAPPINGS_CSV, match_tracks.MAPPING_FIELDS, list(mappings_by_id.values()))

    return uris, report


def main():
    parser = argparse.ArgumentParser(description="Create-or-sync a Spotify playlist from a DJ set")
    parser.add_argument("--set-id", required=True)
    parser.add_argument("--type", choices=["dj_set", "candidates"], required=True)
    parser.add_argument("--pool-size", type=int, default=40)
    parser.add_argument("--track-ids-file", help="One Track ID per line; overrides --pool-size for candidates")
    args = parser.parse_args()

    market = os.environ.get("SPOTIFY_MARKET")

    sets = {s["set_id"]: s for s in read_csv(SETS_CSV)}
    set_row = sets.get(args.set_id)
    if not set_row:
        raise SystemExit(f"Set '{args.set_id}' not found in {SETS_CSV}")

    if args.type == "dj_set":
        track_ids = ordered_set_track_ids(args.set_id)
    elif args.track_ids_file:
        track_ids = [line.strip() for line in Path(args.track_ids_file).read_text().splitlines() if line.strip()]
    else:
        track_ids = heuristic_candidate_pool(set_row, args.pool_size)

    if not track_ids:
        raise SystemExit(f"No tracks resolved for set '{args.set_id}' (type={args.type}).")

    token = spotify_client.get_access_token()
    uris, report = resolve_uris(track_ids, token, market)

    playlists = read_csv(PLAYLISTS_CSV)
    playlists_by_key = {(p["set_id"], p["playlist_type"]): p for p in playlists}
    key = (args.set_id, args.type)
    existing = playlists_by_key.get(key)

    name, description = playlist_name_and_description(set_row, args.type)
    now = datetime.now().isoformat(timespec="seconds")

    playlist_id = None
    if existing:
        live = spotify_client.get_playlist(token, existing["spotify_playlist_id"])
        if live:
            playlist_id = existing["spotify_playlist_id"]
            spotify_client.update_playlist_details(token, playlist_id, name=name, description=description)

    created = False
    if not playlist_id:
        user_id = spotify_client.get_current_user_id(token)
        playlist = spotify_client.create_playlist(token, user_id, name, description, public=False)
        playlist_id = playlist["id"]
        created = True

    if uris:
        spotify_client.replace_playlist_items(token, playlist_id, uris)

    playlist_url = f"https://open.spotify.com/playlist/{playlist_id}"
    playlists_by_key[key] = {
        "set_id": args.set_id,
        "playlist_type": args.type,
        "spotify_playlist_id": playlist_id,
        "spotify_playlist_url": playlist_url,
        "created_at": existing["created_at"] if existing else now,
        "last_synced_at": now,
    }
    write_csv(PLAYLISTS_CSV, PLAYLIST_FIELDS, list(playlists_by_key.values()))

    action = "Created" if created else "Synced"
    total = len(track_ids)
    included = len(uris)
    print(f"{action} playlist '{name}': {playlist_url}")
    print(f"{included}/{total} tracks matched and included.")
    for status, count in report.items():
        if count and status not in INCLUDABLE_STATUSES:
            print(f"  {status}: {count}")


if __name__ == "__main__":
    main()
