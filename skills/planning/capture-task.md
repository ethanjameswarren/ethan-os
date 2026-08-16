# Skill: capture-task

## Purpose

Convert an ad-hoc action item into a Task object, linked to a Project or Goal when one is known.

## Input

Natural language describing something Ethan needs or wants to do.

## Extract

- the concrete action, stated as a verb phrase
- project or goal it relates to, if mentioned or inferable from recent context
- priority, if stated
- due date, if stated
- situational context needed to act (e.g. requires a specific tool, location, or energy level)

## Rules

- Do not infer `priority` or `due_date` the user has not stated.
- If a task clearly relates to an existing Project or Goal, link it via `project_id` or `goal_id`. Otherwise, create it as a standalone task; do not force a link.
- Prefer updating an existing task's status (e.g. `todo` → `done`) over creating a duplicate when the user reports completing something already captured.

## Output

Create or update a Task object in `ethan-life/domains/planning/tasks/`.

Use schema `planning.task` and version `1`. See `instructions/domains/planning/object-prompts/task.md` for the full field list.

## Confirmation policy

- Auto-execute: creating a draft task from a clear action statement.
- Ask for confirmation: when the linked project/goal is ambiguous between multiple candidates, or when marking a task `done` would also imply a milestone or goal is complete.

## Relationship types

- `part_of` — task → project or task → goal
- `related_to` — related tasks
