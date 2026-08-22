# Skill: classify-dj-set-feedback

## Purpose

During DJ set auditioning, classify one of Ethan's natural-language observations into the correct
destination: the track's permanent DJ profile, this set's track relationship, or transition
knowledge between two adjacent tracks.

## Input

- `note`: Ethan's message, e.g.:
  - `This is more of a builder.`
  - `Way too aggressive here.`
  - `This works perfectly after track 4.`
  - `Move this toward the end.`
  - `This is a tool.`
  - `Energy 4.`
  - `Great transition into X.`
  - `Don't use these two together.`
  - `next` / `done`
- `audition`: active set audition state (`active-set-audition.yaml`) — `set_id`, `current_position`, ordered track list with `track_id`/`role_in_set`/`evidence_level` per position.

## Output

- `action`: `update_track_profile` | `update_set_track` | `update_transition` | `reorder` | `next_track` | `end_audition` | `clarify`
- `target_track_id` / `target_position`: which track(s) the note refers to.
- `fields`: structured field updates for the chosen destination.
- `session_updates`: any changes to `active-set-audition.yaml` (e.g. `current_position`).

## Instructions

1. If the note is `done`, `end`, or similar, return `action: end_audition`.
2. If the note is `next`, `next track`, or a bare track reference with no content, return `action: next_track` and advance `current_position`.
3. Resolve which track(s) the note refers to:
   - No explicit reference → the current track at `current_position`.
   - `"track 4"` / an explicit position → that position in the audition tracklist.
   - `"after X"` / `"into X"` / `"before X"` → the current track plus the named adjacent track.
   - If ambiguous, return `action: clarify`.
4. Classify the note's scope:
   - **Permanent track profile** — statements that describe the track itself, independent of this arrangement (e.g. "Energy 4", "Rating 5", "This is a tool" as a general statement, "Boomy and driving"). Route existing objective/Ethan-only fields (`Energy`, `Rating`, `Special`, `Base`, `Tags`, `Comment`) to `tracks.csv` exactly as `resolve-listening-note` does. Route DJ-role/mix-note statements to `dj_track_profiles.csv` (`dj_role_confirmed`, `mix_notes`, `listened_at`).
   - **Set-track relationship** — statements scoped to this set's arrangement (e.g. "Move this toward the end", "This is more of a builder here", "too aggressive at this point in the set"). Update `role_in_set`, `position` (via `action: reorder`), or leave a note in this set's `set_tracks.csv` row.
   - **Transition knowledge** — statements about how two specific tracks mix together (e.g. "This works perfectly after track 4", "Great transition into X", "Don't use these two together"). Write to `transition_notes` on the relevant `set_tracks.csv` row(s), naming both tracks. A negative statement ("don't use these two together") should be recorded plainly as a caution, not silently dropped or reworded as positive.
   - Default to the narrowest applicable scope (set-track or transition) over the permanent profile when a note could plausibly be either — auditioning feedback is usually about this arrangement, not a universal claim about the track.
5. When a role is confirmed as a *general* property of the track (Ethan states it without set-specific qualification, e.g. plainly "This is a tool"), it is acceptable to also update `dj_role_confirmed`. When it's qualified to this set/position (e.g. "It's a tool here", "in this slot it's more of a reset"), only update `role_in_set` on this `set_tracks.csv` row.
6. For `reorder` actions, update `position` values in `set_tracks.csv` for the affected set only; do not touch other sets containing the same track.
7. After any `update_track_profile`, `update_set_track`, or `update_transition` action, mark the affected `set_tracks.csv` row's `evidence_level` as `observed` (or `mixed` if only part of the placement is now confirmed).
8. Preserve existing values not mentioned in the note; never clear a field because it was omitted.
9. Return a concise confirmation of what was recorded and where (track profile vs. this set vs. transition).

## Constraints

- Never invent a track or position not present in the active audition tracklist.
- Never silently promote a set-specific observation into the permanent track profile.
- Missing/ambiguous references return `action: clarify` rather than guessing.
