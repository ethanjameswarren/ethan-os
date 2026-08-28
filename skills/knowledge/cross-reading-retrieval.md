# Skill: cross-reading-retrieval

## Purpose

Answer questions across the user's entire reading history by retrieving from Sources, Reading Sessions, Ideas, Summaries, Reviews, Retention state, and typed relationships.

## Supported queries

- "What have I learned about incentives?"
- "What have books taught me about strategy?"
- "What did I think about Dune's politics?"
- "What ideas have I connected to work?"
- "Where have I disagreed with authors?"
- "What themes keep coming up across books?"
- "Show me ideas from Thinking in Systems that relate to Good Strategy/Bad Strategy."

## Retrieval sources

1. `knowledge.source` — book metadata, tags, ownership/reading status, ratings
2. `knowledge.reading-session` — user observations, discussion summaries, extracted insights, predictions, connections
3. `knowledge.idea` — durable reusable ideas with positions and confidence
4. `knowledge.summary` — personal syntheses, 30-second / 5-minute / detailed sections
5. `knowledge.review` — flagged items, contradictions, low-confidence notes
6. `retention-state.yaml` — current confidence and recall history
7. Typed `links` between objects

## Retrieval principles

1. Preserve provenance. Every answer should be traceable back to source IDs and session IDs.
2. Prefer user-derived observations and AI synthesis from sessions over generic summaries.
3. Do not rely only on final book summaries. Use session-level captures when available.
4. Respect fiction spoiler boundaries. Do not retrieve or reveal material beyond the user's allowed boundary.
5. Distinguish source claims from the user's interpretation and from AI synthesis.
6. When the answer spans multiple books, organize by theme or question rather than dumping a list.

## Output

- concise answer with inline citations (`source_id`, `session_id`, `idea_id`)
- relevant object IDs
- optional follow-up question to deepen the query

## Example

Query: "What have I learned about incentives?"

Response:
- From *Atomic Habits* (`src-20260115-001`, `idea-20260115-001`): behavior is shaped by systems, not goals — position `agree`, confidence `high`.
- From *Thinking in Systems* session (`rs-20260827-001`): feedback loops in labor planning made you notice that final numbers hide upstream inputs.
- You connected incentives to identity in session `rs-20260115-002`.
- No strong disagreement captured yet.
