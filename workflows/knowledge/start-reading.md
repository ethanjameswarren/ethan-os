# Workflow: start-reading

## Purpose

Begin reading a new book and establish its canonical source, active reading state, and reflection mode.

## Triggers

- "I'm starting Dune"
- "I'm reading Thinking in Systems"
- "Start a reading session for Good Strategy Bad Strategy"

## Steps

1. Resolve the book title from the user's input.
2. Search `ethan-life/domains/knowledge/sources/` for an existing `knowledge.source` with matching title or `source_type: book`.
3. If no source exists, create a new `knowledge.source` with:
   - `source_type: book`
   - `status: reading`
   - `schema: knowledge.source`, `schema_version: 1`
   - `reading_mode` classified from title/context (nonfiction / fiction / music_history_culture / other)
   - `started_at`: today's date
   - provenance noting the start-reading workflow
4. If a source exists but is `finished`, treat this as a new reading cycle:
   - Update `status` to `reading`.
   - Update `started_at` to today's date.
   - Optionally clear or archive prior reading state in a note.
5. Look up `knowledge.reading-profile` for this source in `ethan-life/domains/knowledge/reading-profiles/`.
6. If no profile exists, run `skills/knowledge/pre-reading-assessment.md`:
   - Create a `knowledge.reading-profile` object linked to the source.
   - Infer fields from natural language; ask at most 1-3 follow-up prompts.
   - For fiction, establish `spoiler_policy` explicitly if not inferable.
7. Run `skills/knowledge/enrich-reading-source.md` to determine source access:
   - If the user provided a digital copy, record `source_access: full_text_available`, format, locator, and alignment confidence.
   - If only physical/audiobook, set `source_access: metadata_only`.
   - If model knowledge is appropriate and no digital copy exists, set `source_access: model_knowledge`.
   - Do not block the session if enrichment fails or is incomplete; default to `metadata_only`.
8. Add/update the book in `ethan-life/domains/knowledge/reading-state.yaml` with:
   - `source_id`
   - `status: active`
   - `current_page`: 0 or user-provided value
   - `last_completed_range`: null
   - `spoiler_boundary`: same as `current_page`
   - `last_reading_at`: today's date
   - `last_session_id`: null
9. If the user did not provide a current page or reading mode, ask one concise follow-up:
   - "What page are you starting on?"
   - "Is this fiction, nonfiction, music history/culture, or something else?" (only if classification is uncertain)
10. Return a concise confirmation: title, mode, source access, status, and any profile summary used.

## Output

- created/updated `knowledge.source` ID
- `reading-state.yaml` entry
- follow-up question(s) if needed

## Confirmation policy

Auto-execute. Starting a book is low-risk and reversible.
