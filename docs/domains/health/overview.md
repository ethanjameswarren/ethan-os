# Health Domain

The fifth fully implemented domain in Ethan OS.

## Purpose

Track recurring health habits, log metrics against them, and record medical notes.

## v0.1 objects

- Habit (`health.habit`)
- Log Entry (`health.log-entry`)
- Medical Note (`health.medical-note`)

## Object flow

```
Habit → Log Entry (linked to habit, recomputes current_streak)
Medical Note (standalone; may relate to a Habit)
```

## Design principles

- `current_streak` is always derived from Log Entries, never hand-set.
- Log Entries are immutable historical records; corrections go through `workflows/core/revise.md`.
- Medical Notes carry a higher confidentiality bar: no full medical record numbers or insurance IDs, even in a private repository.
- Review surfaces findings (broken streaks, overdue follow-ups); it never silently changes status.
