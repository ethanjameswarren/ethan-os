#!/usr/bin/env python3
r"""
Resolve ethan-life canonical tracks against Spotify and persist the result to
spotify_track_mappings.csv. Reuses a cached mapping before searching again -- same "reuse before
research" pattern as the AI track assessment layer.

Usage:
  python match_tracks.py --track-id RYCL016-A1
  python match_tracks.py --missing-only --limit 25
  python match_tracks.py --track-id RYCL016-A1 --force     # explicit reassessment, ignores cache/rejection
  python match_tracks.py --refresh-stale --limit 25         # re-check ambiguous/needs_review rows only

Environment:
  SPOTIFY_CLIENT_ID / SPOTIFY_CLIENT_SECRET / SPOTIFY_REFRESH_TOKEN - required
  ETHAN_LIFE_DIR - defaults to D:\GIT\ethan-life
  SPOTIFY_MARKET - optional ISO 3166-1 alpha-2 market code for search/availability checks
"""

import argparse
import csv
import os
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import client as spotify_client  # noqa: E402

ETHAN_LIFE = Path(os.environ.get("ETHAN_LIFE_DIR", "D:\\GIT\\ethan-life"))
TRACKS_CSV = ETHAN_LIFE / "data" / "music" / "record-collection" / "tracks.csv"
ALBUMS_CSV = ETHAN_LIFE / "data" / "music" / "record-collection" / "albums.csv"
MAPPINGS_CSV = ETHAN_LIFE / "data" / "music" / "record-collection" / "spotify_track_mappings.csv"

MAPPING_FIELDS = [
    "track_id", "spotify_track_id", "spotify_uri", "spotify_artist", "spotify_title",
    "spotify_album", "match_status", "match_confidence", "match_method", "matched_at", "verified",
]

TERMINAL_STATUSES = {"matched", "rejected", "unavailable"}


