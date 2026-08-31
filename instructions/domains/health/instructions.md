# Health Domain Instructions

## Scope

Track recurring health habits, log metrics against them, record medical notes, and plan training based on available equipment and training locations.

## Object flow

```
Habit → Log Entry (linked to habit, recomputes current_streak)
Medical Note (standalone; may link to a Habit, e.g. medication adherence)

Training Location → Equipment inventory + Exercise capability mapping
Workout → training_location + exercises selected from location-capable candidates
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

## Training location and equipment handling

- Use `skills/health/audit-gym-equipment.md` to add or update a `health.training-location` object from a photo audit, walkthrough, or other source.
- Use `skills/health/add-training-location.md` to create a new location (e.g. commercial gym, hotel gym, home) before an audit.
- Store Training Locations in `ethan-life/domains/health/training-locations/`.
- Each Training Location carries a canonical `equipment` inventory with `canonical_type` from `ethan-os/config/health/equipment-taxonomy.yaml`.
- Mark `confidence` and `audit_date` for every equipment entry. Use `unknown` rather than guessing weights, quantities, or model numbers.
- Temporary equipment unavailability is captured per-session, not by editing the location object.

## Exercise capability mapping

- `ethan-os/config/health/exercise-library.yaml` is the canonical exercise catalog.
- Each exercise declares `required_equipment` as a list of canonical equipment types.
- Workout planning is location-aware: candidate exercises are filtered to those whose required equipment is present and not temporarily excluded.
- `skills/health/show-available-exercises.md` and `skills/health/find-exercise-substitution.md` use this mapping.
- `skills/health/generate-workout-at-location.md` builds a workout from a target location.

## Workout planning

- Workouts are `health.workout` objects linked to a `health.training-location`.
- Workout generation follows:
  ```
  goal / program → movement or muscle target → candidate exercises
  → equipment requirements → location inventory → feasible exercises
  → rank/select exercises → workout blocks
  ```
- If an exercise is unavailable, use the substitution hierarchy first; fall back to matching `movement_pattern` and `primary_muscles`.
- Preserve stability, loading potential, isolation, and hypertrophy/strength suitability when ranking substitutes.
- `excluded_equipment` supports temporary constraints such as "Smith machine is occupied" without mutating the permanent inventory.

## Review

- Use `skills/health/suggest-habit-insights.md` to identify broken streaks, habits with no recent logs, and medical follow-ups coming due.
- `workflows/health/weekly-health-review.md` runs this periodically and surfaces findings; it does not silently alter habit status or streaks outside of normal recomputation.

## Confidentiality

- `ethan-life` is private, but Medical Notes should still avoid storing full medical record numbers, insurance member IDs, or other identifiers not needed for personal reference. Summarize provider guidance in Ethan's own words where practical.

## Relationships

- Use inline typed links (see `docs/architecture/relationships.md`).
- Common relations: `part_of` (log entry → habit, habit → goal), `related_to` (medical note → habit, workout → location), `revised_by`.

## Lifecycle

- Habit: `active` → `paused` → `dropped`, or back to `active`.
- Medical Note: `active` → `monitoring` → `resolved`.
- Training Location: `active` → `inactive` → `active`.
- Workout: `planned` → `completed` / `skipped` / `revised`.
