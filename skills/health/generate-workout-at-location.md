# Skill: generate-workout-at-location

## Purpose

Build a location-aware workout of a given duration and goal.

## Input

A request like "Build a 45-minute hypertrophy workout at Apartment Gym" or "Create a full-body session at the hotel gym."

## Steps

1. Resolve the `health.training-location` id.
2. Ask for or infer `goal` (strength, hypertrophy, conditioning) and `duration_min`.
3. Apply any `excluded_equipment` for the session.
4. For each target muscle or movement pattern, choose the highest-ranking available exercise:
   - Prefer compound for chest, back, shoulders, legs.
   - Allow isolation for arms, calves, and direct core work.
5. Avoid duplicate exercises across blocks when possible.
6. Assign sets/reps/rest appropriate to the goal.
7. Create a `health.workout` object if the user wants it persisted.

## Output

A list of workout blocks with sets, reps, rest, and equipment.
