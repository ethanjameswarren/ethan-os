# Health Medical Note Object Prompt

## Purpose

Generate or update a Medical Note object.

## Required fields

- `id`: stable ID
- `schema`: `health.medical-note`
- `schema_version`: `1`
- `title`
- `note_type`: appointment | diagnosis | medication | lab_result | other
- `date`
- `created_at`
- `provenance`

## Optional fields

- `provider`
- `summary`
- `follow_up`: any stated follow-up action or next appointment
- `status`: active | resolved | monitoring
- `links`: typed relationships
- `## Evolution` section

## Instructions

- Do not store full medical record numbers, insurance member IDs, or other identifiers not needed for personal reference.
- Always capture `follow_up` explicitly when the user mentions a next step or appointment, so it is not lost.
- Prefer updating an existing note's `status` (e.g. `active` → `resolved`) over creating a duplicate for the same issue.
