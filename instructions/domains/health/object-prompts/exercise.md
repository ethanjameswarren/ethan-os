# Health Exercise Object Prompt

## Purpose

Define an exercise in the canonical exercise library.

## Required fields

- `id`: stable unique exercise ID
- `schema`: `health.exercise`
- `schema_version`: `1`
- `title`
- `created_at`
- `provenance`
- `movement_pattern`
- `primary_muscles`

## Optional fields

- `secondary_muscles`
- `training_objectives`
- `required_equipment`: list of canonical equipment type IDs
- `optional_equipment`
- `substitutes`: ordered list of preferred alternative `exercise_id`s
- `unilateral`
- `stability`: fixed | supported | free
- `loading_potential`: low | moderate | high
- `isolation`
- `hypertrophy_suitability`: low | medium | high
- `strength_suitability`: low | medium | high
- `cardio`
- `notes`
- `links`

## Instructions

- Use canonical equipment type IDs from `ethan-os/config/health/equipment-taxonomy.yaml`.
- Keep `required_equipment` minimal. If an exercise needs a rack *and* a bar, list both.
- Order `substitutes` from closest to least-close match.
- Mark `stability` and `loading_potential` honestly; they drive substitution ranking.
