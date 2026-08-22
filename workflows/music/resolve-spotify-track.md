# Workflow: resolve-spotify-track

## Purpose

Resolve one track, a batch of unmapped tracks, or the whole collection incrementally against
Spotify, independent of any specific playlist export. This is also what "Map my collection to
Spotify" runs, in bounded batches.

## Trigger

- `Find the Spotify version of this track.`
- `Map RYCL016-A1 to Spotify.`
- `Map my collection to Spotify.`
- `Resolve the tracks with no Spotify match yet.`

## Inputs

- Ethan's reference (a specific track, "unmapped tracks", or "my collection") and optional batch
  size
- `ethan-life/data/music/record-collection/tracks.csv`, `albums.csv`
- `ethan-life/data/music/record-collection/spotify_track_mappings.csv`

## Outputs

- Updated `spotify_track_mappings.csv`
- A concise report of what was resolved and to what confidence

## Steps

### 1. Determine scope

- A specific track reference → resolve just that one.
- "Unmapped"/"my collection" → batch mode, default limit 25 unless Ethan asks for more (ask for
  confirmation before resolving more than ~100 in one run, since each unmapped track is a live
  Spotify search call).

### 2. Resolve

Run `ethan-os/skills/music/match-spotify-track.md` for the scoped track(s).

### 3. Report

- Single track: state the match (or why it couldn't be matched) plainly, including confidence.
- Batch: report counts by outcome (matched / likely_match / ambiguous-needs-review / not_found /
  unavailable), and how many unmapped tracks remain in the collection afterward.

### 4. Offer next steps

If any results are `ambiguous`/`needs_review`, offer to run `review-spotify-matches`. If Ethan was
resolving tracks for a set he's about to export, hand off to `export-dj-set-to-spotify`.

## Confirmation policy

- Auto-execute: single-track resolution, batch resolution up to the default limit (25).
- Ask for confirmation: batch runs larger than the default limit.
