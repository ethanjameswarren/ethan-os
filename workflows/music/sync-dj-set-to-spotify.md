# Workflow: sync-dj-set-to-spotify

## Purpose

Push the current canonical state of a set (added/removed/reordered tracks, or newly-resolved
Spotify mappings) to its existing Spotify playlist. Canonical `ethan-life` state always wins —
this never reads a manual edit back from Spotify into the canonical set.

## Trigger

- `Sync Hypnotic 01 to Spotify.`
- `Sync the Spotify playlist.`
- `Update the candidates playlist for Hypnotic 01.`

## Inputs

- Ethan's reference to a set (and playlist type, if ambiguous)
- Same inputs as `export-dj-set-to-spotify`
- `ethan-life/data/music/dj-sets/spotify_playlists.csv` (must already have a row for this
  `(set_id, playlist_type)` — if not, this is really a first export; hand off to
  `export-dj-set-to-spotify` instead of failing)

## Outputs

- Updated Spotify playlist items (full idempotent replace, in canonical order for `dj_set`)
- Updated `spotify_playlists.csv.last_synced_at`
- Updated `spotify_track_mappings.csv` for any newly resolved tracks

## Steps

### 1. Resolve the set and playlist type; check for an existing playlist relationship

If `spotify_playlists.csv` has no row for this `(set_id, playlist_type)`, treat this as a first
export instead (run `export-dj-set-to-spotify`'s steps) rather than failing.

### 2. Run the same export/sync mechanics

```
python ethan-os/scripts/spotify/export_playlist.py --set-id <set_id> --type <dj_set|candidates>
```

This is the same script used for the initial export — it already checks for an existing playlist
via `spotify_playlists.csv` (recreating it only if Spotify reports it's been deleted) and performs
a full item replace, so repeated syncs are idempotent: no duplicate playlists, no duplicate
tracks, and already-resolved tracks are not re-searched.

### 3. Report what changed

Summarize track count/match changes since the last sync if notable (e.g. "2 tracks added, 1
removed, reordered"); otherwise a brief confirmation is enough.

## Constraints

- Never treat a manual edit Ethan made directly in the Spotify app as a canonical change to
  `set_tracks.csv` — this workflow only pushes `ethan-life → Spotify`, never the reverse. (A
  future explicit reconciliation feature could inspect Spotify-side edits; that is out of scope
  here.)
- If the stored `spotify_playlist_id` no longer exists on Spotify (deleted), create a replacement
  and update `spotify_playlists.csv` — tell Ethan this happened rather than silently doing it.

## Confirmation policy

- Auto-execute: the entire sync, including resolving any newly-unmapped tracks up to the default
  batch size.
