# Workflow: discuss-reading

## Purpose

Discuss a book without a new page progress report, capturing reactions, predictions, connections, or questions.

## Triggers

- "The Bene Gesserit seem sketchy"
- "This reminds me of work"
- "I don't buy his argument here"
- "What do you think about this idea?"

## Steps

1. Resolve the active source.
   - If the user references a title or enough context, match it.
   - If exactly one active book exists and no title/context points elsewhere, use it.
   - If multiple active books are active and the reference is ambiguous, ask which one.
2. Load the current `spoiler_boundary` from `reading-state.yaml` and the `knowledge.reading-profile` for the source.
3. If mode is `fiction`, apply `skills/knowledge/spoiler-aware-discussion.md` strictly, honoring the profile's `spoiler_policy` and retrieval boundary.
4. If the user asks about specific content and `source_access == full_text_available` with `ingestion_status == complete`, retrieve only the relevant portion within the spoiler boundary (for fiction) or current page range (for nonfiction). Mark retrieved material as SOURCE-DERIVED.
5. If the user offers an observation but did not explicitly recall from a recent section, optionally use `skills/knowledge/active-recall.md` to ask what they remember; skip if they have already volunteered recall content.
6. Engage conversationally. Do not dump questions. Follow the user's observation.
7. If the discussion produces material worth preserving, create or append to the most recent `knowledge.reading-session` for this source (usually the one referenced by `last_session_id`). If no session exists, create one covering the current spoiler boundary pages.
8. Use `skills/knowledge/reading-knowledge-extraction.md` to extract structured knowledge.
9. If the discussion yields durable takeaways, run `skills/knowledge/compress-session.md` and update `ethan-life/domains/knowledge/retention-state.yaml` via `skills/knowledge/schedule-review.md`.
10. Update `reading-state.yaml` `last_reading_at` and `last_session_id`.
11. Validate and write.

## Output

- updated or created `knowledge.reading-session` ID
- any promoted `knowledge.idea` IDs
- concise synthesis of what was captured

## Confirmation policy

Auto-execute. Ask for confirmation only on relationship changes that imply contradiction or belief revision.
