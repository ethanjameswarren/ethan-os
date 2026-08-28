# Skill: spoiler-aware-discussion

## Purpose

Prevent fiction spoilers by constraining discussion to material the user has explicitly read.

## Input

- `source` object (book)
- `reading_profile` object (`knowledge.reading-profile`) for the book, if any
- `spoiler_boundary`: integer page number the user has completed
- `user_message`: current user message
- `discussion_so_far`: current conversation context
- `external_knowledge`: optional known information about the book from outside the user's reported reading

## Rules

1. Determine the effective spoiler policy in this order:
   - If `reading_profile.spoiler_policy` is set, it overrides everything.
   - If not set, default to `strict_current_page` for fiction and `known_material_ok` only if the user has explicitly mentioned prior exposure to this specific source.
2. The `spoiler_boundary` is the highest page the user has explicitly reported completing in this book. It advances only when the user reports progress.
3. For `strict_current_page`: do not reveal, imply, or confirm:
   - future plot events
   - later character developments
   - later terminology explanations
   - thematic conclusions that depend on unread material
4. For `known_material_ok`: the user is okay with material from a known adaptation or prior read, but not with book-only content beyond their current page. Ask the user to clarify the scope if uncertain.
5. For `full_spoilers_ok`: the user explicitly allows full discussion. Do not infer this from familiarity alone.
6. If the user asks a question whose answer would require information beyond the effective boundary:
   - State the boundary and ask if they want to open it.
   - Offer to discuss what is known up to the current page.
7. Do not use model knowledge about the book to fill in gaps about later material unless `full_spoilers_ok` is active.
8. Speculation about the future is allowed only when clearly framed as speculation and grounded on material up to the spoiler boundary.
9. If the user says something like "around page 40" or "somewhere in chapter 3", record it as an approximate reference in the session but do not advance the spoiler boundary unless they explicitly confirm a completed page.
10. **Retrieval boundary**: if `source_access == full_text_available` and content is retrieved to ground discussion, the retrieval itself must respect the spoiler policy. For `strict_current_page`, retrieve only up to the current `spoiler_boundary` plus harmless local context needed to interpret the current passage. Do not retrieve later chapters or substantive future material and then merely avoid mentioning it.

## Output

- `safe_to_discuss`: true | false
- `boundary_note`: short note if progress is approximate or ambiguous
- `response_guidance`: how to answer or deflect without spoiling
