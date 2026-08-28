# Skill: enrich-reading-source

## Purpose

Determine what source material is available for a book, record the access level safely, and expose retrieval instructions to reading workflows without persisting copyrighted full text.

## Input

- `source` object (`knowledge.source`)
- `reading_profile` object (`knowledge.reading-profile`) for the source, if any
- user message (e.g., "I have the PDF", "physical book", "I listened to the audiobook")
- environment context (available local files, URLs the user provides, etc.)

## Output

- Updated `knowledge.reading-profile` with:
  - `source_access`: metadata_only | model_knowledge | full_text_available
  - `content_locator`: path/URL/identifier of the accessible content, if any
  - `content_format`: pdf | epub | txt | markdown | other
  - `ingestion_status`: not_started | pending | complete | failed
  - `page_alignment`: exact | approximate | unknown
  - `last_indexed_at`: date, if content was inspected
  - `source_provenance`: human-readable description of the source and access restrictions
- Optional safe retrieval instructions for workflows

## Rules

1. Do not persist full copyrighted book text inside `ethan-life` objects.
   - Persist only: locators, page/chapter references, short excerpts necessary for discussion, user observations, derived notes.
2. Determine `source_access` in this order of preference:
   - `full_text_available`: user provides or authorizes a legitimate local digital copy (PDF, EPUB, TXT, Markdown, etc.) and access succeeds.
   - `model_knowledge`: no digital copy, but the book is well-known and reliable model knowledge is available.
   - `metadata_only`: no usable text or model knowledge beyond metadata.
3. Never claim `full_text_available` unless content was actually located and readable.
4. If a digital copy is available, attempt to identify edition/version (ISBN, publisher, file metadata) and compare to the user's edition.
   - If uncertain, set `page_alignment: approximate` or `unknown`.
   - If confident it matches, set `page_alignment: exact`.
5. When content is available, record the locator (relative path under the user's control, URL, or canonical identifier). Do not record secrets, keys, or private download links.
6. Update `ingestion_status` honestly:
   - `not_started`: no attempt yet
   - `pending`: ingestion/inspection in progress
   - `complete`: successfully inspected and ready for retrieval
   - `failed`: could not read or parse
7. Record `source_provenance` describing:
   - where the content came from (user file, public domain text, model knowledge)
   - any access restrictions or copyright notes
   - whether page alignment is trusted
8. If the user only has a physical copy or audiobook, default to `metadata_only` unless they provide extractable digital material.
9. Do not block starting or continuing a reading session because enrichment is incomplete.
10. If the user does not mention digital text, and no prior profile exists, default to `metadata_only` and proceed.

## Retrieval instructions for workflows

When `source_access == full_text_available` and `ingestion_status == complete`:

- Retrieve only the page range or section the user explicitly reports.
- For fiction with `spoiler_policy: strict_current_page`, retrieve only up to the current `spoiler_boundary` plus harmless local context.
- Do not retrieve later chapters/pages merely for convenience.
- Return short excerpts and references, not the whole section.
- Preserve provenance: mark retrieved passages as SOURCE-DERIVED.

When `source_access == model_knowledge`:

- Use reliable model knowledge plus prior user discussion.
- Treat page numbers as edition-dependent and uncertain.
- Do not imply exact knowledge of what appears on specific pages.
- Be conservative about spoilers.

When `source_access == metadata_only`:

- Rely primarily on the user's account of what they read.
- Ask open questions that let the user surface interesting material.
- Do not fabricate section content, quotes, or page-specific details.

## Question generation guidance

- `full_text_available` + `exact` alignment: questions can reference specific ideas/examples from the retrieved range.
- `full_text_available` + `approximate`/`unknown` alignment: questions should use chapter/section/user descriptions, not assume exact page contents.
- `model_knowledge`: ask broader thematic/structural questions, not "on page X...".
- `metadata_only`: ask the user what stood out, surprised them, or connected to other knowledge.
