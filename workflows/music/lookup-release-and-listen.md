# Workflow: lookup-release-and-listen

## Purpose

Start a listening session by identifying a physical record from minimal input, retrieving objective metadata from external sources, confirming the match with Ethan, and preparing the canonical collection and session state.

## Trigger

- `Start <identifier>`
- `Listen to <identifier>`
- `Lookup <identifier>`

## Inputs

- Natural-language identifier (catalog/release number, artist + title, etc.)
- Access to `ethan-life/data/music/record-collection/albums.csv`
- Access to `ethan-life/data/music/record-collection/tracks.csv`

## Outputs

- Updated canonical CSV records for the release
- New row in `ethan-life/data/music/record-collection/lookup-log.csv`
- `ethan-life/data/music/record-collection/sessions/current.yaml` listening session state
- Synced Album/Track pages in Notion (via `sync_release.py`)

## Steps

### 1. Parse the identifier

Determine whether the input is primarily:

- a catalog/release number (e.g., `SK11X025`, `KW34`)
- an artist + release title (e.g., `Holden Federico - Dust`)
- mixed or ambiguous

### 2. Check the canonical store

Read `albums.csv` and `tracks.csv`.

- If the release already exists and all objective Album + Track fields are populated, short-circuit to step 6 (start session) using the canonical data.
- If the release exists but is incomplete (e.g., stub with only catalog number), proceed to external lookup to fill gaps.
- If the release does not exist, proceed to external lookup.

### 3. External lookup

Run `ethan-os/skills/music/lookup-release.md`.

Search external sources in priority order:

1. Discogs
2. Hard Wax
3. Official label pages / Bandcamp
4. Other reputable record stores
5. Broader web search if needed

### 4. Confirm the match

- If one high-confidence exact catalog match exists, present a concise proposed match (release, label, year, album title, artist, track count) and ask Ethan to confirm.
- If multiple plausible matches exist, present the top candidates with distinguishing info and ask Ethan to select.
- If no reliable match exists, tell Ethan and offer to create a manual stub so the session can still proceed.

Do not proceed to writing until Ethan confirms or selects.

### 5. Write canonical records

On confirmation:

1. Append or update `albums.csv` with objective Album fields only.
2. Append or update `tracks.csv` with objective Track fields only.
3. Apply the external-BPM policy:
   - Only write BPM if a credible source explicitly lists it.
   - Do not overwrite an existing Ethan-entered BPM.
   - If sources disagree, leave BPM blank.
4. Append a provenance row to `lookup-log.csv` with:
   - timestamp
   - release
   - query
   - source URLs
   - matched catalog number
   - confidence
   - candidate count
   - Ethan's confirmation
   - BPM source flag (external / none / conflict)

### 6. Sync to Notion

Run `ethan-notion/scripts/sync_release.py <release>`.

If Notion sync fails, preserve the canonical CSV update and report the failure. Do not roll back canonical state.

### 7. Start the listening session

Write `ethan-life/data/music/record-collection/sessions/current.yaml`:

```yaml
release: <catalog/release number>
started_at: <ISO timestamp>
current_track: <first track side/position>
tracks:
  - side: A1
    artist: ...
    title: ...
    # ... objective fields
  - ...
```

Confirm to Ethan:

- Release identified
- Number of tracks
- Current track
- How to capture notes (e.g., `A1 energy 3, rating 4`)

### 8. Hand off to listening-note capture

Subsequent messages are routed to `ethan-os/skills/music/resolve-listening-note.md` until Ethan says `done` or starts a new lookup.

## Confirmation policy

- Auto-execute: parsing and canonical-store lookup.
- Ask for confirmation: proposed external match, multiple candidates, creating a manual stub.
- Auto-execute after confirmation: CSV writes, provenance logging, Notion sync, session start.
