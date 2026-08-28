# Workflow: finish-reading

## Purpose

Close a book reading cycle by reviewing accumulated sessions, capturing final reflections, and producing a user-grounded synthesis.

## Triggers

- "I finished Dune"
- "Done with the book"
- "Finished Thinking in Systems"

## Steps

1. Resolve the source from the user's message or the active reading state.
2. Gather all `knowledge.reading-session` objects for the source.
3. Review existing `knowledge.idea` objects linked to the source.
4. Ask only high-value final reflection questions that are not already answered in the sessions:
   - What do you think the book was ultimately saying?
   - What changed in how you think?
   - What are the 1-3 ideas you expect to remember?
   - What did you disagree with?
   - Would you recommend it? Rating?
5. Capture the user's final reflection in the most recent reading session or create a final `knowledge.reading-session` if needed.
6. Update `knowledge.source`:
   - `status: finished`
   - `finished_at`: today's date
   - `rating`: if provided
7. Update `reading-state.yaml`:
   - `status: finished` for this source
   - keep `current_page` and `spoiler_boundary` at their final values
   - `last_reading_at`: today
8. If `source_access == full_text_available` and `ingestion_status == complete`, retrieve the full source text or table of contents only to support summarization of sections the user has actually read. Do not use full-text access to override the user's own words.
9. Create or update the canonical `knowledge.summary` for the source using `skills/knowledge/generate-summary.md`, but base it primarily on the accumulated reading-session discussions, user observations, extracted insights, and promoted ideas. Do not fill gaps with a generic model summary.
10. Inspect `ethan-life/domains/knowledge/retention-state.yaml` for items linked to this source:
    - Identify strongest retained ideas (`current_confidence: high`, multiple successful recalls).
    - Identify weak or unreviewed items (`current_confidence: low`, `failed_recalls > 0`, `last_reviewed_at: null`).
    - Identify important items the user explicitly marked as `high` priority.
    - Offer to do a brief retention review of 0-3 selected items, respecting spoiler policy for fiction.
    - Important durable ideas continue into long-term review even though the book is finished.
11. Optionally create a `knowledge.review` if there are contradictions, low-confidence items, or open questions worth revisiting.
12. Validate and write.

## Output

- updated `knowledge.source` with finished status and rating
- updated `reading-state.yaml`
- created/updated `knowledge.summary` ID
- any final `knowledge.idea` promotions
- updated `retention-state.yaml` (continued long-term review, final retention review offered)
- concise synthesis

## Confirmation policy

Auto-execute. Updating the summary with material semantic change may require confirmation per existing policy, but finishing a book and synthesizing the user's own accumulated material is expected behavior.
