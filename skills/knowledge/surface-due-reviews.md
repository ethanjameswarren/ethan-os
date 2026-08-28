# Skill: surface-due-reviews

## Purpose

Surface a small number of reading-derived retention items that are due for review, without requiring a scheduler or notification infrastructure.

## Input

- `ethan-life/domains/knowledge/retention-state.yaml`
- `ethan-life/domains/knowledge/reading-state.yaml`
- `knowledge.source`, `knowledge.idea`, and `knowledge.reading-session` objects referenced by due items

## Rules

1. Filter `retention_items` where `status == active` and `next_review_due_at <= today`.
2. Sort by:
   - `retention_priority` (high first)
   - `current_confidence` (low first)
   - `next_review_due_at` (earliest first)
3. Select a small number (default 1-3) for surfacing. Do not overwhelm the user.
4. Respect fiction spoiler boundaries when loading source or session content.
5. Prefer generation/reconstruction prompts over recognition prompts.
6. When surfacing during a reading interaction, keep it brief and optional. Do not interrupt every reading session.

## Output

- list of 0-3 due retention item IDs with:
  - title
  - source book
  - days overdue or due
  - suggested retrieval prompt
- optional brief note if no items are due

## Example prompts

- "Before we start, a quick review: a few days ago you connected feedback loops to labor planning. What was the connection?"
- "One idea from your books is due: explain stock and flow in your own words."

## In-session behavior

- If the user is already in a review-reading workflow, surface all due items as part of that flow.
- If the user is starting or continuing reading, surface at most one due item and allow "skip".
