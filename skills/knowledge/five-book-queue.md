# Skill: five-book-queue

## Purpose

Build a coherent five-book reading sequence. This is a thin wrapper around `skills/knowledge/build-reading-queue.md` with length five and stronger sequencing guidance.

## Trigger

- "Build me my next 5-book queue."

## Steps

1. Call `skills/knowledge/build-reading-queue.md` with target length 5.
2. Ensure the sequence is coherent, not just the five highest-scoring similar books.
3. Apply the following sequencing defaults unless the user overrides:
   - Alternate or vary modes when possible (e.g., nonfiction → fiction → nonfiction).
   - Avoid placing the same author or narrow theme twice in a row.
   - Vary difficulty/length when known (a dense book may be followed by a shorter/lighter one).
   - Start with a strong next-up pick that matches current interests.
   - End with a broader or exploratory choice, possibly from outside the known library.
4. Explain the sequence briefly:
   - why each book was selected
   - how it follows the previous one or provides contrast
   - whether it is owned, wishlisted, or a new discovery

## Output

- five `reading_queue` entries in `reading-state.yaml`
- position 1 set to `next_up`
- positions 2-5 set to `queued`
- brief rationale for each slot

## Example

For a user reading *Thinking in Systems*, interested in systems/strategy, and owning *Dune*, *The Box*, and *Good Strategy Bad Strategy*:

1. Dune — fiction break and power/politics depth (`next_up`)
2. The Box — owned nonfiction; logistics/systems follow-up
3. Der Klang der Familie — music/culture palate cleanser
4. Good Strategy Bad Strategy — strategy synthesis after systems exposure
5. [discovered recommendation] — rare-event risk/uncertainty outside the current library
