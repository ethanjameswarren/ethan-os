# Workflow: manage-book-library

## Purpose

Add or update a book in the library from natural-language statements about ownership, wishlist, reading status, or format, without requiring a form.

## Triggers

- "I bought The Box."
- "I own Dune already."
- "Add Fooled by Randomness to my wishlist."
- "I want to read Skunk Works eventually."
- "I finished The Psychology of Money years ago."
- "I don't own this one."
- "I have this on Kindle."
- "I borrowed this from someone."
- "Mark Thinking in Systems as paused."

## Steps

1. Resolve the book title/author from the user's input.
2. Search `ethan-life/domains/knowledge/sources/` for an existing `knowledge.source` with matching title or `source_type: book`.
3. If no source exists:
   - Create a new `knowledge.source` with `source_type: book`.
   - Set `status` and `ownership_status` from inference.
   - Fill known metadata (author, ISBN, year) if available from user input or reliable external lookup.
   - Record provenance noting this workflow.
4. If a source exists, update fields only where the user provides new information or changes status:
   - `ownership_status`
   - `status` (reading lifecycle)
   - `format`, `acquired_at`, `acquisition_source`
   - `started_at`, `finished_at`, `rating`
   - `tags`, `user_interest_notes`
5. Infer ownership and reading status from natural language:

   | user cue | ownership_status | status |
   |----------|------------------|--------|
   | "I bought..." / "I own..." / "I have this" | owned_physical or owned_digital (infer format) | unread if not stated otherwise |
   | "on Kindle" / "ebook" / "PDF" | owned_digital | unread |
   | "borrowed" / "from the library" | borrowed | unread |
   | "wishlist" / "want to buy" / "want to read eventually" | wishlist | unread |
   | "finished" / "read years ago" | keep existing or unknown | finished |
   | "abandoned" / "DNF" | keep existing | abandoned |
   | "paused" | keep existing | paused |
   | "don't own" / "not owned" | not_owned | keep existing |

6. Ask for clarification only if both `ownership_status` and `status` remain ambiguous after inference.
7. If the book is being added as wishlist or not-owned, do not create a reading-profile or reading-state entry unless the user starts reading.
8. Validate and write to `ethan-life`.

## Output

- created/updated `knowledge.source` ID
- inferred `ownership_status` and `status`
- concise confirmation

## Confirmation policy

Auto-execute. Adding or updating library metadata is low-risk. Ask for confirmation only when an update would overwrite important existing data (e.g., changing a finished book back to unread).
