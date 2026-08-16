# Health Log Entry Object Prompt

## Purpose

Generate a Log Entry object.

## Required fields

- `id`: stable ID
- `schema`: `health.log-entry`
- `schema_version`: `1`
- `title`
- `date`
- `metric_type`
- `created_at`
- `provenance`

## Optional fields

- `habit_id`: ID of the `health.habit` this entry counts toward, if any
- `value`: freeform value appropriate to `metric_type`, e.g. "7.5 hours", "32 min run"
- `notes`
- `links`: typed relationships
- `## Evolution` section

## Instructions

- Link to an existing Habit via `habit_id` when one exists for this `metric_type`; otherwise leave it standalone rather than forcing a link.
- Treat log entries as immutable historical records; corrections go through `workflows/core/revise.md`.
- Do not infer a `value` the user has not stated.
