# Workflow: build-dj-set

## Purpose

Build a candidate DJ set from Ethan's existing vinyl collection using objective track metadata,
external release context (already recorded in the collection), and Ethan's confirmed listening
data. The result is always a `candidate` set — never presented as a finished, ready-to-play mix,
and never presented as knowing how an unlistened-to track actually sounds.

## Trigger

- `Build me a techno set`
- `Build a 90-minute hypnotic set`
- `Give me a driving set around 140 BPM`
- `Build a set from the records I've rated highest`
- `Start deep and hypnotic and get harder`
- `Give me tracks that could work after <track/release>`
- `Build a set using only records I've listened to`
- `Find some peak-time options from my collection`

## Inputs

- Ethan's natural-language request
- `ethan-life/data/music/record-collection/albums.csv`
- `ethan-life/data/music/record-collection/tracks.csv`
- `ethan-life/data/music/record-collection/dj_track_profiles.csv`
- `ethan-life/data/music/record-collection/ai_track_assessments.csv`
- `ethan-life/data/music/dj-sets/sets.csv` (for `set_id` numbering)

## Outputs

- New row in `ethan-life/data/music/dj-sets/sets.csv` (`status: candidate`)
- New rows in `ethan-life/data/music/dj-sets/set_tracks.csv` for the proposed tracklist
- A proposed ordering presented to Ethan, with evidence flags

## Steps

### 1. Parse the request

Extract whatever constraints are present: target duration, style/mood descriptor, BPM range or
target, energy arc description, and any explicit restriction (e.g. "only records I've listened
to", "highest rated", "could work after `<track>`"). Missing constraints are fine — use sensible
defaults (e.g. no duration limit, full collection as the pool) and say what you assumed.

### 2. Load collection state

Read `albums.csv`, `tracks.csv`, `dj_track_profiles.csv`, and `ai_track_assessments.csv`. This is
"reuse before research": normal set construction relies on what's already persisted rather than
re-researching tracks from scratch.

### 3. Build candidates (reuse cached assessments; enrich only meaningful gaps)

Run `ethan-os/skills/music/build-dj-set-candidates.md` with the parsed request and collection
state, including the loaded AI assessments.

If the skill reports `assessment_gaps` (strong-fit candidate tracks with no usable/fresh AI
assessment), perform targeted enrichment for those specific tracks only via
`ethan-os/workflows/music/enrich-dj-track-assessments.md` (single-track/gap-fill mode), capped at
a small default (10 tracks) per build request. Do not re-query or reassess the whole collection as
part of a normal build. If more than the cap would meaningfully improve the set, mention that to
Ethan and offer a follow-up `enrich-dj-track-assessments` batch run rather than doing it inline.

Re-run candidate selection with the newly enriched assessments included, then continue.

### 4. Present the proposal

Show Ethan:

- The proposed ordering with role labels (opener/builder/driver/peak/tool/reset/closer).
- The arc summary (BPM/energy progression).
- Any tracks/transitions flagged as relying heavily on inferred metadata rather than his own
  listening data — call these out explicitly and separately, don't bury them.
- Approximate total duration if a target was given.

### 5. Persist as a candidate set

On presenting the proposal (no separate confirmation needed to create the candidate — creating a
*candidate* is low-risk and reversible; confirmation is required later to move it beyond
`candidate`):

1. Generate `set_id` as `set-YYYYMMDD-NNN` (next sequence number for the day in `sets.csv`).
2. Append a row to `sets.csv` with `status: candidate`, the parsed constraints
   (`target_duration_minutes`, `style`, `bpm_start`, `bpm_end`), `name` left blank unless Ethan
   named it in the same request, and `created_at`/`updated_at` timestamps.
3. Append one row per track to `set_tracks.csv` with `position`, `role_in_set`, `added_reason`,
   `evidence_level`, and `status: proposed`.
4. Tell Ethan the `set_id` (and name, if any) so he can refer back to it, and that it's saved as a
   candidate — not yet confirmed or played.

### 6. Offer next steps

Suggest natural next actions: naming/saving it (`manage-dj-set`), auditioning it
(`audition-dj-set`), or asking for a revised build.

## Confirmation policy

- Auto-execute: parsing, candidate generation, targeted gap-fill enrichment up to the default cap
  (10 tracks), writing the `candidate` set and its tracks.
- Ask for confirmation: nothing required to create a candidate, or for capped enrichment.
  Confirmation is required before a set moves to `confirmed`, `played`, or `archived` (handled by
  `manage-dj-set`), and before enrichment beyond the default cap (handled by
  `enrich-dj-track-assessments`).
