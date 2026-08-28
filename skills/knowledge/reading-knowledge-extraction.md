# Skill: reading-knowledge-extraction

## Purpose

Extract structured knowledge from a guided reading discussion without over-producing objects or losing provenance.

## Input

- `source` object (book)
- `reading_session` object in progress or completed
- `discussion` transcript or summary of user/agent turns
- `prior_ideas` list of existing knowledge.idea objects linked to the source
- `prior_summaries` list of existing knowledge.summary objects linked to the source

## Output

- Updated `reading_session` with:
  - `user_observations`
  - `extracted_insights`
  - `predictions`
  - `open_questions`
  - `applications`
  - `connections`
  - `notable_passages`
- Optional list of `candidate_ideas` to promote to `knowledge.idea`

## Extraction rules

1. Preserve the user's actual wording in `user_observations`. Do not replace user language with polished paraphrase.
2. `discussion_summary` must be clearly labeled as AI synthesis and must not be presented as the user's thought.
3. Extract `extracted_insights` at the session level when they are useful but not yet durable enough for the global idea graph.
4. Promote to `knowledge.idea` only when the insight is:
   - reusable outside the immediate passage or book,
   - meaningfully distinct from existing ideas,
   - likely useful for later retrieval.
5. Record source/belief separation on any promoted idea:
   - `claim`: what the source says
   - `interpretation`: the user's interpretation
   - `position`: agree / disagree / neutral / exploring
   - `confidence`: low / medium / high
6. For `connections`, reference existing objects by ID when possible. Include a short contextual justification.
7. For `predictions`, tag them as `resolved: false` initially and resolve later if confirmed by reading.
8. Do not invent page references. Use the page range from the session or explicit user-provided references.
9. Do not create dozens of trivial insights. Use judgment.

## Promotion rule

If fewer than 1-3 strong candidate ideas emerge from a session, leave them in `extracted_insights` rather than forcing durable idea creation.