def read_csv(path):
    with open(path, "r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path, header, rows):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=header, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in header})


def normalize(text):
    text = text or ""
    text = text.lower()
    text = re.sub(r"\bfeat\.?\b|\bft\.?\b", "feat", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def parse_length_seconds(length):
    if not length or ":" not in length:
        return None
    try:
        m, s = length.split(":")
        return int(m) * 60 + int(s)
    except ValueError:
        return None


def artists_overlap(canonical_artist, candidate_artists):
    canon_parts = {normalize(p) for p in re.split(r",|&| and ", canonical_artist) if p.strip()}
    cand_parts = {normalize(a["name"]) for a in candidate_artists}
    return bool(canon_parts & cand_parts) or any(
        c in cand or cand in c for c in canon_parts for cand in cand_parts if c and cand
    )


def score_candidate(track_row, album_row, candidate):
    title_norm = normalize(track_row["Track"])
    cand_title_norm = normalize(candidate["name"])
    title_exact = title_norm == cand_title_norm

    artist_ok = artists_overlap(track_row["Artist"], candidate["artists"])

    length_s = parse_length_seconds(track_row.get("Length"))
    duration_s = candidate["duration_ms"] / 1000.0
    duration_close = length_s is not None and abs(duration_s - length_s) <= 3

    album_title_norm = normalize(album_row["Album"]) if album_row and album_row.get("Album") else ""
    cand_album_norm = normalize(candidate["album"]["name"])
    album_match = bool(album_title_norm) and (
        album_title_norm in cand_album_norm or cand_album_norm in album_title_norm
    )

    if artist_ok and title_exact and (duration_close or album_match):
        return "high"
    if artist_ok and title_exact:
        return "medium"
    if artist_ok and (cand_title_norm in title_norm or title_norm in cand_title_norm):
        return "low"
    return None


def match_one(token, track_row, album_row, market=None):
    artist = track_row["Artist"]
    title = track_row["Track"]

    query = f'track:"{title}" artist:"{artist}"'
    results = spotify_client.search_track(token, query, limit=5, market=market)
    method = "catalog_search"
    if not results:
        query = f"{artist} {title}"
        results = spotify_client.search_track(token, query, limit=5, market=market)
        method = "artist_title_search"

    if not results:
        return {"match_status": "not_found", "match_confidence": "", "match_method": method}

    scored = []
    for c in results:
        conf = score_candidate(track_row, album_row, c)
        if conf:
            scored.append((conf, c))

    high = [c for conf, c in scored if conf == "high"]
    medium = [c for conf, c in scored if conf == "medium"]
    low = [c for conf, c in scored if conf == "low"]

    def as_result(candidate, status, confidence, verified):
        market_ok = market is None or candidate.get("is_playable", True)
        if not market_ok:
            return {
                "spotify_track_id": candidate["id"],
                "spotify_uri": candidate["uri"],
                "spotify_artist": ", ".join(a["name"] for a in candidate["artists"]),
                "spotify_title": candidate["name"],
                "spotify_album": candidate["album"]["name"],
                "match_status": "unavailable",
                "match_confidence": confidence,
                "match_method": method,
                "verified": "",
            }
        return {
            "spotify_track_id": candidate["id"],
            "spotify_uri": candidate["uri"],
            "spotify_artist": ", ".join(a["name"] for a in candidate["artists"]),
            "spotify_title": candidate["name"],
            "spotify_album": candidate["album"]["name"],
            "match_status": status,
            "match_confidence": confidence,
            "match_method": method,
            "verified": "true" if verified else "",
        }

    if len(high) == 1 and not medium and not low:
        return as_result(high[0], "matched", "high", verified=True)
    if len(high) >= 1:
        # Multiple high-scoring candidates (e.g. same track on several releases) -- don't
        # auto-pick one; a false match is worse than an unmatched track.
        return as_result(high[0], "ambiguous", "low", verified=False)
    if len(medium) == 1 and not low:
        return as_result(medium[0], "likely_match", "medium", verified=False)
    if medium or low:
        best = (medium or low)[0]
        return as_result(best, "needs_review", "low", verified=False)

    return {"match_status": "not_found", "match_confidence": "", "match_method": method}


def main():
    parser = argparse.ArgumentParser(description="Resolve ethan-life tracks against Spotify")
    parser.add_argument("--track-id")
    parser.add_argument("--missing-only", action="store_true")
    parser.add_argument("--refresh-stale", action="store_true")
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument("--force", action="store_true", help="Ignore cache/rejection and re-search")
    args = parser.parse_args()

    market = os.environ.get("SPOTIFY_MARKET")

    tracks = {t["Track ID"]: t for t in read_csv(TRACKS_CSV)}
    albums = {a["Release"]: a for a in read_csv(ALBUMS_CSV)}
    mappings = read_csv(MAPPINGS_CSV) if MAPPINGS_CSV.exists() else []
    mappings_by_id = {m["track_id"]: m for m in mappings}

    if args.track_id:
        targets = [args.track_id]
    elif args.missing_only:
        targets = [tid for tid in tracks if tid not in mappings_by_id][: args.limit]
    elif args.refresh_stale:
        targets = [
            tid for tid, m in mappings_by_id.items()
            if m["match_status"] in ("ambiguous", "needs_review", "not_found")
        ][: args.limit]
    else:
        raise SystemExit("Specify --track-id, --missing-only, or --refresh-stale.")

    token = spotify_client.get_access_token()

    resolved, skipped = 0, 0
    for tid in targets:
        existing = mappings_by_id.get(tid)
        if existing and existing["match_status"] in TERMINAL_STATUSES and not args.force:
            skipped += 1
            continue
        track_row = tracks.get(tid)
        if not track_row:
            print(f"Skipping unknown track_id: {tid}")
            continue
        album_row = albums.get(track_row["Release"])
        result = match_one(token, track_row, album_row, market=market)
        result["track_id"] = tid
        result["matched_at"] = datetime.now().isoformat(timespec="seconds")
        mappings_by_id[tid] = result
        resolved += 1
        print(f"{tid}: {result['match_status']} ({result.get('match_confidence') or 'n/a'})")

    write_csv(MAPPINGS_CSV, MAPPING_FIELDS, list(mappings_by_id.values()))
    print(f"\nResolved {resolved} track(s), skipped {skipped} already-terminal mapping(s).")


if __name__ == "__main__":
    main()
