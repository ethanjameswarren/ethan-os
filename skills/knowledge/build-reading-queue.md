# Skill: build-reading-queue

## Purpose

Build a coherent reading queue from the user's library, goals, and current state. A queue is a lightweight ordered list of source IDs stored in `reading-state.yaml`, not a separate domain.

## Input

- All `knowledge.source` objects with `source_type: book`
- `reading-state.yaml` active_books and reading_queue
- `knowledge.reading-profile` objects
- Optional user constraints: "after Dune", "mostly nonfiction", "mix fiction", "make it 5 books", etc.

## Output

- Updated `reading-state.yaml` `reading_queue` list with:
  - `source_id`
  - `queue_position` (1 = next up)
  - `status`: queued | next_up | recommended | removed
  - `reason`: short note
- Brief explanation of why the sequence works

## Queue design principles

1. **Coherence over pure score.** The queue is a sequence, not a top-N list. Avoid five nearly identical books in a row.
2. **Prefer owned unread books** to reduce unnecessary purchases, but do not let ownership dominate fit.
3. **Balance modes and themes** when the user's goals are broad:
   - alternate fiction/nonfiction if the user reads both
   - vary depth/length when known
   - avoid clustering the same author or narrow theme unless requested
4. **Honor user overrides.** A user saying "put Dune next" should set Dune as `next_up` regardless of other signals.
5. **Include wishlist or not-owned books when appropriate.** If the user asks for a queue and lacks strong owned candidates, include discovered recommendations.
6. **Limit length.** Default to a short queue (3-5 books). The user can extend it.
7. **Do not remove active books.** If a book is currently `reading` in `active_books`, it is not removed from the queue; it may be skipped in queue suggestions until finished.

## Steps

1. Determine desired queue length from user request (default 5).
2. Filter candidates:
   - exclude finished and abandoned books unless the user explicitly wants to revisit
   - exclude books the user has explicitly removed from the queue
   - include owned unread, paused, wishlist, and strong discovered recommendations
3. Build a derived reading profile from recent sessions, ideas, ratings, and goals.
4. Score candidates for fit, ownership, and diversity.
5. Assemble an ordered sequence that varies mode/theme/difficulty and respects overrides.
6. Set position 1 as `next_up`; the rest as `queued`.
7. Write updated `reading-state.yaml`.

## Updating the queue

- "Put Dune next." → set Dune to `next_up`; shift others if necessary.
- "Move Good Strategy after Dune." → reorder around the named anchor.
- "Remove this from the queue." → set the entry `status: removed` or delete it.
- "Build me my next 5-book queue." → replace/extend the queue with a coherent 5-book sequence.

## Example

For a user currently reading *Thinking in Systems* with an interest in systems and strategy, owned copies of *The Box* and *Good Strategy Bad Strategy*, and wishlisted *Skunk Works*:

1. Dune — next_up, fiction break after dense nonfiction
2. The Box — owned, systems/logistics follow-up
3. Skunk Works — wishlist, engineering/innovation systems story
4. Good Strategy Bad Strategy — strategy synthesis
5. A newly recommended book outside the known library — broader perspective
