# Cross-Domain Reasoning Evaluation Expectations

Static behavioral expectations for `scripts/core/cross_domain_reasoning.py`.

## Provenance

- Every material finding references `object_ids` from the context bundle.
- No personal facts are introduced without source objects.

## Domain boundaries

- Reasoning only uses objects present in the bundle.
- Excluded domains are never used as evidence.

## Goals

- Goals can be focal objects for reasoning.
- `connection` findings can trace from goal to supporting objects.
- `what supports this?` traces reverse from goal to supporting work.
- `why?` traces from a task or project toward the goal it serves.

## Finding types

- `transfer_opportunity` is produced when learning/knowledge can apply to a project or career evidence.
- `overlap` is produced when two learning sources cover similar concepts.
- `gap` / `evidence_gap` is produced when a goal, project, or job target lacks expected support.
- `tradeoff` / `conflict` is produced when active commitments compete.
- `priority_mismatch` is produced when an active goal lacks active execution.

## Activity vs outcome

- Task and session completion is treated as activity.
- Evidence, metrics, and observed results are treated as outcome.
- No task counts are converted into goal percentages.

## Boundedness

- Default mode returns 3–7 high-value findings.
- Deep mode returns more but stays bounded.
- Findings are sorted by confidence and cross-domain value.

## No autonomous action

- The reasoning layer does not create, modify, schedule, or purchase anything.
- `suggested_action` is advisory and must be routed through the appropriate domain workflow.

## Anti-optimization

- Recreation, curiosity, and inherently valuable activity are not marked as defective for lacking a goal.
- `stale_assumption` findings are only generated for meaningful active objects that appear isolated.
