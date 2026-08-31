# Skill: generate-weekly-plan

## Purpose

Produce a concrete weekly plan from a baseline schedule, active overrides, goals, and tasks.

## Input

- Active `planning.baseline-schedule`.
- `planning.schedule-override` objects whose scope covers the target week.
- Active `planning.goal` and `planning.task` objects for the same horizon.
- Optional user priorities (e.g., "make room for project X").

## Steps

1. Start from the baseline recurring blocks, mapped to each day of the target week.
2. Apply `one_off` overrides to their specific dates only.
3. Apply `temporary` overrides to each day of the target week that falls within their date range.
4. If a permanent override has been confirmed, update the baseline blocks before generating the plan.
5. Load normalized Google Calendar events for the date range if the integration is enabled; include `fixed` busy events, note `informational` events, and ignore cancelled/declined events.
6. Place fixed blocks first: sleep, work, appointments, travel, hard commitments, and fixed calendar events.
6. Place flexible blocks second: exercise, learning, project work, chores. When choosing among candidate actions, use the ordered recommendations from `skills/planning/suggest-next-actions.md` rather than urgency alone.
7. Place optional blocks last: extra reading, optional calls, bonus workouts.
8. Resolve conflicts by:
   - preserving fixed blocks;
   - moving flexible blocks to the next available slot respecting preferences;
   - dropping optional blocks if necessary;
   - surfacing any unresolvable conflict.
9. Account for dependencies: a changed departure cascades to morning routine, wake time, and bedtime.
10. Generate a draft `planning.weekly-plan` with block source, category, and status.

## Output

- Draft `planning.weekly-plan` object.
- List of applied overrides.
- List of conflicts and how they were resolved.
- Notes on dependencies or tradeoffs.

## Rules

- Never silently convert a temporary or one-off override into a permanent baseline change.
- Never delete a fixed block without explicit user confirmation.
- Apply the minimal change needed to fit new commitments.
- Respect `minimum_sleep_hours` and `latest_bed` / `earliest_wake` constraints.
- `protected_evenings` are treated as fixed unless the user explicitly overrides them.
