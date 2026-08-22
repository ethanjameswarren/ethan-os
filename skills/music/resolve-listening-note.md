# Skill: resolve-listening-note

## Purpose

Map a natural-language listening observation about the current session's release into structured Track fields.

## Input

- `note`: Ethan's message, e.g.:
  - `A1 energy 3, rating 4. Boomy and driving. Definitely a weapon.`
  - `A2 favorite, groovy and trippy`
  - `B1 rating 2`
  - `next`
  - `done`
- `session`: current listening session state (`release`, `tracks`, `current_track`).

## Output

- `action`: `update_track` | `next_track` | `next_release` | `end_session` | `clarify`
- `track_ref`: side/position or track title that the note refers to.
- `fields`: dict of structured fields to write (Energy, Rating, Special, Base, Tags, Comment).
- `session_updates`: any changes to the session state (current track, etc.).

## Instructions

1. Load `ethan-life/data/music/record-collection/sessions/current.yaml`.
2. If the note is `done`, `end`, or similar, return `action: end_session`.
3. If the note is `next`, `next track`, or a track reference without subjective data, advance `current_track` and return `action: next_track`.
4. Otherwise, resolve the track reference:
   - Side/position (`A1`, `B2`, `C1`) matches against the session tracklist.
   - Track title matches against the session tracklist if no side is given.
   - If ambiguous, return `action: clarify` and ask Ethan which track.
5. Extract subjective fields from the note:
   - **Energy**: integer 1-5 if explicitly stated.
   - **Rating**: integer 1-5 if explicitly stated.
   - **Special**: a known tag like `Favorite`, `Weapon`, etc., if explicitly stated.
   - **Base**: style/base descriptor if explicitly stated (e.g., `Techno`, `Trance`).
   - **Tags**: comma-separated descriptors (e.g., `Boomy, Dark`).
   - **Comment**: the remaining descriptive text.
6. Preserve existing values that are not mentioned; do not clear a field because it was omitted.
7. Update the matching row in `ethan-life/data/music/record-collection/tracks.csv`.
8. Run `ethan-notion/scripts/sync_release.py <release>` to push the updated track to Notion.
9. Update `sessions/current.yaml` if `current_track` changed.
10. Return a concise confirmation of what was recorded and the next track if relevant.

## Constraints

- Only update tracks that belong to the current session release.
- Never invent a track that is not in the session tracklist.
- Missing values remain blank.
- Do not interpret ambiguous adjectives as explicit ratings unless Ethan states a number or clear descriptor mapped to a field.
