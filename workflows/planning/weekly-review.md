# Workflow: weekly-review

## Purpose

Periodically surface what needs attention across active Goals, Projects, and Tasks.

## Steps

1. Load all Goal, Project, and Task objects from `ethan-life/domains/planning/`.
2. Run `skills/planning/suggest-next-actions.md` to identify unblocked tasks, blocked items, stale projects, and goals without momentum.
3. Optionally create a summary artifact of the findings (plain text; no new schema required for v0.1).
4. Return the prioritized findings to the user.

## Output

- prioritized list of findings with reasons
- no objects are modified by this workflow

## Confirmation policy

- Read-only workflow: no confirmation required to run.
- Any status change the user decides to make based on the findings goes through `workflows/core/revise.md`.
