# Workflow: export-dj-set-to-spotify

## Purpose

Send a saved DJ set — or a broader candidate/audition pool for it — to Spotify as a playlist, for
casual listening or auditioning. Creates the playlist if none exists yet for this
`(set_id, playlist_type)`; if one already exists, this behaves the same as
`sync-dj-set-to-spotify` rather than creating a duplicate.

## Trigger

- `Send Hypnotic 01 to Spotify.`
- `Put the candidates for Hypnotic 01 on Spotify.`
- `Make a Spotify playlist from these candidates.`

## Inputs

- Ethan's reference to a set (name or `set_id`) and which type he means (the set itself, or its
  candidates/audition pool — infer from wording; ask if genuinely ambiguous)
- `ethan-life/data/music/dj-sets/sets.csv`, `set_tracks.csv`
- `ethan-life/data/music/record-collection/tracks.csv`, `albums.csv`,
  `spotify_track_mappings.csv`
- `ethan-life/data/music/dj-sets/spotify_playlists.csv`

## Outputs

- A new (or reused) Spotify playlist
- Updated `spotify_track_mappings.csv` for any newly resolved tracks
- Updated `spotify_playlists.csv` relationship row

## Steps

### 1. Resolve the set and playlist type

Match Ethan's reference against `sets.csv`. Determine `playlist_type`:

- **DJ Set** (`dj_set`): "send/put/export **the set**" — uses the canonical `set_tracks.csv`
  ordering (only `proposed`/`confirmed` rows).
- **Candidates** (`candidates`): "the candidates"/"audition pool"/"options" — a broader pool for
  casual evaluation. Prefer generating this pool via
  `ethan-os/skills/music/build-dj-set-candidates.md` (run with a larger pool size, e.g. 30-50, and
  without writing every result into `set_tracks.csv`) and pass the resulting track ID list to the
  export script; only fall back to the script's simple BPM/rating heuristic for a quick, low-
  stakes request where Ethan hasn't asked for anything curated.

### 2. Resolve tracks and export

Run:

```
python ethan-os/scripts/spotify/export_playlist.py --set-id <set_id> --type <dj_set|candidates> \
  [--track-ids-file <path>] [--pool-size <n>]
```

This resolves any unmapped tracks (via `match-spotify-track`), creates or reuses the playlist per
`spotify_playlists.csv`, and replaces its items with the confidently matched tracks in the
appropriate order (canonical `position` order for `dj_set`; unordered for `candidates`).

### 3. Report the result

State plainly: playlist created (or reused), the Spotify URL, and match counts, e.g.:

> Hypnotic 01 created on Spotify.
> 17/20 tracks matched.
> 2 vinyl-only/unavailable.
> 1 ambiguous match needs review.

Never let missing/unavailable tracks block playlist creation — the canonical set's positions are
unaffected by what Spotify could represent.

### 4. Offer next steps

If anything is `ambiguous`/`needs_review`, offer `review-spotify-matches`. Mention that future
changes to the set can be pushed with `sync-dj-set-to-spotify` (or just re-running this same
request, since it's idempotent).

## Confirmation policy

- Auto-execute: resolving unmapped tracks up to the default batch size, creating/updating the
  playlist, reporting results.
- Ask for confirmation: only if the set/type reference is ambiguous.
