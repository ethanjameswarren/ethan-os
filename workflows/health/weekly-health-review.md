# Workflow: weekly-health-review

## Purpose

Periodically surface what needs attention across active Habits and Medical Notes.

## Steps

1. Load all Habit, Log Entry, and Medical Note objects from `ethan-life/domains/health/`.
2. Run `skills/health/suggest-habit-insights.md` to identify broken streaks, habits with no recent logs, and medical follow-ups coming due.
3. Return the prioritized findings to the user.

## Output

- prioritized list of findings with reasons
- no objects are modified by this workflow

## Confirmation policy

- Read-only workflow: no confirmation required to run.
- Any change the user decides to make based on the findings goes through `skills/health/log-metric.md`, `skills/health/capture-medical-note.md`, or `workflows/core/revise.md`.
