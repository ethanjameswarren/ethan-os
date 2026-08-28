# Skill: cross-book-synthesis

## Purpose

Surface meaningful connections across books the user has read, when both concepts have already been encountered.

## When to use

- During a review of a retention item from one book, when another book has a related idea.
- During a reading discussion, when the current observation clearly relates to a prior book's concept.
- Sparingly; connections should be genuinely useful, not forced.

## Rules

1. Only suggest connections when the user has actually encountered both ideas.
2. Prefer asking the user to articulate the connection before explaining it.
3. Persist meaningful relationships with typed `links` and a contextual justification.
4. Do not fabricate quotes or specific page references.
5. For fiction, respect spoiler boundaries when discussing prior books.

## Example prompts

- "How does Meadows' idea of leverage points relate to Rumelt's idea of a guiding policy?"
- "This stock/flow idea seems similar to something you noticed in *Atomic Habits*. Do you see a connection?"
- "Both books talk about identity. How do their framings differ?"

## Output

- `suggested_connection`: description of the relationship
- `source_items`: retention item or idea IDs involved
- `persist`: whether to create a `related_to` or `supports` link between objects
