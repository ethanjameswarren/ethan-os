# Workflow: manage-dj-set

## Purpose

Handle DJ set lifecycle and management actions that fall outside of building a new candidate or
live auditioning: naming/saving, opening an existing set for review, confirming it, marking it
played or archived, and direct edits (reorder, add/remove a track) requested outside an audition
session.

## Trigger

- `Save that as "Hypnotic 01".`
- `Open Hypnotic 01.`
- `Confirm this set.` / `This set is ready.`
- `Mark Hypnotic 01 as played.`
- `Archive set-20260822-001.`
- `Remove track 6 from Hypnotic 01.`
- `Add <track/release> to Hypnotic 01.`

## Inputs

- Ethan's instruction, referencing a set by name/`set_id` or "it"/"that" from conversation context
- `ethan-life/data/music/dj-sets/sets.csv`
- `ethan-life/data/music/dj-sets/set_tracks.csv`
- `ethan-life/data/music/record-collection/tracks.csv` (for resolving track/release references)

## Outputs

- Updated `sets.csv` row (`name`, `description`, `status`, `updated_at`)
- Updated `set_tracks.csv` rows (add/remove/reorder)
- Notion `DJ Sets` sync, when implemented

## Steps

### 1. Resolve the set

Match against `name` or `set_id`. If ambiguous, list candidates and ask.

### 2. Determine the requested action

- **Save/rename**: set `name` (and `description`, if given). Does not change `status`.
- **Open**: load and display the current tracklist, status, and any `inferred` flags. No writes.
- **Confirm**: only allowed from `candidate` or `auditioning` → `confirmed`. Ask for confirmation
  first if the set still has unresolved `inferred` placements Ethan hasn't reviewed; otherwise
  proceed.
- **Mark played**: `confirmed` → `played`. If the set was never `confirmed`, ask Ethan to confirm
  this is intentional before marking it played.
- **Archive**: any status → `archived`. This does not delete `set_tracks.csv` rows; it only changes
  `sets.csv.status`.
- **Add/remove/reorder track**: resolve the referenced track against `tracks.csv`
  (`Track ID`/artist+title/release+side), then insert/remove/renumber `position` values in
  `set_tracks.csv` for this `set_id` only. A newly added track gets `evidence_level: inferred`
  unless Ethan states it's based on something he's heard, and `added_reason` describing why it was
  added.

### 3. Write and confirm

Update `updated_at` on the set row, apply the change, and confirm back to Ethan in one line (what
changed, new status/name if relevant).

## Confirmation policy

- Auto-execute: save/rename, open, add/remove/reorder track edits.
- Ask for confirmation: moving `status` to `confirmed`, `played`, or `archived`, since these are
  more consequential/less reversible in intent than a `candidate` edit.
