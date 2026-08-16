# Planning Goal Object Prompt

## Purpose

Generate or update a Goal object.

## Required fields

- `id`: stable ID
- `schema`: `planning.goal`
- `schema_version`: `1`
- `title`
- `status`: active | achieved | abandoned | on_hold
- `created_at`
- `provenance`

## Optional fields

- `horizon`: short_term | medium_term | long_term
- `why_it_matters`
- `success_criteria`: list of concrete, checkable statements
- `target_date`
- `links`: typed relationships
- `## Evolution` section

## Instructions

- Ask for success criteria if the user has not stated any; a goal without them cannot be reviewed meaningfully later.
- Do not assign a horizon the user has not stated or clearly implied.
- Prefer updating an existing goal over creating a near-duplicate for the same underlying objective.
