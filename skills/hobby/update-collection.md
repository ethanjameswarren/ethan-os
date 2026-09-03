# Skill: update-collection

## Purpose

Update one or more `hobby.collection-item` records based on a concise status change.

## Input

- Collection item title or ID.
- One or more fields to change: `purchase_status`, `assembly_status`, `painting_status`, `magnetization_status`, `quantity`, `events`, `notes`.

## Output

- Updated collection item file.
- A brief confirmation of the change and any downstream consequences.

## Instructions

1. Locate the matching collection item by ID or title.
2. Apply only the explicitly stated changes.
3. Append a dated event to `events` when the change represents a meaningful milestone (acquired, assembled, primed, painted, completed, sold, etc.).
4. If `assembly_status` changes to `assembled` or `partially_assembled` and `magnetization_status` is `planned_review`, surface a reminder to resolve the magnetization decision.
5. If the change implies a narrative consequence (e.g., a unit completed and named), ask whether to create a `hobby.lore-candidate`.
6. Return the updated record summary.
