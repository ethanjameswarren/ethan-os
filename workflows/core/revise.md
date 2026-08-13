# Workflow: revise

## Purpose

Update an existing object while preserving meaningful evolution.

## Steps

1. Resolve object by ID or title.
2. Load current object.
3. Determine what changed and why.
4. If the change materially alters interpretation, position, or confidence, ask for confirmation.
5. Update the object and append an `## Evolution` note.
6. Validate and write.

## Output

- updated object ID
- summary of changes

## Confirmation policy

- Minor corrections (typos, links): auto-execute.
- Material interpretation or belief change: ask for confirmation.
