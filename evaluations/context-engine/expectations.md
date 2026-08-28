# Context Engine Evaluation Expectations

These are deterministic behavioral expectations for the Context Engine. They are not a full LLM-as-judge harness.

## Retrieval

- Irrelevant domains are excluded when `avoid_domains` is set.
- Direct `entity_refs` return the exact object first.
- Active/current objects are preferred over historical ones.
- Cross-domain typed relationships improve retrieval.
- No query returns an empty result instead of fabricated or unrelated objects.

## Context Assembly

- `light` depth returns at most 5 relevant items.
- `deep` depth includes linked objects but stays bounded (<= 30).
- Sensitive domains are not loaded unless requested.
- Every bundle entry includes provenance.
- `current_state`, `related_knowledge`, and `active_constraints` are populated for relevant intents.

## Course Decision

- Retrieves active goals, career targets, current learning, and related projects.
- Excludes unrelated domains.
- Produces a recommendation traceable to the context bundle.

## Resume

- Career evidence is retrieved.
- Health, finance, and music are excluded.
- Claims about relevant skills have provenance.

## Sunday Planning

- Goals, projects, tasks, learning programs, and schedule constraints are included.
- Unrelated personal domains are not dumped into the context.
