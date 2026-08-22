# Workflow: enrich-dj-track-assessments

## Purpose

Reusable entry point for creating/refreshing persisted AI track assessments
(`ai_track_assessments.csv`), so `build-dj-set` can rely on cached assessments instead of
researching the whole collection on every request. Supports single-track, gap-filling, batch, and
explicit-refresh modes.

## Trigger

- `Assess RYCL016 A1 for DJ use.`
- `Assess tracks with no AI assessment.`
- `Batch-enrich 50 more tracks.`
- `Refresh stale AI assessments.`
- `Reassess A2, I think the style read is wrong.`

## Inputs

- Ethan's instruction (single track, gap-fill, batch count, refresh, or explicit reassessment)
- `ethan-life/data/music/record-collection/tracks.csv`
- `ethan-life/data/music/record-collection/albums.csv`
- `ethan-life/data/music/record-collection/dj_track_profiles.csv`
- `ethan-life/data/music/record-collection/ai_track_assessments.csv`
- `ethan-life/data/music/record-collection/lookup-log.csv` (reuse recorded source URLs before any
  new external call)

## Outputs

- New/updated rows in `ai_track_assessments.csv`
- Mirrored `dj_role_suggested` updates in `dj_track_profiles.csv`
- Optional Notion sync of the small AI-field subset exposed on `Tracks` (`sync_ai_track_assessment.py <track_id>`), when implemented

## Modes

### 1. Assess one track

Resolve the track reference (Track ID, or artist+title, or side+release in context), then run
`ethan-os/skills/music/assess-track-for-dj-use.md` with `mode: assess_if_missing`.

### 2. Assess tracks with no assessment (gap-fill)

Scan `tracks.csv` for `Track ID`s with no row in `ai_track_assessments.csv`. If Ethan gave a
scope (e.g. a style/BPM filter, "only records I've listened to"), apply it first. Run the skill
for each match, up to a reasonable default batch size (25) unless Ethan asks for more/all.

### 3. Batch enrichment of the collection

Same as gap-fill but explicitly scoped to "the whole collection" or a stated count. Because this
can be slow and, for tracks needing external lookup, makes real external requests, confirm the
approximate count and expected scope with Ethan before running more than the default batch size
(25). Process in the same batch, report progress (e.g. "Assessed 40 of 719; 679 remain") and stop
at the agreed count — this is resumable, not all-or-nothing.

### 4. Refresh stale/low-confidence assessments

Scan `ai_track_assessments.csv` for rows that are stale (fingerprint mismatch or outdated
`assessment_version`, per the skill's staleness check) or `ai_confidence: low`. Run the skill with
`mode: assess_if_missing` for stale rows (it will detect staleness and regenerate) and offer to
do the same for low-confidence rows if Ethan wants them prioritized, since low confidence alone
doesn't force a refresh.

### 5. Explicit reassessment

When Ethan says a specific track's AI read seems wrong, run the skill with `mode: force_reassess`
for that track regardless of freshness.

## Steps (all modes)

1. Determine mode and scope from Ethan's message.
2. Load the CSVs listed in Inputs.
3. Resolve the target track(s) for the mode.
4. Run `ethan-os/skills/music/assess-track-for-dj-use.md` per track, respecting batch limits.
5. Report a concise summary: how many assessed/refreshed/skipped (already fresh), and how many
   required a fresh external lookup vs. were derived from already-stored data.
6. If a Notion sync script for AI fields exists, sync the touched tracks.

## Confirmation policy

- Auto-execute: single-track assessment, gap-fill up to the default batch size (25), refresh of
  stale assessments up to the default batch size, explicit reassessment of a named track.
- Ask for confirmation: any run explicitly scoped larger than the default batch size (e.g. "enrich
  the whole collection", "assess all 719 tracks"), since it may involve many external lookups.
