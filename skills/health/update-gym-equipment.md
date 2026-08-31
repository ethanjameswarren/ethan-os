# Skill: update-gym-equipment

## Purpose

Update a `health.training-location` object when a single piece of equipment changes.

## Input

A statement such as "The leg press at Apartment Gym is out of order" or "They added a new rack."

## Extract

- location id
- equipment `canonical_type`
- what changed (added, removed, out of order, quantity, weight range)
- confidence

## Rules

- Do not overwrite the entire inventory. Change only the affected item(s).
- Update `updated_at` and `audit_date` if the change is from a new observation.
- If equipment is temporarily unavailable, set `availability` on the record. For session-only constraints, use `excluded_equipment` in a workout.

## Output

Edit the relevant `ethan-life/domains/health/training-locations/{id}.md`.
