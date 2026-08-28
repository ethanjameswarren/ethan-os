# Workflow: continue-reading

## Purpose

Record reading progress, continue the guided discussion, and persist the session's knowledge.

## Triggers

- "Finished pages 1-15"
- "Read through page 42"
- "Did another chapter"
- "I got to page 80"
- "Just finished 16-32"
- "Did 16-32" (when a book is active)

## Steps

1. Resolve the active source.
   - If the user provided a title, match it against `reading-state.yaml` active entries and `knowledge.source` titles.
   - If exactly one active book exists and no title is given, use it.
   - If multiple active books exist and no title is given, ask which one and stop.
   - If no active book exists, suggest running `start-reading`.
2. Parse the page range from the user's message. If only one page is given, treat it as `end` and infer `start` from `current_page + 1` if reasonable; otherwise ask.
3. Update `reading-state.yaml` for this source:
   - `current_page`: end of the completed range
   - `last_completed_range`: `{ start, end }`
   - `last_reading_at`: today's date
   - `spoiler_boundary`: end of the completed range (only advances forward)
   - `status: active`
   - `last_session_id`: set after session creation
4. Load the `knowledge.reading-profile` for this source and determine `source_access`:
   - If `full_text_available` and `ingestion_status == complete`:
     - Retrieve the portion corresponding to the reported page range.
     - If `page_alignment` is not `exact`, treat page numbers as approximate and prefer chapter/section/user descriptions.
     - For fiction with `strict_current_page`, retrieve only up to the current `spoiler_boundary` plus harmless local context; never retrieve later substantive content.
     - Record retrieved excerpts/locators in the session with SOURCE-DERIVED provenance.
   - If `model_knowledge`, use reliable general knowledge plus prior user discussion; do not imply exact page contents.
   - If `metadata_only`, rely on the user's account and ask open questions.
5. Create a `knowledge.reading-session` object with:
   - `source_id`
   - `session_date`: today
   - `pages`: `{ start, end }`
   - `spoiler_boundary_at`: end of range
   - `reading_mode`: from source
   - `user_observations`: any observations the user already volunteered
   - source-derived references/excerpts (only if content was actually retrieved)
   - provenance linking to this workflow and, if applicable, to the retrieved content
6. Run `skills/knowledge/active-recall.md` BEFORE explaining or summarizing the section:
   - Ask a light retrieval prompt.
   - If the user already described what stood out, use that as the recall output and skip the prompt.
   - Accept "not much" as valid.
7. Use `skills/knowledge/elaborate-concept.md` for 0-2 follow-ups that deepen understanding, based on the user's recall and the discussion direction.
8. Load skill `skills/knowledge/guided-reading-reflection.md` to generate 2-4 adaptive questions based on the new range, mode, prior sessions, reading profile, and available source material.
   - If full text with exact alignment is available, questions can reference specific content from the range.
   - If only metadata or approximate alignment, keep questions general and user-centered.
9. If mode is `fiction`, load `skills/knowledge/spoiler-aware-discussion.md` and constrain all responses to the `spoiler_boundary`.
10. Engage in conversational discussion, following interesting answers. Stop when the user indicates done ("that's it", "save that", "done", changes subject).
11. When ending, run `skills/knowledge/reading-knowledge-extraction.md` to populate the session with structured insights.
12. Run `skills/knowledge/compress-session.md` to identify 0-3 durable takeaways.
    - Promote strong, reusable insights to `knowledge.idea` objects. Link them to the source via `sourced_from`.
    - For session-level insights worth reviewing but not globally reusable, assign stable `insight_id`s and `retention_priority`.
13. Run `skills/knowledge/schedule-review.md` to update `ethan-life/domains/knowledge/retention-state.yaml`:
    - Add/update retention items for high/normal-priority takeaways.
    - Do not schedule `low` priority items unless the user explicitly overrides.
    - If a takeaway already has an active retention item, leave it unchanged unless the session adds new significance.
14. Optionally use `skills/knowledge/cross-book-synthesis.md` to suggest connections to prior books/ideas if the session surfaces a clear link.
15. Update `reading-state.yaml` `last_session_id`.
16. Validate all objects and write to `ethan-life`.

## Output

- updated `reading-state.yaml`
- created/updated `knowledge.reading-session` ID
- any created `knowledge.idea` IDs
- updated `retention-state.yaml` with scheduled review items
- brief synthesis of what was captured

## Confirmation policy

Auto-execute. Creating captures, sessions, and extracted insights is low-risk.
- Ask for confirmation before promoting more than 3 ideas in one session.
- Ask for confirmation before creating relationships that imply contradictions or belief changes.
