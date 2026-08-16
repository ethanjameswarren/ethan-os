# Skill: capture-habit

## Purpose

Define a recurring health behavior to track.

## Input

Natural language stating an intention to track or build a habit.

## Extract

- what is being tracked (`metric_type`): exercise, sleep, meditation, water, medication_adherence, or another clear category
- target frequency, if stated (e.g. "5x per week", "daily")
- whether it supports a broader goal already captured in Planning

## Rules

- Do not invent a target frequency the user has not stated.
- If a habit for the same `metric_type` already exists, update it rather than creating a duplicate.
- Link to a `planning.goal` via `goal_id` only when the user has stated or clearly implied the connection.

## Output

Create or update a Habit object in `ethan-life/domains/health/habits/`.

Use schema `health.habit` and version `1`. See `instructions/domains/health/object-prompts/habit.md`.

## Confirmation policy

- Auto-execute: creating a habit from a clear statement of intent.
- Ask for confirmation: before marking a habit `dropped`.

## Relationship types

- `part_of` — habit → goal
- `related_to` — related habits
