# Schedule Planning

## What it does

Maintain a reusable baseline schedule, adapt it when life changes, and generate concrete weekly plans that respect fixed commitments, flexible priorities, and recovery time.

## Why it exists

Most scheduling tools treat every change as either a permanent routine or a one-off event. Ethan OS separates the two so a dinner invitation does not rewrite your weekly routine and a permanent commute change does not require manually editing every future week.

## What you do

- Describe a change in plain language.
- Ask for a weekly plan, a day preview, or a schedule diagnosis.
- Confirm permanent baseline changes.
- Optionally ask for a full rebuild if the current schedule is not working.

## What Ethan OS does

- Keeps a baseline schedule for your normal week.
- Applies one-off and temporary overrides without changing the baseline.
- Generates a weekly plan by combining baseline + overrides + active goals and tasks.
- Resolves conflicts by protecting fixed commitments, moving flexible items, and dropping optional ones.
- Reasons about dependencies (e.g., earlier departure → earlier wake → earlier bedtime).
- Diagnoses schedule problems and recommends targeted fixes instead of adding more blocks.

## Key ideas

### Baseline, weekly plan, and override are separate

- **Baseline** — the recurring normal structure.
- **Weekly plan** — one concrete week derived from the baseline.
- **Override** — a one-off, temporary, or permanent change.

A one-off dinner on Thursday only changes that Thursday's plan. A permanent "Wednesday is reading night" change updates the baseline.

### Smallest change first

The system makes the minimal adjustment needed to fit a new commitment. It only regenerates the week when the plan becomes infeasible or the user explicitly asks.

### Fixed, flexible, optional

- **Fixed** — work, appointments, sleep, travel, hard commitments. These do not move without confirmation.
- **Flexible** — workouts, learning, project work, chores. These can shift within constraints.
- **Optional** — extra reading, bonus workouts, optional calls. These drop first when time is overloaded.

### Dependencies matter

A change in one block can cascade. The system warns you about dependencies before applying a change.

## Example interaction

> **You:** "I have dinner Thursday at 7 this week."  
> **OS:** "Got it. That's a one-off override for this Thursday. I'll adjust Thursday's plan and keep your baseline unchanged."  
>
> *(later)*  
>
> **You:** "From now on Wednesday night is reading night."  
> **OS:** "This sounds like a permanent baseline change. Should I add a reading block to every Wednesday baseline and regenerate the current week?"  
> **You:** "Yes."  
> **OS:** "Done. I'll keep the block flexible so it can move if another commitment conflicts."

## What gets saved

Canonical state lives in `ethan-life/domains/planning/`:

- **Baseline schedule** — `baseline-schedule.md`: recurring weekly blocks, constraints, and preferences.
- **Schedule override** — `schedule-overrides/<override>.md`: the change, its scope, dates, and reason.
- **Weekly plan** — `weekly-plans/<plan>.md`: concrete blocks for a specific week, with sources and categories.
- **Schedule diagnosis notes** — optional notes on tradeoffs and recommendations, kept inside the relevant plan or override.

## Important behaviors

- Never silently convert a one-off into a permanent routine.
- Never silently convert a temporary override into a permanent baseline change.
- Never delete fixed commitments to make room.
- Never add optional blocks if they crowd fixed or flexible recovery time.
- Surface dependency implications before applying changes.
- Diagnose schedule problems with targeted fixes, not blanket overhauls.

## Related workflows

- [Schedule your week](../workflows/schedule-planning.md)
- [Plan your week](planning.md) — for goal and task prioritization

## Technical implementation

- Workflows: `workflows/planning/schedule-weekly-plan.md`
- Skills: `skills/planning/apply-schedule-change.md`, `skills/planning/generate-weekly-plan.md`, `skills/planning/diagnose-schedule.md`
- Schemas: `schemas/domains/planning/baseline-schedule.schema.yaml`, `weekly-plan.schema.yaml`, `schedule-override.schema.yaml`
