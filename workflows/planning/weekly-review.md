# Workflow: weekly-review

## Purpose

Periodically surface what needs attention across active Goals, Projects, and Tasks, and on Sunday build the upcoming week's concrete plan.

## Steps

1. Load all Goal, Project, and Task objects from `ethan-life/domains/planning/`.
2. Run `skills/planning/suggest-next-actions.md` to identify unblocked tasks, blocked items, stale projects, and goals without momentum.
3. If the intent is "sunday-review" or the user asks to plan next week, run `skills/planning/sunday-weekly-planning.md` to build a draft `planning.weekly-plan`.
4. Otherwise, optionally create a summary artifact of the findings (plain text; no new schema required for v0.1).
5. Return the prioritized findings or the candidate weekly plan to the user.

## Output

- prioritized list of findings with reasons, or
- a draft `planning.weekly-plan` for the upcoming week

## Confirmation policy

- Read-only review: no confirmation required to run.
- Sunday weekly plan: present the draft; only save as `accepted` after the user confirms.
- Any status change the user decides to make based on the findings goes through `workflows/core/revise.md`.
