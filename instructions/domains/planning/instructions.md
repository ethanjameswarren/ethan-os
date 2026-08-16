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

## Lifecycle

- Goal: `active` → `achieved` | `abandoned` | `on_hold`.
- Project: `planned` → `active` → `completed` | `blocked` | `abandoned`.
- Task: `todo` → `in_progress` → `done` | `blocked` | `dropped`.
- Objects may move backward (e.g. `active` → `on_hold`) when priorities change.
