# Workflow: update-paint-inventory

## Purpose

Add, remove, or change the status of paints, brushes, and tools.

## Trigger

- "I bought Leadbelcher."
- "My Nuln Oil is empty."
- "I picked up a fine detail brush."

## Inputs

- Supply name/type and status change.

## Outputs

- New or updated `hobby.paint-supply` file.

## Steps

1. Locate the existing supply by ID or title. If it does not exist, create one with `status: owned` or `status: wishlist`.
2. Apply the change (owned, empty, depleted, discarded, wishlist).
3. Update `quantity` if provided.
4. If a newly owned supply enables a planned unit's painting plan, mention that.
5. Confirm the update.
