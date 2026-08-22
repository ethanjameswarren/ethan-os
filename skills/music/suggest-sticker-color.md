# Skill: suggest-sticker-color

## Purpose

Answer "what sticker color should this track get?" using Ethan's own documented convention —
never an invented or assumed color meaning.

## Input

- `track_id`
- `ethan-life/data/music/record-collection/sticker-color-taxonomy.md`
- Canonical track data (`tracks.csv`, `dj_track_profiles.csv`) if the taxonomy maps colors to
  fields Ethan has defined (e.g. "Red = Energy 4-5")

## Output

- `suggested_color`: a color name, or `null` if the taxonomy can't determine one
- `basis`: which taxonomy row/rule was used, or a note that the taxonomy is undefined/doesn't
  cover this case

## Instructions

1. Read `sticker-color-taxonomy.md`. If it has no defined color rows yet, respond that Ethan
   hasn't captured his sticker-color convention yet and ask him to fill it in — do not guess a
   plausible-sounding scheme (e.g. "red = high energy") on his behalf.
2. If rows exist, check whether any row's "Meaning" is expressed in terms of canonical fields
   (e.g. an explicit "Red = Energy 4-5" mapping documented by Ethan). If so, evaluate the track's
   canonical data against that mapping and suggest the matching color.
3. If the taxonomy exists but its meanings are freeform/not tied to canonical fields (e.g. "Red =
   my personal favorites, no fixed rule"), say so and ask Ethan directly which color applies,
   rather than guessing.
4. Never write a new row into `sticker-color-taxonomy.md` on Ethan's behalf — this file is only
   ever edited by Ethan's own input.

## Constraints

- Never infer a meaning for an undocumented color.
- Never treat an AI track assessment (`ai_track_assessments.csv`) as authoritative input to a
  sticker suggestion tied to Ethan's own subjective system, unless Ethan's taxonomy explicitly
  says to use it.
