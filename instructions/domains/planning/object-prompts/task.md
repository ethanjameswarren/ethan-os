# Planning Task Object Prompt

## Purpose

Generate or update a Task object.

## Required fields

- `id`: stable ID
- `schema`: `planning.task`
- `schema_version`: `1`
- `title`
- `status`: todo | in_progress | blocked | done | dropped
- `created_at`
- `provenance`

## Optional fields

- `project_id`: ID of the parent `planning.project`
- `goal_id`: ID of the parent `planning.goal`, if there is no project
- `priority`: low | medium | high
- `due_date`
- `context`: situational context needed to act (energy, location, tool)
- `notes`
- `links`: typed relationships
- `## Evolution` section

## Instructions

- Link every task to a project or goal when one is known; a task with neither is a valid standalone to-do but should be flagged during review.
- Do not infer a `due_date` or `priority` the user has not stated.
- Prefer updating an existing task's status over creating a duplicate task for the same action.
