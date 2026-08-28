# Workflow: update-reading-profile

## Purpose

Update a book's reading profile mid-read from natural-language statements about familiarity, goals, or spoiler preferences, without restarting the book.

## Triggers

- "I've actually read this before."
- "You can spoil Dune, I know the whole story."
- "Don't spoil anything beyond the movies."
- "I want to focus more on the ecology."
- "Let's keep the questions lighter."
- "I just saw the film, so I know the broad strokes."

## Steps

1. Resolve the active source from the user's message or reading state.
   - If exactly one active book exists and no title is given, use it.
   - If multiple active books exist and the reference is ambiguous, ask which one.
2. Load the existing `knowledge.reading-profile` for the source, or create one if missing.
3. Infer updated fields from the user's message using `skills/knowledge/pre-reading-assessment.md`.
4. Update the profile's `updated_at` and provenance note describing what changed.
5. Validate and write to `ethan-life/domains/knowledge/reading-profiles/` (as `reading-profile-<source-id>.md` or similar stable filename).
6. Confirm the change concisely.

## Output

- updated or created `knowledge.reading-profile` ID
- summary of what changed

## Confirmation policy

Auto-execute. Updating a reading profile is low-risk and reversible.
