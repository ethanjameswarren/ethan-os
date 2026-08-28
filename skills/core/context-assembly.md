# Skill: context-assembly

## Purpose

Assemble only the personal context needed for a given user request. Avoid loading unrelated private or sensitive domains. Preserve provenance and make context explainable.

## Input

A `core.context-request` object with:

- `intent`
- `domains`
- `entity_refs` (optional)
- `time_horizon` (optional)
- `desired_depth` (optional)
- `avoid_domains` (optional)

## Output

A `core.context-bundle` object containing:

- `current_state` — relevant current objects by domain.
- `relevant_history` — recent objects or sessions tied to the same topic/entity.
- `related_knowledge` — linked ideas or summaries.
- `active_constraints` — schedule, deadlines, goals, preferences, privacy limits.
- `preferences` — relevant user preferences.
- `provenance` — source of every loaded item.

## Implementation

The runtime can call `scripts/core/context_assembly.py` to assemble a bundle from a `core.context-request`.

```python
from context_assembly import assemble

bundle = assemble({
    "intent": "course-decision",
    "query": "Should I take this LinkedIn Learning agentic AI course?",
    "domains": ["planning", "knowledge", "career"],
    "avoid_domains": ["health", "finance", "music"],
    "desired_depth": "normal",
    "time_horizon": "now",
})
```

The assembly engine uses `scripts/core/universal_retrieval.py` to discover candidate objects, then filters, ranks, and organizes them.

## Rules

- Load from `ethan-life` only. `ethan-os` never contains personal data.
- Do not load a domain unless it is in `domains` or is clearly relevant.
- Respect `avoid_domains`.
- Use `desired_depth` to control verbosity:
  - `minimal` — current state only.
  - `normal` — current state + relevant history + constraints.
  - `deep` — add cross-domain knowledge, related ideas, and temporal patterns.
- Prefer object summaries over full object content.
- Record why each item is included.
- Never load unrelated sensitive domains (e.g., health, finance, career evidence) unless the intent explicitly requires them.

## Example

```
intent: start-learning
 domains: [knowledge, planning]
 entity_refs: ["Statistics 301"]
 desired_depth: normal
```

The bundle might include:
- current `knowledge.learning-program` for "Statistics 301" if it exists,
- active `planning.goal` related to statistics or data skills,
- relevant `knowledge.idea` about feedback loops or distributions,
- schedule constraints from `planning.baseline-schedule` if a study block is relevant,
- but not finance, health, or music data.

## Notes

This is the foundational contract. Implementations may later become smarter about retrieval, but the schema and rules remain the interface.
