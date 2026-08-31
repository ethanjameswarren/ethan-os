# Skill: add-training-location

## Purpose

Create a new `health.training-location` object.

## Input

Natural language describing a training location (e.g. "Add a commercial gym I can use near work").

## Extract

- `name`
- `location_type` (apartment_gym, commercial_gym, home, work_gym, hotel_gym, travel, outdoor)
- `availability` or access notes
- any equipment already known

## Rules

- Do not create a duplicate `id`. Use a stable, URL-safe id.
- If no audit has been performed, set `confidence` to `low` and leave `equipment` empty or minimally populated.
- Mark `status` as `active` unless the user says otherwise.

## Output

Create `ethan-life/domains/health/training-locations/{id}.md` with schema `health.training-location`.

## Relationship types

- `part_of` — location → planning.project or planning.goal if relevant
