# Skill: log-metric

## Purpose

Record a single health measurement or event, and update the related Habit's streak if applicable.

## Input

Natural language describing something Ethan did or measured: a workout, sleep hours, weight, mood, water intake, medication taken.

## Steps

1. Extract `metric_type`, `date` (default today if phrasing implies "just now"), and `value`.
2. If an active Habit exists for this `metric_type`, link the new Log Entry via `habit_id`.
3. Recompute the Habit's `current_streak` from all of its Log Entries in chronological order.

## Rules

- Do not infer a `value` the user has not stated.
- Do not hand-set `current_streak` directly; always recompute it from Log Entries.
- Treat each Log Entry as an immutable record of what happened.

## Output

Create a Log Entry object in `ethan-life/domains/health/logs/`.

Use schema `health.log-entry` and version `1`. See `instructions/domains/health/object-prompts/log-entry.md`.

Update the linked Habit's `current_streak` if applicable.

## Confirmation policy

- Auto-execute: creating a log entry from a clear statement.
- Ask for confirmation: when the metric type is ambiguous between two existing habits.

## Relationship types

- `part_of` — log entry → habit
