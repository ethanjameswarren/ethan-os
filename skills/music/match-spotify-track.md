# Skill: match-spotify-track

## Purpose

Resolve one or more canonical tracks to a Spotify track identity, reusing any cached mapping
before searching again, and never guessing when evidence is weak. The deterministic matching and
persistence logic lives in `ethan-os/scripts/spotify/match_tracks.py`; this skill describes when
and how to invoke it and how to interpret/report the result.

## Input

- `track_id`(s) to resolve, or a mode: `missing_only` (unmapped tracks) or `refresh_stale`
  (re-check `ambiguous`/`needs_review`/`not_found` rows)
- `force`: if true, ignore the cache (including `rejected`) and re-search
- Canonical data: `tracks.csv`, `albums.csv`
- Existing `spotify_track_mappings.csv`

## Output

- Updated `spotify_track_mappings.csv` row(s)
- A short report per track: status, confidence, and (if not matched) why

## Instructions

1. For each requested track, check `spotify_track_mappings.csv` first. If a row exists with
   `match_status` in `matched`, `rejected`, or `unavailable` and `force` is not set, use it as-is —
   do not call Spotify again.
2. Otherwise, run `python ethan-os/scripts/spotify/match_tracks.py --track-id <id>` (or
   `--missing-only`/`--refresh-stale` for batch modes), which:
   - Searches Spotify with a catalog-scoped query first (`track:"<title>" artist:"<artist>"`),
     falling back to a plain `<artist> <title>` query if that returns nothing.
   - Scores each candidate deterministically against artist, title, duration, and album/release
     evidence (see "Matching evidence and confidence" in
     `instructions/domains/music/instructions.md` for the exact rules) — no statistical/ML scoring.
   - Writes the result to `spotify_track_mappings.csv`.
3. Interpret the result:
   - `matched` (high confidence) — safe to include in playlist exports automatically.
   - `likely_match` (medium confidence) — usable, but call it out in any report rather than
     treating it identically to a high-confidence match.
   - `ambiguous` / `needs_review` (low confidence) — never auto-include; route to
     `review-spotify-matches`.
   - `not_found` — normal and expected for vinyl-only/underground releases; not an error.
   - `unavailable` — a Spotify track exists but isn't playable in Ethan's market or was removed.
4. Batch/background enrichment ("Map my collection to Spotify") uses `--missing-only` with a
   bounded `--limit` (default 25) per run, mirroring the AI-assessment enrichment workflow's
   incremental approach — never require resolving the whole ~700+ track collection before export
   works.

## Constraints

- Never select a low-confidence/ambiguous candidate automatically. A false match is worse than an
  unmatched track.
- Never re-search a `rejected` mapping without an explicit refresh/force request.
- Never write Spotify-derived fields (genre, popularity, audio features, etc.) anywhere other than
  `spotify_track_mappings.csv`'s own columns — never into `tracks.csv`, `dj_track_profiles.csv`,
  or `ai_track_assessments.csv`.
