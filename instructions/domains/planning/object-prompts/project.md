# Planning Project Object Prompt

## Purpose

Generate or update a Project object.

## Required fields

- `id`: stable ID
- `schema`: `planning.project`
- `schema_version`: `1`
- `title`
- `status`: planned | active | blocked | completed | abandoned
- `created_at`
- `provenance`

## Optional fields

- `goal_id`: ID of the parent `planning.goal`
- `description`
- `milestones`: list of `{ title, target_date, status }`
- `next_actions`: list of strings
- `links`: typed relationships
- `## Evolution` section

## Instructions

- Only create a Project when a Goal requires multiple coordinated steps over time; otherwise create Tasks directly under the Goal.
- Link the Project to its Goal via both `goal_id` and a `part_of` relationship.
- Keep `next_actions` short and concrete; convert them into Task objects when the user is ready to act.
