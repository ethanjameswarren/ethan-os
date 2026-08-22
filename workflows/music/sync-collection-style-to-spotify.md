# Workflow: sync-collection-style-to-spotify

## Purpose

Additively sync an existing, Ethan-owned Spotify playlist (not created by EJ OS) with tracks from
his vinyl collection matching a style filter — e.g. "make sure my Techno records are in my Techno
playlist." Unlike a DJ Set/Candidate playlist, EJ OS does not own or fully control this playlist,
so this only ever **adds** missing tracks; it never removes or reorders anything Ethan already put
there.

## Trigger

- `Make sure my Techno records are in this playlist: <spotify playlist URL/ID>.`
- `Add my [style] vinyl tracks to my [style] Spotify playlist.`
- `Sync my collection's Techno tracks into <playlist>.`

## Inputs

- Ethan's style filter (matched against `tracks.csv.Base`, exact match by default — confirm with
  Ethan if a broader/hybrid match like "contains Techno" is intended instead) and the target
  Spotify playlist ID/URL
- `ethan-life/data/music/record-collection/tracks.csv`, `albums.csv`,
  `spotify_track_mappings.csv`
- `ethan-life/data/music/record-collection/spotify_collection_playlists.csv`

## Outputs

- Additively updated Spotify playlist (only adds; never removes/reorders existing items)
- Updated `spotify_track_mappings.csv` for newly resolved tracks
- Updated `spotify_collection_playlists.csv` relationship row (`playlist_key: style:<value>`)

## Steps

### 1. Confirm scope and target

Confirm the exact style filter and target playlist with Ethan if there's any ambiguity (e.g.
"Techno" exact vs. "contains Techno" including hybrid tags like "Techno / Trance"), and whether
this should be additive-only (default and strongly preferred) or, if Ethan explicitly asks for it,
a full replace — a full replace risks destroying manual curation Ethan did directly in Spotify, so
only do it on an explicit, unambiguous request.

### 2. Resolve and sync in bounded batches

Run:

```
python ethan-os/scripts/spotify/sync_collection_style_playlist.py --style <value> \
  --playlist-id <id> --resolve-limit <n, default 50>
```

This prioritizes tracks with no Spotify mapping at all over re-searching ones already marked
`ambiguous`/`needs_review`/`not_found` (those are surfaced via `review-spotify-matches`, not
silently re-searched). Repeat with the same `--style`/`--playlist-id` to work through a large
collection incrementally — each run reports how many are still unresolved.

### 3. Report

State: pool size, how many were already in the playlist, how many were newly added this run, and
counts of `ambiguous`/`needs_review`/`not_found` (with an offer to run `review-spotify-matches`
for the ones that need it). If there are still unresolved tracks, mention that and offer to
continue.

## Constraints

- Never perform a destructive replace on a playlist EJ OS doesn't own unless Ethan explicitly asks
  for one, understanding it will remove anything else in the playlist.
- Never re-search a track already marked `ambiguous`/`needs_review`/`not_found` without an
  explicit refresh request (`--refresh-non-terminal` or an explicit "try that one again").

## Confirmation policy

- Auto-execute: resolving up to the default batch size and adding matched tracks.
- Ask for confirmation: batches larger than the default, or any full-replace request.
