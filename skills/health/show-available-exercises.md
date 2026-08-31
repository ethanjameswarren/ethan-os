# Skill: show-available-exercises

## Purpose

List exercises that can be performed at a given training location, optionally filtered by muscle or movement pattern.

## Input

A query like "What chest exercises can I do at Apartment Gym?" or "Show hamstring exercises at the hotel gym."

## Steps

1. Load the `health.training-location` object.
2. Build the set of available `canonical_type` equipment, applying any temporary exclusions.
3. Filter `ethan-os/config/health/exercise-library.yaml` for exercises whose `required_equipment` is a subset of available types.
4. If a muscle or movement pattern is specified, filter further.
5. Rank by `loading_potential` and `hypertrophy_suitability` for hypertrophy goals, or `strength_suitability` for strength goals.

## Output

A concise list of exercises with equipment and loading notes.
