# Health Training Location Object Prompt

## Purpose

Define a gym or training location with its equipment inventory.

## Required fields

- `id`: stable ID
- `schema`: `health.training-location`
- `schema_version`: `1`
- `title`
- `created_at`
- `provenance`
- `name`
- `location_type`: apartment_gym | commercial_gym | home | work_gym | hotel_gym | travel | outdoor
- `status`: active | inactive | planned

## Optional fields

- `availability`
- `hours`
- `equipment`: array of equipment records conforming to `health.equipment` shape
- `audit_date`
- `audit_source`
- `confidence`: high | medium | low | unknown
- `notes`
- `links`

## Instructions

- Create one file per location in `ethan-life/domains/health/training-locations/`.
- Use `audit_date` and `audit_source` to track provenance.
- List `equipment` with canonical `canonical_type` from the taxonomy.
- Do not invent details. Mark exact quantities or max weights as `unknown` when not verified.
