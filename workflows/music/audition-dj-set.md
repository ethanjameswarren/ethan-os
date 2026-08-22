# Workflow: audition-dj-set

## Purpose

Start or resume listening through a saved DJ set, handing control to per-track feedback capture
while retaining the active set context, so Ethan's observations can update the right canonical
record (track profile, set-track relationship, or transition).

## Trigger

- `Let's audition it`
- `Audition Hypnotic 01`
- `Audition set-20260822-001`

## Inputs

- Ethan's reference to a set (by name or `set_id`), or "it"/"that" referring to the most recently
  built/opened set in conversation context
- `ethan-life/data/music/dj-sets/sets.csv`
- `ethan-life/data/music/dj-sets/set_tracks.csv`
- `ethan-life/data/music/record-collection/tracks.csv`

## Outputs

- `ethan-life/domains/music/sessions/active-set-audition.yaml` (new or resumed)
- Updated `status` on the set's row in `sets.csv` (→ `auditioning`, if not already there or later)

## Steps

### 1. Resolve the set

Match Ethan's reference against `name` or `set_id` in `sets.csv`. If ambiguous or not found, ask
Ethan to clarify or offer to list recent candidate sets.

### 2. Load the tracklist

Join `set_tracks.csv` rows for this `set_id` with `tracks.csv` (by `track_id`) to build the ordered
tracklist, including `role_in_set` and `evidence_level` per position.

### 3. Start (or resume) the audition session

Write `ethan-life/domains/music/sessions/active-set-audition.yaml`:

```yaml
set_id: <set_id>
started_at: <ISO timestamp>
current_position: <first position, or the position where Ethan left off if resuming>
tracks:
  - position: 1
    track_id: <track_id>
    release: <Release>
    side: <Side>
    artist: <Artist>
    track: <Track>
    role_in_set: <role_in_set>
    evidence_level: <evidence_level>
  - ...
```

If `sets.csv.status` is `candidate`, update it to `auditioning`.

### 4. Confirm to Ethan

State: the set name/id, number of tracks, the current (first) track, and how to give feedback
(e.g. "This is a builder", "Move this toward the end", "Great transition into X", `next`, `done`).

### 5. Hand off

Subsequent messages during this session are routed to
`ethan-os/workflows/music/capture-set-audition-feedback.md` until Ethan says `done` or starts a new
lookup/build/audition.

## Confirmation policy

- Auto-execute: resolving the set, loading the tracklist, writing the session file, updating
  `sets.csv.status` to `auditioning`.
- Ask for confirmation: only if the set reference is ambiguous.
