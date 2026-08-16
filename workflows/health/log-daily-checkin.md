# Workflow: log-daily-checkin

## Purpose

Capture one or more health metrics for the day in a single pass and update the relevant habit streaks.

## Steps

1. Parse the input for one or more mentioned metrics (e.g. sleep, exercise, mood, water).
2. For each metric, run `skills/health/log-metric.md`.
3. Return a short summary of what was logged and any streak changes.

## Output

- Log Entry object IDs created
- updated `current_streak` for any linked Habits
- brief summary

## Confirmation policy

- Auto-execute: logging clearly stated metrics.
- Ask for confirmation: whenever `skills/health/log-metric.md` would (ambiguous metric type).
