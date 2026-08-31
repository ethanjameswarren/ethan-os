# Health Workout Object Prompt

## Purpose

Define a planned or completed workout at a specific training location.

## Required fields

- `id`: stable ID
- `schema`: `health.workout`
- `schema_version`: `1`
- `title`
- `created_at`
- `provenance`
- `training_location_id`
- `status`: planned | completed | skipped | revised

## Optional fields

- `scheduled_date`
- `duration_min`
- `goal`
- `target_muscles`
- `excluded_equipment`: temporary out-of-service or occupied equipment
- `blocks`: array of `{exercise_id, sets, reps, rest, load, note}`
- `notes`
- `links`

## Instructions

- Link to a `health.training-location` by `id`.
- Use `excluded_equipment` for temporary constraints (e.g. occupied machine, out of order).
- `blocks` refer to `exercise_id`s from `ethan-os/config/health/exercise-library.yaml`.
- If an exercise is unavailable, substitute using the exercise's `substitutes` list or movement-pattern fallback.
