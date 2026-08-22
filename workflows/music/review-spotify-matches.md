# Workflow: review-spotify-matches

## Purpose

Present Spotify mappings that need Ethan's judgment (`ambiguous`, `needs_review`, and optionally
`likely_match`) and apply his decision, so weak matches never silently end up in a playlist and
rejected candidates are never re-suggested.

## Trigger

- `Show me Spotify matches that need review.`
- `Approve the Spotify match for RYCL016-A1.`
- `That's not the right track — reject it.`
- `Use this Spotify track instead: <spotify track id/URL>.`
- `Mark that track as unavailable on Spotify.`

## Inputs

- `ethan-life/data/music/record-collection/spotify_track_mappings.csv`
- `ethan-life/data/music/record-collection/tracks.csv`, `albums.csv` (for context)

## Outputs

- Updated `spotify_track_mappings.csv` rows (via `ethan-os/scripts/spotify/apply_review_decision.py`)

## Steps

### 1. List pending matches

Filter `spotify_track_mappings.csv` to `match_status` in `ambiguous`, `needs_review` (and
`likely_match` if Ethan wants those double-checked too). For each, present:

- Canonical track (artist, title, release)
- Proposed Spotify track (artist, title, album)
- Duration, if available
- Confidence and a short reason it needed review (e.g. "two equally plausible candidates", "album
  doesn't match the vinyl release", "duration unknown")

### 2. Apply Ethan's decision

- **Approve**: `python ethan-os/scripts/spotify/apply_review_decision.py --track-id <id> --decision approve`
- **Reject**: `... --decision reject` — this track's proposed candidate will not be re-suggested
  on future resolution runs unless Ethan explicitly asks for a re-search.
- **Choose an alternative**: `... --decision manual --spotify-track-id <id>` — looks up the
  specified Spotify track directly and records it as a verified, high-confidence match.
- **Mark unavailable**: `... --decision unavailable`.

### 3. Confirm and move on

Acknowledge each decision briefly and move to the next pending item. If a set export/sync is
waiting on this review, mention that re-running the export will now pick up the resolved tracks.

## Constraints

- Never repeatedly re-ask about a `rejected` mapping.
- Never apply a decision Ethan didn't actually state (e.g. don't infer "approve" from silence).

## Confirmation policy

- Auto-execute: listing pending matches (read-only) and applying an explicit decision Ethan just
  stated.
