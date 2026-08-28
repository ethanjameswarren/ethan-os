# Workflow: reading-status

## Purpose

Answer questions about current reading state, progress, history, and cross-book connections.

## Triggers

- "What am I reading?"
- "Where am I in Dune?"
- "What have I thought about Thinking in Systems so far?"
- "What books have I finished?"
- "What ideas from books have I connected to work?"

## Steps

1. Parse what the user is asking for:
   - current active books
   - progress in a specific book
   - history of thoughts/sessions for a book
   - finished books
   - library overview (owned, wishlist, unread, finished, paused, abandoned)
   - cross-source connections or ideas
   - due retention reviews
   - retention strength for a book/concept
   - concepts the user is struggling with
   - most important learned ideas
2. For library overview queries ("What books do I own?", "Show my reading library"), load all `knowledge.source` objects with `source_type: book` and group by `ownership_status` and `status`. Route full "Show my reading library" to `workflows/knowledge/book-recommendation.md` for a formatted overview.
3. Read `ethan-life/domains/knowledge/reading-state.yaml`.
4. Read relevant `knowledge.source` and `knowledge.reading-session` objects from `ethan-life`.
5. For retention queries, read `ethan-life/domains/knowledge/retention-state.yaml` and the referenced `knowledge.idea` or `knowledge.reading-session` objects. Use `skills/knowledge/surface-due-reviews.md` to select due items.
6. For cross-source queries, read `knowledge.idea` and `knowledge.summary` objects and their `links`.
7. For library/statistics queries ("Show my reading library", "What have I finished this year?"), load all book sources and use `skills/knowledge/reading-stats.md` to produce useful summaries.
8. Answer concisely with citations by object ID.
8. If no matching active book, retention item, or library entry exists, say so and offer to start one, add one, or review.

## Output

- concise status or retrieval answer
- relevant object IDs
- optional follow-up prompt (e.g., "Want to continue?")
