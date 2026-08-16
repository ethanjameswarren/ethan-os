# Health Habit Object Prompt

## Purpose

Generate or update a Habit object.

## Required fields

- `id`: stable ID
- `schema`: `health.habit`
- `schema_version`: `1`
- `title`
- `status`: active | paused | dropped
- `created_at`
- `provenance`

## Optional fields

- `metric_type`: what this habit tracks, e.g. exercise, sleep, meditation, water, medication_adherence
- `target_frequency`: plain description, e.g. "5x per week"
- `current_streak`: recomputed from linked log entries, not hand-maintained
- `goal_id`: related `planning.goal`, if any
- `links`: typed relationships
- `## Evolution` section

## Instructions

- Never hand-set `current_streak`; it is recomputed by `skills/health/log-metric.md` or the weekly review workflow.
- Do not create a duplicate habit for the same `metric_type` the user is already tracking; update the existing one.
