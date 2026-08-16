# Workflow: plan-project

## Goal

Turn a stated aspiration into a Goal, and — when warranted — a Project with milestones and initial Tasks.

## Required inputs

- natural language description of what Ethan wants to achieve
- access to `ethan-life/domains/planning/goals/`, `ethan-life/domains/planning/projects/`, `ethan-life/domains/planning/tasks/`

## Produced artifacts

- Goal object (`planning.goal`) in `ethan-life/domains/planning/goals/`
- Project object (`planning.project`) in `ethan-life/domains/planning/projects/`, if warranted
- initial Task objects (`planning.task`) in `ethan-life/domains/planning/tasks/`, if the user is ready to commit to next actions

## Steps

### 1. Capture or resolve the Goal

Run `skills/planning/capture-goal.md`.

If the input matches an existing Goal, update it rather than creating a duplicate.

### 2. Decide whether a Project is warranted

A Project is warranted only if achieving the Goal requires multiple coordinated steps over time. If the Goal can be accomplished with one or two direct actions, skip to step 4 and create Tasks linked directly to the Goal.

### 3. Break down the Project

Run `skills/planning/breakdown-project.md` using the Goal from step 1.

Link the Project to the Goal via `goal_id` and a `part_of` relationship.

### 4. Create initial Tasks

For next actions the user is ready to commit to now, run `skills/planning/capture-task.md` for each, linking to the Project (`project_id`) or, if there is no Project, the Goal (`goal_id`).

Do not manufacture tasks the user has not actually agreed to do next.

### 5. Validate

- Every Project links back to a Goal.
- Every Task links to a Project or Goal, or is intentionally standalone.
- No milestone or task duplicates an existing one.

## User-facing output

Return:

1. the Goal (created or updated)
2. the Project and its milestones, if created
3. initial Tasks created
4. anything left unresolved that requires the user's input

## Confirmation policy

- Auto-execute: creating the Goal, Project, and Tasks from clear input.
- Ask for confirmation: when it is unclear whether a Project is warranted, when milestone sequencing depends on an unconfirmed assumption, or when a new Goal may overlap significantly with an existing one.
