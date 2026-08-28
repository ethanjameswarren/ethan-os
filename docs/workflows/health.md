# Workflow: Weekly Health & Habit Review

## What you do

Tell Ethan OS about a habit log, metric, or medical note, or ask for a weekly health review.

Example:

> **You:** "I went to the gym twice this week. Also had a follow-up with the doctor scheduled for next month."

## What Ethan OS does

1. Loads habits and their log entries.
2. Computes streaks and trends from log history.
3. Loads medical notes and checks follow-up dates.
4. Surfaces broken streaks, overdue or upcoming follow-ups, and notable patterns.
5. Presents a concise review with actionable next steps.

## Conceptual stages

- **Collect** — habits, log entries, medical notes.
- **Derive** — streaks, completion rates, follow-up status.
- **Surface** — flags for attention.
- **Summarize** — present a readable weekly review.

## Outputs

- A weekly health review with streak status and follow-up reminders.
- Flags for broken streaks or overdue medical follow-ups.
- Suggested actions, not applied automatically.

## Safeguards

- Streaks are derived from logs, not hand-set.
- Existing log entries are not overwritten; corrections use a revision workflow.
- Medical notes avoid insurance IDs, medical record numbers, and other identifiers.
- Trends are reported from data, not motivational guesses.

## Technical details

- Workflows: `workflows/health/weekly-review.md`
- Skills: `skills/health/check-streaks.md`, `skills/health/flag-follow-ups.md`
- Schemas: `schemas/domains/health/habit.schema.yaml`, `log-entry.schema.yaml`, `medical-note.schema.yaml`
