# Skill: breakdown-project

## Purpose

Break a Goal into a Project with milestones and initial next actions.

## Input

- a Goal object (`planning.goal`), by ID or content
- optional user-provided constraints (deadline, resources, dependencies)

## Steps

1. Confirm the Goal actually requires multiple coordinated steps over time. If it can be accomplished with one or two direct actions, recommend Tasks under the Goal instead of a Project.
2. Identify a logical sequence of milestones that lead to the goal's success criteria.
3. For each milestone, define a clear, checkable definition of done.
4. Identify concrete next actions that would move the first milestone forward.
5. Do not invent deadlines, scope, or resources the user has not stated.

## Output

Create or update a Project object in `ethan-life/domains/planning/projects/`.

Use schema `planning.project` and version `1`. See `instructions/domains/planning/object-prompts/project.md` for the full field list.

Link the Project to its Goal via `goal_id` and a `part_of` relationship.

## Confirmation policy

- Auto-execute: drafting milestones and next actions from a clear Goal.
- Ask for confirmation: when the milestone sequence depends on an assumption about scope or timing the user has not confirmed, or before marking a Project `completed` or `abandoned`.

## Relationship types

- `part_of` — project → goal
- `derived_from` — project derived from the goal breakdown
- `related_to` — related projects
