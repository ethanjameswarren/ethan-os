# Skill: record-painting-log

## Purpose

Create or update a `hobby.painting-log` record for a completed (or in-progress) model.

## Input

- Collection item ID.
- Painting plan ID.
- Start/end dates, phases completed, recipe, techniques, mistakes, corrections, time, photos, self-assessment, lessons.

## Output

- New or updated `hobby.painting-log` Markdown file.
- Updated collection item status (`painting_status`, `painting_completed_date`, events).

## Instructions

1. If a log exists for the model, update it; otherwise create one.
2. Record only what is useful for future painting. Do not force detailed data entry.
3. Capture: date range, phases completed, recipe (short map of area → paint), techniques practiced, mistakes, corrections that worked, approximate time, photo references/captions, self-assessment, and lessons for the next model.
4. Update the collection item's `painting_status` and append an event (`painting_started`, `phase_completed`, `painting_completed`).
5. If the model is completed, set `painting_status: completed` and record `events` with the completion date.
6. Link to the painting plan and any related sessions.
