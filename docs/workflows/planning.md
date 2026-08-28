# Workflow: Plan Your Week

## What you do

Tell Ethan OS what is happening this week and what you want to get done.

Example:

> **You:** "I need to finish the home office project, run three times, and I have a dentist appointment on Thursday at 3."

## What Ethan OS does

1. Loads your active goals, projects, and tasks.
2. Loads your baseline schedule and any temporary overrides.
3. Places fixed commitments first.
4. Derives the smallest set of flexible and optional blocks needed to move goals forward.
5. Surfaces conflicts, overload, or tradeoffs if not everything fits.
6. Produces a concrete weekly plan.

## Conceptual stages

- **Collect** — fixed commitments, goals, habits, tasks.
- **Fit** — place hard constraints, then flexible items, then optional ones.
- **Resolve** — surface conflicts and ask which items move, drop, or wait.
- **Publish** — produce the accepted weekly plan.

## Outputs

- A Weekly Plan object with fixed, flexible, and optional blocks.
- A list of conflicts or tradeoffs that require your decision.
- Updated task/habit status only after you confirm.

## Safeguards

- Fixed commitments are never silently deleted to make room.
- A one-off event does not rewrite your baseline schedule.
- The OS asks before making a permanent baseline change.
- Sleep and recovery blocks are treated as hard constraints by default.

## Technical details

- Workflows: `workflows/planning/schedule-weekly-plan.md`, `workflows/planning/weekly-review.md`
- Skills: `skills/planning/apply-schedule-change.md`, `skills/planning/diagnose-schedule.md`, `skills/planning/suggest-next-actions.md`
- Schemas: `schemas/domains/planning/baseline-schedule.schema.yaml`, `weekly-plan.schema.yaml`, `schedule-override.schema.yaml`
