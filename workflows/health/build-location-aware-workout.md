# Workflow: build-location-aware-workout

## Purpose

Generate a workout that only includes exercises feasible at a specified training location.

## Steps

1. Load the `health.training-location` object for the requested location.
2. Capture `goal` and `duration_min`. Default to `hypertrophy` and `45` if not stated.
3. Capture any `excluded_equipment` for the session (e.g. occupied machines).
4. Run `skills/health/generate-workout-at-location.md` to select and rank exercises.
5. Produce a `health.workout` object if the user wants to save the plan.
6. If an exercise in an existing plan is unavailable, run `skills/health/find-exercise-substitution.md` and present the substitution.

## Output

- A location-aware workout with exercises, sets, reps, rest, and equipment
- Optional `health.workout` object in `ethan-life/domains/health/workouts/`

## Confirmation policy

- Read-only if the user only wants suggestions.
- Auto-execute for creating a planned `health.workout` from a clear request.
