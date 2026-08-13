# Idea Object Prompt

## Purpose

Generate or update an Idea object.

## Required fields

- `id`: stable ID
- `schema`: `knowledge.idea`
- `schema_version`: `1`
- `title`
- `claim` (what the source claims)
- `created_at`
- `provenance`: `capture_id`, `source_id`, `agent_version`, `provenance_note`

## Optional fields

- `interpretation` (Ethan's reading)
- `position`: agree | disagree | neutral | exploring
- `confidence`: low | medium | high
- `status`: captured | understood | connected | testing | practicing | internalized
- `lifecycle_note`
- `links`: typed relationships
- `## Evolution` section

## Instructions

- Keep the claim distinct from interpretation.
- Record Ethan's position explicitly.
- Do not create an Idea for every sentence. Only atomic, reusable concepts.
- Resolve duplicates: if an idea matches an existing one, update or link it rather than create a new object.
