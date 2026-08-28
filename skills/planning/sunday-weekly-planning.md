# Skill: sunday-weekly-planning

## Purpose

Build the upcoming week's concrete plan from the existing baseline, real calendar, local overrides, current priorities, and recurring responsibilities. The Sunday review starts from the user's normal week and changes only what needs to change.

## Triggers

- "Let's do my Sunday review."
- "Plan next week."
- "What does next week look like?"
- "Build next week's schedule."

## Input

- Active `planning.baseline-schedule` from `ethan-life/domains/planning/baseline-schedule.md`.
- Active `planning.schedule-override` objects covering the upcoming week.
- `ethan-life/domains/planning/calendar-integration.yaml` if enabled.
- Active `planning.goal`, `planning.project`, and `planning.task` objects.
- Reading state from the knowledge domain if Guided Reading is active.
- Any user-stated preferences, special events, or desired changes.

## Output

- Draft `planning.weekly-plan` for the upcoming week.
- Candidate changes (overrides or baseline updates if the user wants them).
- Concise human-readable summary of the week: priorities, notable days, changes from normal, admin/chores, and intentionally open time.

## Sequence

### 1. Look back briefly

- Inspect the most recently accepted `planning.weekly-plan` and any completed/dropped tasks from the prior week.
- If stored state is enough, summarize the likely issues:
  - blocks repeatedly skipped,
  - goals/tasks with no progress,
  - unusual overloads.
- Ask at most one or two targeted questions if a pattern is unclear.

### 2. Load next week's fixed reality

- Load the `planning.baseline-schedule` as the starting shape.
- Load active overrides (`one_off` and `temporary`) that cover the upcoming week.
- If Google Calendar is enabled, fetch relevant events and normalize them.
- Mark fixed blocks: baseline fixed, calendar busy events, and one-off fixed commitments.
- Identify unusually busy or disrupted days.
- Do not ask the user to repeat information already available.

### 3. Identify next week's priorities

- Run `skills/planning/suggest-next-actions.md` to surface active goals, projects, and unblocked tasks.
- Inspect active `knowledge.learning-program` objects and their current module/assessment status.
- Inspect active reading state and retention reviews if relevant.
- Ask: "What are the 1–3 things you most want to make progress on next week?" only if priorities cannot be confidently inferred.
- Limit weekly focus. Do not try to advance every active project.

### 4. Maintenance / admin

- Check recurring responsibilities based on canonical state and the prior week:
  - chores
  - errands
  - groceries
  - laundry
  - household tasks
  - financial/admin work
- Only place an item if it is actually due or needed next week.
- Do not add a recurring item simply because the concept exists.

### 5. Place flexible priorities

- Fit high-value flexible work into the existing baseline containers first.
- Use themed/flexible evening blocks before adding new time.
  - If Wednesday carries a Learning block and Guided Reading is a priority, use that block.
  - If Thursday is the Build block, place project work there.
- If a project has a concrete next action, schedule the concrete action, not a vague "work on project" block.
- Respect schedule preferences (`preferred_workout_time`, `cognitive_work_window`, `downtime_days`, etc.).

### 6. Protect free time

- Do not optimize every empty hour.
- Preserve downtime, flexible evenings, and weekend free time as configured.
- Default toward leaving `downtime_days` largely open.
- Recovery and sleep blocks are fixed and not squeezed.

### 7. Realism / capacity check

Before presenting the plan, verify:

- total fixed time vs. discretionary time each day,
- sleep feasibility (`minimum_sleep_hours`, `latest_bed`, `earliest_wake`),
- commute/travel transitions are realistic,
- cognitively demanding evenings are not stacked,
- number of major priorities is realistic,
- chores/maintenance load is not concentrated on one day,
- weekend crowding is reasonable,
- consecutive overloaded days are flagged.

If overloaded:
- reduce or defer lower-priority flexible items,
- propose a feasible version rather than just reporting overload.

### 8. Build the weekly-plan object

Run `skills/planning/generate-weekly-plan.md` with the prepared inputs:
- baseline blocks for the week,
- external calendar events as fixed blocks with `source: calendar`,
- overrides,
- prioritized flexible items placed in existing containers.

Store the draft as `planning.weekly-plan` with status `draft` in `ethan-life/domains/planning/weekly-plans/`.

### 9. Present the plan

Use a compact human-readable format:

```
# Next Week

## Main priorities
1. ...
2. ...

## Monday
- Normal workday
- 7:00–8:00 PM — Career task

## Tuesday
...

## Admin / chores
- ...

## Changes from normal
- Thursday dinner at 7
- Sunday game
- Wednesday Learning block used for Guided Reading

## Intentionally left open
- Friday evening
- Saturday afternoon/evening
```

Emphasize what is different from normal. Do not dump every routine unless the user asks for a full timetable.

### 10. Confirm and persist

- Allow the user to accept, adjust, regenerate a day, move a block, or remove something.
- Apply any requested changes with `skills/planning/apply-schedule-change.md` (correct scope).
- On acceptance, update the weekly plan status to `accepted`.
- Save the final plan.

## Rules

- Start from the baseline. Plan exceptions and priorities, not a blank week.
- Ask as few questions as possible; use stored state first.
- Use existing flexible/themed blocks before inventing new ones.
- Protect free time and recovery.
- Use concrete next actions, not vague project labels.
- Do not advance every active project in one week.
- Special events reshape only the affected area.
- Persist only after the user confirms.
