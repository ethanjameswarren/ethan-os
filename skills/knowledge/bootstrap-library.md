# Skill: bootstrap-library

## Purpose

Seed or update a user's entire reading library from a single natural-language list. Avoid requiring one-at-a-time entry.

## Input

A user message such as:

- "Here are the books I own: Thinking in Systems, Dune, The Box."
- "These are books I've already read: Atomic Habits, The Psychology of Money."
- "Add these to my wishlist: Skunk Works, Fooled by Randomness."
- "I own all of these physically."
- "I finished these years ago: Dune, Neuromancer."

## Steps

1. Parse the list of books from the user's message. Accept common separators: commas, newlines, "and", "also".
2. For each book:
   a. Normalize title/author for matching.
   b. Search `ethan-life/domains/knowledge/sources/` for an existing `knowledge.source` with `source_type: book`.
   c. Use `skills/knowledge/resolve-book-edition.md` to match against existing sources and avoid duplicate logical books.
   d. If no source exists, create a new `knowledge.source` with `source_type: book`.
3. Apply ownership/reading status inference from the surrounding message context:
   - "I own..." / "I bought..." / "I have..." → `ownership_status: owned_physical` or `owned_digital` (infer format if mentioned)
   - "physical / paperback / hardcover" → `owned_physical`
   - "Kindle / ebook / on my phone" → `owned_digital`
   - "borrowed / from the library" → `borrowed`
   - "wishlist / want to read / buy-list" → `wishlist`
   - "finished / read" → `status: finished`
   - "currently reading / reading now" → `status: reading`
   - "started" → `status: reading`
   - "paused" → `status: paused`
   - "abandoned / DNF" → `status: abandoned`
   - no status mentioned → `status: unread` (if owned/wishlist), or keep existing
4. If a book's status is `reading`, consider adding it to `reading-state.yaml` active_books if not already present.
5. Track any unresolved items (ambiguous title, no author, conflicting existing data) and ask the user about them after the bulk operation.
6. Summarize what was created, updated, or unresolved.

## Output

- list of created/updated source IDs
- inferred ownership_status and status for each
- any unresolved items requiring user clarification

## Rules

- Do not create duplicate logical books. Prefer updating an existing source's edition/ownership/format rather than creating a new one.
- If the message contains both ownership and reading status context, apply it to all listed books unless individual cues contradict it.
- Do not automatically mark discovered external books as owned or wishlist; set `not_owned` or `unknown` if only the title is known.
- Preserve existing `current_page` authority in `reading-state.yaml`.
