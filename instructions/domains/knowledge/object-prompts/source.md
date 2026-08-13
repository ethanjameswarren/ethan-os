# Source Object Prompt

## Purpose

Generate or update a Source object.

## Required fields

- `id`: stable ID
- `schema`: `knowledge.source`
- `schema_version`: `1`
- `title`
- `source_type`: book | article | paper | podcast | video | course | conversation | experience | observation
- `created_at`
- `provenance`

## Optional fields

- `author`
- `url`
- `published_date`
- `summary` (one or two sentences)
- `status`: unread | reading | finished | reference
- `rating`

## Instructions

- Infer missing optional fields from context or leave blank.
- Do not fabricate metadata.
- If the source already exists, update only changed fields and record an `## Evolution` note if significant.
