# Skill: cross-domain-reasoning

## Purpose

Interpret a `core.context-bundle` to identify meaningful cross-domain patterns: connections, overlaps, gaps, conflicts, dependencies, transfer opportunities, priority mismatches, and unsupported assumptions.

## Input

- A `core.context-bundle` from `scripts/core/context_assembly.py`.
- `intent` for the reasoning session (e.g., `course-decision`, `sunday-review`, `tailored-resume`, `goal-review`, `ask`).
- Optional `focal_id` — a goal, object, or question to center the reasoning.
- Optional `modes` — list of finding types to compute. If omitted, all applicable modes run.

## Output

A list of `findings`. Each finding contains:

- `type`
- `statement`
- `object_ids`
- `domains`
- `evidence`
- `confidence` (`high`, `medium`, `low`)
- `why_it_matters`
- `implication` (optional)
- `suggested_action` (optional)

## Finding types

- `connection` — explicit or inferred relationships between objects.
- `transfer_opportunity` — learning, idea, or project that could be applied in another domain.
- `overlap` — similar material in two learning sources or programs.
- `gap` / `evidence_gap` — a missing supporting element.
- `conflict` / `tradeoff` — competing commitments or resources.
- `priority_mismatch` — active priority with little active execution.
- `dependency` — one object depends on another being completed first.
- `stale_assumption` — a meaningful active object without clear context.

## Rules

- Every material claim must trace back to the context bundle.
- Do not invent personal facts.
- Distinguish fact, inference, and suggestion.
- Preserve provenance in `evidence`.
- Stay bounded. Default to 3–7 useful findings.
- Do not create, modify, or schedule anything automatically.
- Excluded domains must not be used in findings.

## Implementation

Run `scripts/core/cross_domain_reasoning.py`:

```python
from cross_domain_reasoning import reason

findings = reason(
    bundle,
    focal_id="goal-ai-engineering",
    modes=["transfer_opportunity", "overlap", "gap", "tradeoff"],
    limit=7,
)
```

## Confidence

- `high` — explicit typed relationship or direct chain.
- `medium` — shared tags, concepts, or one-hop inference.
- `low` — heuristic or broad pattern.
