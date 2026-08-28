# Skill: reading-stats

## Purpose

Generate useful, low-friction summaries of the user's reading library and history without gamifying reading.

## Input

- All `knowledge.source` objects with `source_type: book`
- `ethan-life/domains/knowledge/reading-state.yaml`
- `ethan-life/domains/knowledge/retention-state.yaml`
- Optional: `knowledge.idea`, `knowledge.reading-session`, `knowledge.summary`, `knowledge.review`

## Useful summaries

- **Currently reading** — active books with progress
- **Finished this month/year** — by `finished_at` date
- **Owned unread count** and list
- **Wishlist count** and list
- **Paused / abandoned** books
- **Recently added** books (by `created_at` or `acquired_at`)
- **Fiction vs nonfiction mix**
- **Common themes/domains** from `tags` and `knowledge.idea` links
- **Strongest retained ideas** — high-confidence retention items or highly-rated ideas
- **Weak concepts due for review** — active retention items with low confidence or failed recalls
- **Average rating** if there are enough rated finished books to be meaningful

## Principles

1. Be useful, not competitive. No streaks, badges, page-count races, or arbitrary volume targets.
2. Only compute averages when there are enough data points to be meaningful.
3. Prefer concise over comprehensive. The user can ask for more detail.
4. Preserve provenance. Cite source IDs when listing specific books or ideas.
5. Do not fabricate stats from missing data.

## Example output

> You own 12 books and have 7 on your wishlist. 4 are currently active: *Dune* (p. 35), *Thinking in Systems* (p. 15), *The Hobbit* (p. 12), *Der Klang der Familie* (p. 20). You finished 3 books this year. Themes that keep coming up: systems, incentives, risk, and power. Your strongest retained idea is "You fall to the level of your systems" (`idea-20260115-001`). One weak concept due for review: stock/flow labor connection (`ret-20260827-002`).

## Output

- summary of requested statistics
- relevant source/idea/retention item IDs
- optional follow-up prompt
