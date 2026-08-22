# Skill: evaluate-label-readiness

## Purpose

Compute the four label-readiness axes (data readiness, print status, application status, sticker
status) for an album or a track, live from canonical data, with specific `gap_reasons` — never a
single "incomplete" flag. This is the shared logic behind `audit-record-labels` and
`print-record-labels`; both call this skill rather than duplicating the rules.

## Input

- `entity_type`: `album` | `track`
- `entity_id`: `Release` (album) or `Track ID` (track)
- `albums`: rows from `ethan-life/data/music/record-collection/albums.csv`
- `tracks`: rows from `ethan-life/data/music/record-collection/tracks.csv`
- `ai_assessments`: rows from `ethan-life/data/music/record-collection/ai_track_assessments.csv` (tracks only, for the informational annotation described below)
- `physical_status`: matching row (if any) from `ethan-life/data/music/record-collection/physical_label_status.csv`

## Output

- `data_readiness`: `blocked` | `printable` | `complete`
- `gap_reasons`: list of `{field, category, action}` entries, e.g.
  `{field: "Energy", category: "ethan_listening", action: "listen"}`,
  `{field: "BPM", category: "objective_metadata", action: "lookup"}`,
  `{field: "Comment", category: "external_context", action: "external_lookup"}` (albums only)
- `print_status`: `not_printed` | `printed` (from `physical_status.label_printed`)
- `application_status`: `not_applied` | `applied` (from `physical_status.label_applied`)
- `sticker_status` (tracks only): `{sticker_color_applied: bool, bpm_written: bool}`
- `ai_assessment_available` (tracks only): `true` if `ai_track_assessments.csv` has a row for this
  track and at least one Ethan-listening gap exists — purely informational, never used to fill
  print content.

## Instructions

### 1. Determine required vs. desired fields

**Album**: required = `Album`, `Release` (missing either → `blocked`). Desired = `Year`, `Label`,
Avg BPM, Avg Energy, Avg Rating, `Comment`.

**Track**: required = `Track`, `Artist` (missing either → `blocked`). Desired = `Energy`, `Tags`,
`Comment`. `BPM`/`Key` are not required or desired for the *printed* label (they don't appear on
it), but a blank `BPM` still contributes a `gap_reason` (category `objective_metadata`, action
`lookup`) since Ethan needs it for the handwritten sticker — tag it clearly as a sticker-only gap,
not a print-blocking one.

### 2. Compute derived album fields (see instructions.md rounding/blank rules)

For an album, gather all `tracks.csv` rows with matching `Release`. Compute Avg BPM (nearest whole
number), Avg Energy (one decimal), Avg Rating (one decimal), each only over tracks with a
non-blank value; blank if zero tracks have a value. Never treat a blank as `0`.

### 3. Classify data readiness

- Any required field blank → `data_readiness: blocked`.
- All required fields present, at least one desired field blank/unavailable → `printable`, with a
  `gap_reasons` entry for each missing desired field.
- All required and desired fields present → `complete`.

### 4. Classify each gap's category and action

- Blank objective field (BPM, Artist, Year, Label, catalog/`Release`) → `category:
  objective_metadata`, `action: lookup`.
- Blank Ethan-subjective field (Energy, Rating, Tags, Comment on `tracks.csv`) → `category:
  ethan_listening`, `action: listen`.
- Blank album-level `Comment` (Hard Wax-style) → `category: external_context`, `action:
  external_lookup`.
- A track/album that is `complete`/`printable` but not yet printed, or printed but not applied, or
  (tracks) missing a sticker/BPM write → `category: physical_work`, `action: physical_labeling`
  (this is a separate axis, reported alongside but not merged into `data_readiness`).

### 5. Physical axes

Look up `physical_label_status.csv` for `(entity_type, entity_id)`. If no row exists, treat all
four booleans as false/not-done (a track/album with no row simply hasn't been touched by the
physical workflow yet — this is a valid, common state, not an error).

### 6. AI assessment annotation (tracks only, informational)

If any `ethan_listening` gap exists for this track and `ai_track_assessments.csv` has a row for
it, set `ai_assessment_available: true` so the calling workflow can say "Ethan data missing; AI
assessment available" — never substitute the AI fields for the missing Ethan fields in any printed
or "complete" determination.

## Constraints

- Never mark a subjective field's absence as blocking print readiness.
- Never invent a value to fill a gap; report it as a gap.
- Never let `label_printed` or `label_applied` be inferred from anything other than
  `physical_label_status.csv` (i.e. never assume something was printed because it was generated).
