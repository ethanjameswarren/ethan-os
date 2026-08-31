# Planning Domain Instructions

## Scope

Capture goals, break them into projects and tasks, track status, and surface what to do next.

## Object flow

```
Goal → Project → Milestones → Tasks
Goal → Task (directly, for goals too small to warrant a project)
```

## Goal handling

- Use `skills/planning/capture-goal.md` to convert a stated aspiration or objective into a Goal object.
- Store Goals in `ethan-life/domains/planning/goals/`.
- Record why the goal matters and concrete success criteria; a goal without success criteria cannot be meaningfully reviewed later.
- Do not infer a horizon (`short_term` / `medium_term` / `long_term`) the user has not stated or clearly implied.

## Project handling

- Use `skills/planning/breakdown-project.md` to break a Goal into a Project with milestones and initial next actions.
- Store Projects in `ethan-life/domains/planning/projects/`.
- Not every goal needs a project. Only create one when the goal requires multiple coordinated steps over time.
- Link every Project to its Goal via `goal_id` and a `part_of` relationship.

## Task handling

- Use `skills/planning/capture-task.md` to convert an ad-hoc action item into a Task object.
- Store Tasks in `ethan-life/domains/planning/tasks/`.
- Link a Task to its Project (`project_id`) or, if there is no project, directly to its Goal (`goal_id`).
- Tasks without any goal/project link are allowed (pure to-dos) but should be flagged during review as candidates for goal alignment.

## Next actions and review

- Use `skills/planning/suggest-next-actions.md` to identify what is actionable now: unblocked tasks, stale projects, goals with no active project or task.
- `workflows/planning/weekly-review.md` runs this periodically and surfaces the result; it does not silently reprioritize or close items without confirmation.

## Relationships

- Use inline typed links (see `docs/architecture/relationships.md`).
- Common relations: `part_of` (task/project → goal), `related_to`, `derived_from` (project ← goal breakdown), `revised_by`.

## Schedule planning

- The baseline schedule (`planning.baseline-schedule`) is the recurring normal-week structure.
- Weekly plans (`planning.weekly-plan`) are derived from the baseline plus temporary overrides and one-off commitments for a specific week.
- Overrides (`planning.schedule-override`) carry an explicit scope:
  - `one_off` — a single occurrence;
  - `temporary` — applies from `start_date` through `end_date`;
  - `permanent` — should be merged into the baseline schedule.
- Never silently convert a `one_off` or `temporary` override into a permanent baseline change.
- Fixed blocks (work, appointments, sleep, travel) are preserved. Flexible blocks (exercise, reading, project work) can move when conflicts arise. Optional blocks drop first when time is overloaded.
- Dependency reasoning is explicit: a changed departure may require an earlier morning routine, which may require an earlier wake time and bedtime.
- Default to the smallest schedule change that solves the problem. Rebuild the week only when asked or when the plan becomes infeasible.

## Strategic objective alignment

When a `long_term` planning goal with a linked career goal and milestone roadmap is active, it functions as the **strategic objective**. See `instructions/policies/configurable/strategic-objective-alignment.md` for the full policy.

Key planning behaviors:

- **Weekly planning**: The current milestone horizon's expectations inform weekly priority selection. Weeks with zero strategic-objective-aligned discretionary blocks trigger a drift warning.
- **Project selection**: New projects are evaluated against the strategic objective's `decision_criteria`. Classification (directly advances / indirectly supports / neutral / competes with) is surfaced to the user but does not block creation.
- **Next actions**: Items linked to the strategic objective or its active milestone horizon are weighted above unlinked items when ranking suggestions.
- **Goal review**: Reviews of the strategic objective include a structured trajectory assessment across the eight milestone dimensions.
- **Drift detection**: Cross-domain reasoning surfaces `strategic_drift` (systematic time allocation away from the objective) and `strategic_gap` (milestone expectations with no supporting execution).

These behaviors surface tradeoffs and gaps. They do not silently reprioritize, close, or defer projects.

## Lifecycle

- Goal: `active` → `achieved` | `abandoned` | `on_hold`.
- Project: `planned` → `active` → `completed` | `blocked` | `abandoned`.
- Task: `todo` → `in_progress` → `done` | `blocked` | `dropped`.
- Objects may move backward (e.g. `active` → `on_hold`) when priorities change.
