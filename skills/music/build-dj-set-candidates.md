# Skill: build-dj-set-candidates

## Purpose

Given a set request (duration, style, BPM range, energy arc, etc.), build a candidate pool from
Ethan's collection and propose an ordered tracklist, while keeping observed evidence and inferred
metadata clearly distinct.

## Input

- `request`: parsed constraints from Ethan's natural-language ask, e.g.:
  - `target_duration_minutes` (optional)
  - `style` / genre or mood descriptor (optional, freeform, e.g. "hypnotic techno")
  - `bpm_start` / `bpm_end` or a single target BPM / range (optional)
  - `energy_arc` (optional, e.g. "starts restrained, gets darker and more driving", "peak-time")
  - `constraints` (optional, e.g. "only records I've listened to", "highest rated", "could work after <track>")
- `tracks`: all rows from `ethan-life/data/music/record-collection/tracks.csv`
- `dj_track_profiles`: all rows from `ethan-life/data/music/record-collection/dj_track_profiles.csv`
- `ai_assessments`: all rows from `ethan-life/data/music/record-collection/ai_track_assessments.csv`
- `albums`: all rows from `ethan-life/data/music/record-collection/albums.csv` (for label/release context)

## Output

- `candidate_tracks`: ordered list of track placements, each with:
  - `track_id`, `position`
  - `role_in_set` (opener | builder | driver | peak | tool | reset | closer)
  - `added_reason`: short, specific explanation, naming which evidence (Ethan's data vs. AI
    assessment vs. raw metadata) drove the decision
  - `evidence_level`: `observed` | `inferred` | `mixed`
- `excluded_notes`: brief notes on notable tracks considered but excluded, if useful
- `arc_summary`: 1-3 sentence description of the intended energy/BPM arc
- `flags`: list of placements that are heavily `inferred`, to highlight to Ethan
- `assessment_gaps`: track IDs that are strong fits by objective filters (BPM/style/duration) but
  have no usable AI assessment (missing, or stale per
  `skills/music/assess-track-for-dj-use.md`'s staleness check) and no Ethan listening data either
  — candidates for targeted enrichment before finalizing the set.

## Instructions

### 1. Determine eligible pool

- Default eligible pool is the full collection unless Ethan restricts it (e.g. "only records I've listened to" → filter to tracks with a non-blank `Energy`/`Rating`/`Comment` in `tracks.csv` or a `listened_at` in `dj_track_profiles.csv`).
- Apply explicit BPM/style/rating filters from the request first; they are hard constraints, not preferences.

### 2. Score and prioritize evidence

For each eligible track, note what evidence exists, in this priority order (do not skip ahead of higher-priority evidence when it's available):

1. Confirmed listening data: `Energy`, `Rating`, `Special`, `Tags`, `Comment`, `dj_role_confirmed`, `mix_notes`, `listened_at`.
2. A persisted, non-stale AI assessment for the track (`ai_track_assessments.csv`): `ai_energy`, `ai_role_suggested`, `ai_style`, `ai_descriptors`, `ai_mixing_notes`. Use it directly rather than re-deriving it — that's the point of persisting it. If the assessment is stale (per the staleness check in `skills/music/assess-track-for-dj-use.md`) or missing, treat this track as having no assessment for this step and note it for `assessment_gaps` if it's otherwise a strong candidate.
3. `BPM`.
4. `Key` (supporting evidence only — never a hard filter).
5. `Base` / style descriptor, label/release context.
6. Nothing beyond the above — if a track has only objective fields and no AI assessment and no listening data, any role/placement assigned to it is `inferred` and should be flagged as a gap if it's a strong candidate.

When both Ethan's data and an AI assessment exist for the same track:

- If they agree (or the AI assessment simply covers an attribute Ethan hasn't given an opinion on), use both — this is typically `mixed` unless Ethan's data alone already fully justifies the placement.
- If they disagree on the same attribute (e.g. AI `ai_energy: 4` / `ai_role_suggested: driver` vs. Ethan `Energy: 3` / `dj_role_confirmed: builder`), use Ethan's confirmed value for the actual placement decision, and mention the AI's differing read in `added_reason` as secondary context rather than discarding it silently.

### 3. Build the energy arc

- Translate the requested arc (e.g. "starts restrained, gets darker/driving", "peak-time", "hypnotic and steady") into a rough BPM/energy progression across set positions.
- Assign role buckets (opener, builder, driver, peak, tool, reset, closer) to positions consistent with that arc. A track may fit more than one role; pick the one that best matches its position.
- Favor tracks with `Rating` >= 4 or `Special: Favorite`/`Weapon` for peak/closer roles when the arc calls for a high-confidence moment, since these are Ethan's own confirmed judgments.

### 4. Order tracks

- Order primarily by the BPM/energy progression from step 3.
- Use `Key` to break ties or smooth adjacent transitions when two tracks are otherwise similarly placed — do not reorder the arc just to chase key compatibility.
- Avoid placing two tracks from the same release back-to-back unless the collection is too small to avoid it.

### 5. Assign evidence_level and added_reason per placement

- `observed`: the decisive evidence for this placement/role came from Ethan's own confirmed listening data for that track.
- `inferred`: the decisive evidence came only from objective metadata (BPM/Key/genre/label) and/or the AI assessment, with no supporting Ethan data for that attribute.
- `mixed`: Ethan supplied some confirmed data relevant to the track, but the specific placement/role decision also relied on the AI assessment or other inference to fill a gap.
- `added_reason` must name the specific evidence used, and which layer it came from (e.g. "Rating 5, tagged Driving, BPM 140 — fits the peak slot" (observed) vs. "AI assessment: style read as driving minimal, ai_role_suggested=driver, confidence medium; BPM 141 also fits — no listening data yet" (inferred) vs. "Ethan rated 4 but hasn't given a role opinion; AI assessment suggests builder based on descriptors — used here" (mixed)).

### 6. Respect target duration

- Sum `Length` for included tracks; stop adding tracks once within a reasonable margin of `target_duration_minutes` (if given). If `Length` is missing for a track, note it and use it cautiously near the duration boundary.

### 7. Identify assessment gaps

List any track that is a strong fit by objective filters (BPM/style/duration in range) but has neither Ethan listening data nor a usable AI assessment as an `assessment_gaps` entry, so the calling workflow can decide whether targeted enrichment is worthwhile before finalizing.

### 8. Summarize

- Produce `arc_summary` and explicitly list `flags` for any track/transition that is `inferred` and consequential (e.g. anchors the peak or an important transition), so the workflow can surface it prominently to Ethan.

## Constraints

- Never fabricate a track's sound, energy, or compatibility. If nothing is known beyond objective metadata, say so plainly via `evidence_level: inferred`.
- Never invent tracks that are not in `tracks.csv`.
- Do not silently drop the honesty flags when presenting results — the calling workflow must surface them.
