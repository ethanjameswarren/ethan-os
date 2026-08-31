# Skill: find-exercise-substitution

## Purpose

Find the closest available substitute for an exercise at a given location.

## Input

A request like "Replace barbell back squat with something at Apartment Gym" or "The Smith machine is occupied; what should I do for chest?"

## Steps

1. Load the location and exercise catalog.
2. If the requested exercise is available and no equipment is excluded, return it.
3. If unavailable, use the exercise's ordered `substitutes` list and return the first available option.
4. If no `substitutes` are available, fall back to exercises with the same `movement_pattern` and overlapping `primary_muscles`.
5. Rank by stability, loading potential, isolation, and goal suitability. Preserve tradeoff information (e.g. "less stability, more load").

## Output

The best substitute and a short note explaining the tradeoff.
