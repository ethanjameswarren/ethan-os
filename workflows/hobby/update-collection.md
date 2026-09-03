# Workflow: update-collection

## Purpose

Apply a specific status change to a collection item (acquired, assembled, painted, completed, sold, etc.).

## Trigger

- "Mark my Warriors as primed."
- "I ordered the Skorpekh Destroyers."
- "My Overlord is now fully painted."
- "I sold the old Start Collecting box."

## Inputs

- Item title or ID.
- Explicit field changes.

## Outputs

- Updated `hobby.collection-item` file.
- Confirmation of the new state and any blocked next steps.

## Steps

1. Run `ethan-os/skills/hobby/update-collection.md`.
2. If `assembly_status` or `magnetization_status` was set in a way that contradicts the pre-build check, surface a warning.
3. Confirm the update.
