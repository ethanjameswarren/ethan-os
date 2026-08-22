#!/usr/bin/env python3
r"""
Additively sync an existing, Ethan-owned Spotify playlist with tracks from his vinyl collection
matching a style filter (e.g. "all my Techno records"). This is distinct from
export_playlist.py's DJ-set playlists: this playlist is not created or fully owned by EJ OS, so
this script only ADDS missing tracks -- it never removes or reorders anything already there,
preserving any manual curation Ethan has done in Spotify.

Usage:
  python sync_collection_style_playlist.py --style Techno --playlist-id 0O8PV7N4kgEbhQ4ybeUhCE --resolve-limit 50

Repeat with the same --style/--playlist-id to resolve more of the collection incrementally;
already-resolved/rejected/unavailable tracks are never re-searched.

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
TRACKS_CSV = ETHAN_LIFE / "data" / "music" / "record-collection" / "tracks.csv"
ALBUMS_CSV = ETHAN_LIFE / "data" / "music" / "record-collection" / "albums.csv"
MAPPINGS_CSV = ETHAN_LIFE / "data" / "music" / "record-collection" / "spotify_track_mappings.csv"
COLLECTION_PLAYLISTS_CSV = (
    ETHAN_LIFE / "data" / "music" / "record-collection" / "spotify_collection_playlists.csv"
)

COLLECTION_PLAYLIST_FIELDS = [
    "playlist_key", "filter_field", "filter_value", "spotify_playlist_id",
    "spotify_playlist_url", "created_at", "last_synced_at",
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


def main():
    parser = argparse.ArgumentParser(
        description="Additively sync an existing Spotify playlist with a collection style filter"
    )
    parser.add_argument("--style", required=True, help='Exact tracks.csv "Base" value, e.g. Techno')
    parser.add_argument("--playlist-id", required=True, help="Existing Spotify playlist ID to add tracks to")
    parser.add_argument("--resolve-limit", type=int, default=50, help="Max unmapped tracks to resolve this run")
    parser.add_argument(
        "--refresh-non-terminal", action="store_true",
        help="Also re-search tracks already marked ambiguous/needs_review/not_found (normally left "
        "for review-spotify-matches instead of being silently re-searched every run)",
    )
    args = parser.parse_args()

    market = os.environ.get("SPOTIFY_MARKET")

    all_tracks = read_csv(TRACKS_CSV)
    pool = [t for t in all_tracks if t["Base"].strip() == args.style]
    if not pool:
        raise SystemExit(f'No tracks found with Base == "{args.style}"')

    albums = {a["Release"]: a for a in read_csv(ALBUMS_CSV)}
    mappings = read_csv(MAPPINGS_CSV)
    mappings_by_id = {m["track_id"]: m for m in mappings}

    token = spotify_client.get_access_token()

    # Prioritize tracks with no mapping at all -- never spend the resolve budget re-searching
    # ambiguous/needs_review/not_found rows (those belong to review-spotify-matches) unless
    # explicitly asked to.
    never_touched = [t for t in pool if t["Track ID"] not in mappings_by_id]
    non_terminal = [
        t for t in pool
        if t["Track ID"] in mappings_by_id
        and mappings_by_id[t["Track ID"]]["match_status"] not in ("matched", "rejected", "unavailable")
    ]
    to_resolve = never_touched + (non_terminal if args.refresh_non_terminal else [])

    resolved_now = 0
    for t in to_resolve[: args.resolve_limit]:
        tid = t["Track ID"]
        album_row = albums.get(t["Release"])
        result = match_tracks.match_one(token, t, album_row, market=market)
        result["track_id"] = tid
        result["matched_at"] = datetime.now().isoformat(timespec="seconds")
        mappings_by_id[tid] = result
        resolved_now += 1
        print(f"{tid}: {result['match_status']} ({result.get('match_confidence') or 'n/a'})")

    write_csv(MAPPINGS_CSV, match_tracks.MAPPING_FIELDS, list(mappings_by_id.values()))

    target_uris = []
    status_counts = {}
    for t in pool:
        m = mappings_by_id.get(t["Track ID"])
        status = m["match_status"] if m else "unresolved"
        status_counts[status] = status_counts.get(status, 0) + 1
        if m and m["match_status"] in INCLUDABLE_STATUSES and m.get("spotify_uri"):
            target_uris.append(m["spotify_uri"])

    existing_uris = spotify_client.get_playlist_items(token, args.playlist_id)
    missing_uris = [u for u in target_uris if u not in existing_uris]

    if missing_uris:
        spotify_client.add_playlist_items(token, args.playlist_id, missing_uris)

    now = datetime.now().isoformat(timespec="seconds")
    playlists = read_csv(COLLECTION_PLAYLISTS_CSV)
    playlists_by_key = {p["playlist_key"]: p for p in playlists}
    key = f"style:{args.style}"
    playlists_by_key[key] = {
        "playlist_key": key,
        "filter_field": "Base",
        "filter_value": args.style,
        "spotify_playlist_id": args.playlist_id,
        "spotify_playlist_url": f"https://open.spotify.com/playlist/{args.playlist_id}",
        "created_at": playlists_by_key.get(key, {}).get("created_at", now),
        "last_synced_at": now,
    }
    write_csv(COLLECTION_PLAYLISTS_CSV, COLLECTION_PLAYLIST_FIELDS, list(playlists_by_key.values()))

    still_unmapped = sum(1 for t in pool if t["Track ID"] not in mappings_by_id)

    print(f"\n{args.style} collection sync (additive only, nothing removed):")
    print(f"  Pool size: {len(pool)} tracks with Base == '{args.style}'")
    print(f"  Resolved this run: {resolved_now}")
    print(f"  Added to playlist: {len(missing_uris)}")
    print(f"  Already in playlist: {len(target_uris) - len(missing_uris)}")
    for status, count in sorted(status_counts.items()):
        if status not in INCLUDABLE_STATUSES:
            print(f"  {status}: {count}")
    if still_unmapped:
        print(f"  Still unresolved (run again to continue): {still_unmapped}")


if __name__ == "__main__":
    main()
