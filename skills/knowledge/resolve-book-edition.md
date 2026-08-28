# Skill: resolve-book-edition

## Purpose

Prevent duplicate logical books when adding or updating library entries, while still distinguishing meaningful editions/formats when necessary.

## Logical work vs manifestation

- **Logical work**: a distinct book, usually identified by title + author.
  - Example: *Dune* by Frank Herbert.
- **Manifestation / edition**: a specific version (paperback, ebook, audiobook, revised edition, translation).
  - Example: *Dune* (Ace 2005 paperback), *Dune* audiobook narrated by Scott Brick.

## Resolution rules

1. **Default: one source per logical work.**
   - If a source already exists with the same normalized title and author, update its `ownership_status`, `format`, `edition`, etc., rather than creating a new source.
   - If the new item is a different format of the same work, add/update `ownership_status` and `format` on the existing source (e.g., mark as both `owned_physical` and `owned_digital` if appropriate).

2. **Create a new source only when there is a meaningful distinction:**
   - clearly different edition that affects page alignment (e.g., revised edition, translation)
   - audiobook/dramatization treated as a separate work by the user
   - user explicitly wants to track multiple copies
   - different ISBN with materially different content

3. **Use ISBN as strongest identifier when available.**
   - If ISBN matches an existing source, merge to that source.
   - If ISBN is missing, fall back to normalized title + author.

4. **Normalize before matching:**
   - lowercase titles
   - remove leading "the " / "a " only when it creates mismatch
   - strip extra whitespace, punctuation variants, subtitles in parentheses unless they change the work
   - author names: normalize order and initials when confident

5. **Preserve user nuance.**
   - If the user says "I have the revised edition of Thinking in Systems," store edition notes and set `page_alignment: approximate` if the existing source was a different edition.
   - Do not silently overwrite `page_alignment` from exact to approximate without noting it.

6. **Avoid creating many sources for the same book.**
   - A paperback + Kindle copy of the same book should generally be one `knowledge.source`.
   - A first edition and a revised edition may be one source if content is substantially the same; if the user cares about the difference, allow two.

## Output

- `resolved_source_id`: existing or newly created source ID
- `action`: merge | create | update
- `notes`: any edition/alignment warnings
