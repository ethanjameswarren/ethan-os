# Health & Habits

## What it does

Track recurring habits, log metrics against them, and keep lightweight medical notes so you can spot trends and stay on top of follow-ups.

## Why it exists

Health data is most useful when it is low-friction and consistent. Ethan OS keeps habits and logs structured enough to review but simple enough to capture in a conversation.

## What you do

- Describe a habit you want to track, a metric you logged, or a medical note you want to keep.
- Ask for streaks, trends, or a weekly health review.
- Flag a missed follow-up or a change in status.

## What Ethan OS does

- Stores habit definitions with frequency and target.
- Logs immutable entries for each habit, deriving the current streak from the log history.
- Stores medical notes with date, topic, and confidentiality level.
- Surfaces broken streaks, overdue follow-ups, and trends during review.
- Stores training-location equipment inventories and builds workouts using exercises available at the selected location.
- Reports substitutions and unavailable equipment rather than assuming access.
- Never silently changes a habit status or deletes log history.

## Key ideas

- **Streaks are derived.** The log is the source of truth; `current_streak` is computed.
- **Logs are immutable.** Corrections go through a revision workflow.
- **Medical notes are privileged.** They avoid identifiers like insurance IDs or full record numbers.
- **Trends come from data.** The system reports what the log shows, not motivational guesses.

## Example interaction

> **You:** "I ran 5k this morning."  
> **OS:** "I'll log that against your running habit. Your current streak is now 3 weeks. Anything else?"  
> **You:** "Also had a dentist appointment."  
> **OS:** "Got it. I'll add a medical note with a follow-up in six months."

## What gets saved

- **Habit** — activity, frequency, target, and status.
- **Log Entry** — timestamp, habit, value, and optional notes.
- **Medical Note** — date, topic, summary, follow-up date, and privacy flag.
- **Training Location** — normalized equipment inventory for a real place.
- **Workout** — exercise plan constrained by a selected training location.

## Important behaviors

- Do not fabricate a log entry.
- Do not overwrite an existing log; use revision.
- Do not store insurance IDs, medical record numbers, or other identifiers.
- Distinguish a habit log from a medical note.

## Related workflows

- [Weekly health review](../workflows/health.md)

## Technical implementation

- Workflows: `workflows/health/`
- Skills: `skills/health/`
- Schemas: `schemas/domains/health/habit.schema.yaml`, `log-entry.schema.yaml`, `medical-note.schema.yaml`
