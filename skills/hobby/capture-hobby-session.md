# Skill: capture-hobby-session

## Purpose

Convert a natural-language description of a hobby activity into a structured `hobby.session` object and update the affected `hobby.collection-item` records.

## Input

- Natural-language session description (date, duration, activity, items involved, outcomes).
- Existing `hobby.collection-item` files in `ethan-life/domains/hobby/<project>/collection/`.

## Output

- One new `hobby.session` Markdown file.
- Updated collection-item records (assembly, painting, magnetization, events, first_game).
- Optional linked `hobby.lore-candidate` IDs if the session produced story ideas.

## Instructions

1. Determine the session type (`build`, `paint`, `lore`, `planning`, `game`, `photo`, `magnetization`, `shopping`, `review`, `other`).
2. Infer `session_date`; ask if missing.
3. Identify every collection item mentioned. If a kit does not exist, ask whether to create a new `hobby.collection-item` record rather than auto-creating it.
4. For each affected collection item, append an event to its `events` list with `date`, `event_type`, and `note`.
5. Update status fields only when the description is explicit. Do not infer completion.
6. If magnetization decisions were made, update `magnetization_status` and `magnetization_note`.
7. If the session produced canon-worthy lore ideas, output candidate IDs in `lore_candidate_ids` and create them via `generate-lore-candidates`.
8. Write the session file to `ethan-life/domains/hobby/<project>/sessions/SESSION-<id>.md`.
9. Confirm what was recorded and what remains unchanged.
