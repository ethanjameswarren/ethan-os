# Workflow: review-reading

## Purpose

Review reading-derived retention items on demand or when due, emphasizing retrieval and understanding.

## Triggers

- "What ideas are due for review?"
- "Review my reading notes."
- "Quiz me on Thinking in Systems."
- "What have I retained from Dune?"
- Scheduled review surfaced automatically (when an automated scheduler exists)

## Steps

1. Read `ethan-life/domains/knowledge/retention-state.yaml`.
2. Determine the review scope from the user's message:
   - If a specific book is named, filter by `source_book_id`.
   - If the user asks for due items, use `skills/knowledge/surface-due-reviews.md` to select active items with `next_review_due_at <= today`.
   - If the user asks broadly, select a small set (1-3) of high-priority/due items.
3. For each selected item, load the referenced object:
   - `knowledge.idea` for `source_type: idea`
   - `knowledge.reading-session` and the specific `insight_id` for `source_type: session_insight`
4. Load the source `knowledge.source` and `knowledge.reading-profile` to honor `spoiler_policy` for fiction.
5. Use `skills/knowledge/perform-review.md` to ask a retrieval-focused question. Never use multiple-choice unless the user explicitly asks.
6. After the user's response, evaluate semantically (strong / partial / failed / skipped).
7. Update the retention item in `retention-state.yaml` using `skills/knowledge/schedule-review.md`.
8. If a cross-book connection is apparent, optionally use `skills/knowledge/cross-book-synthesis.md`.
9. Validate and write.

## Output

- selected retention item IDs reviewed
- recall results and brief notes
- updated `retention-state.yaml`
- concise synthesis of retention status

## Confirmation policy

Auto-execute. Review updates are low-risk. Ask for confirmation only if a review would require retrieving or discussing material beyond the user's spoiler boundary.
