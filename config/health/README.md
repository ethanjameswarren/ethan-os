# Health Exercise / Equipment Reference Data

This directory holds canonical, reusable data for the health domain.

- `equipment-taxonomy.yaml` — canonical equipment type IDs used by exercise definitions, training locations, and workout generation.
- `exercise-library.yaml` — canonical exercise catalog with required equipment, movement patterns, muscle targets, and substitution preferences.

These files are read by:

- `scripts/health/gym_query.py`
- `skills/health/show-available-exercises.md`
- `skills/health/find-exercise-substitution.md`
- `skills/health/generate-workout-at-location.md`
- `workflows/health/build-location-aware-workout.md`

Personal gym inventories and workouts live in `ethan-life/domains/health/`.
