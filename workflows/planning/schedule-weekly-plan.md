# Workflow: schedule-weekly-plan

## Purpose

Build or adapt a concrete weekly plan from the baseline schedule, temporary overrides, one-off commitments, goals, and tasks.

## Triggers

- "Plan my week."
- "What does tomorrow look like?"
- "I have dinner Thursday at 7 this week."
- "From now on Wednesday night is reading."
- "My schedule isn't working — redo it."
- "Where can I fit another workout?"

## Steps

1. Identify the user's intent: create, adjust, rebuild, plan a single day, or diagnose.
2. Determine the relevant week and load the active `planning.baseline-schedule`.
3. Load active `planning.schedule-override` objects:
   - one_off overrides for dates in the week;
   - temporary overrides whose date range covers the week;
   - permanent overrides flagged for baseline update.
4. Load active goals and tasks for the same horizon.
5. Run `skills/planning/generate-weekly-plan.md` to produce a draft `planning.weekly-plan`.
6. Run `skills/planning/apply-schedule-change.md` if the user is changing the baseline or adding an override.
7. Surface conflicts, tradeoffs, and dependency implications.
8. Present the draft for confirmation before saving as `accepted`.
9. Save the accepted weekly plan to `ethan-life/domains/planning/weekly-plans/`.
10. If a permanent override was confirmed, merge it into the baseline schedule and save the updated baseline.

## Output

- A `planning.weekly-plan` object with fixed, flexible, and optional blocks.
- A list of conflicts and resolutions applied.
- Updated baseline schedule if a permanent change was confirmed.
- New or updated `planning.schedule-override` objects for non-permanent changes.

## Confirmation policy

- Read-only previews and diagnoses require no confirmation.
- One-off and temporary overrides are low-risk; confirm once and apply.
- Permanent baseline changes require explicit confirmation.
- Full rebuilds require confirmation when existing accepted weekly plans are superseded.
