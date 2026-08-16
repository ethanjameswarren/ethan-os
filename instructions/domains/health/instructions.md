# Health Domain Instructions

## Scope

Track recurring health habits, log metrics against them, and record medical notes.

## Object flow

```
Habit → Log Entry (linked to habit, recomputes current_streak)
Medical Note (standalone; may link to a Habit, e.g. medication adherence)
```

## Habit handling

- Use `skills/health/capture-habit.md` to define a recurring behavior to track (exercise, sleep, meditation, water, medication adherence, etc.).
- Store Habits in `ethan-life/domains/health/habits/`.
- `current_streak` is recomputed from linked Log Entries during logging/review; never hand-set it.
- A Habit may link to a `planning.goal` via `goal_id` when it supports a broader goal (e.g. "Run a half marathon").

## Log entry handling

- Use `skills/health/log-metric.md` to record a single measurement or event: a workout, sleep hours, weight, mood, water intake, or medication taken.
- Store Log Entries in `ethan-life/domains/health/logs/`.
- Link a Log Entry to its Habit via `habit_id` when one exists for that `metric_type`; otherwise it stands alone.
- Log Entries are immutable historical records; corrections go through `workflows/core/revise.md`.

## Medical note handling

- Use `skills/health/capture-medical-note.md` to record appointments, diagnoses, medications, and lab results.
- Store Medical Notes in `ethan-life/domains/health/medical-notes/`.
- Medical Notes carry a higher confidentiality bar than other Health objects; see below.
- Track `follow_up` explicitly so upcoming appointments or actions are not lost.

## Review

- Use `skills/health/suggest-habit-insights.md` to identify broken streaks, habits with no recent logs, and medical follow-ups coming due.
- `workflows/health/weekly-health-review.md` runs this periodically and surfaces findings; it does not silently alter habit status or streaks outside of normal recomputation.

## Confidentiality

- `ethan-life` is private, but Medical Notes should still avoid storing full medical record numbers, insurance member IDs, or other identifiers not needed for personal reference. Summarize provider guidance in Ethan's own words where practical.

## Relationships

- Use inline typed links (see `docs/architecture/relationships.md`).
- Common relations: `part_of` (log entry → habit, habit → goal), `related_to` (medical note → habit), `revised_by`.

## Lifecycle

- Habit: `active` → `paused` → `dropped`, or back to `active`.
- Medical Note: `active` → `monitoring` → `resolved`.
