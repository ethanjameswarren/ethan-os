# Workflow: book-recommendation

## Purpose

Recommend books to read or buy based on the user's library, reading history, and stated preferences.

## Triggers

- "What should I read next?"
- "What should I buy next?"
- "What do I already own that I should read?"
- "Give me something completely different."
- "What should I read after Dune?"
- "Show my reading library."

## Steps

1. Parse the query intent:
   - `read_next`: general next-read recommendation
   - `buy_next`: purchase recommendation
   - `owned_backlog`: read something already owned
   - `diversify`: something different from recent reading
   - `after_book`: follow-up to a specific finished/current book
   - `library_overview`: summarize the library state
2. Load all `knowledge.source` objects with `source_type: book` from `ethan-life/domains/knowledge/sources/`.
3. Load `ethan-life/domains/knowledge/reading-state.yaml` and `ethan-life/domains/knowledge/retention-state.yaml`.
4. Load relevant `knowledge.reading-session`, `knowledge.idea`, and `knowledge.summary` objects to build a lightweight reading profile.
5. Run `skills/knowledge/recommend-next-book.md` to generate candidates and explanations.
   - For `read_next`, consider owned unread, wishlist, and external discoveries.
   - For `buy_next`, consider wishlist and not-owned books; exclude owned unless edition matters.
   - For `owned_backlog`, restrict to owned unread/paused books.
   - For `diversify`, bias away from recent authors, themes, and reading modes.
   - For `after_book`, use the named book's themes, user reactions, and retained ideas as the primary signal.
6. If `library_overview`, return sections:
   - Reading now
   - Owned unread
   - Wishlist
   - Finished
   - Paused
   - Recently added
   - Recommended / discovered
7. Present 1-5 recommendations with explainable reasons. Do not fabricate user preferences where evidence is weak.
8. Capture user feedback:
   - "I already read that." → update `status` to `finished` if not already.
   - "I own that." → update `ownership_status`.
   - "That sounds boring." / "Not interested." → record negative signal.
   - "Add to wishlist." / "Buy-list it." → create/update source with `ownership_status: wishlist`.
   - "I want something lighter/heavier/fiction/nonfiction." → apply context to future recommendations.
9. Optionally record the recommendation in the source's `user_interest_notes` or provenance if it becomes wishlisted/owned.
10. Validate and write any updated objects to `ethan-life`.

## Output

- list of recommendations with titles, authors, reasons, and expected actions
- any created/updated `knowledge.source` IDs (e.g., wishlist additions)
- concise synthesis of why each was recommended

## Confirmation policy

Auto-execute recommendations. Ask for confirmation before creating or updating a source if the recommendation would change important existing state (e.g., marking a finished book as unread).
