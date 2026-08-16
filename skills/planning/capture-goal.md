# Skill: capture-goal

## Purpose

Convert a stated aspiration, objective, or intention into a durable Goal object.

## Input

Natural language describing something Ethan wants to achieve, in any form: a passing remark, a deliberate statement, or an answer to a clarifying question.

## Extract

- what the goal actually is, stated plainly
- why it matters (motivation, underlying value, or problem it solves)
- apparent horizon: short_term (weeks), medium_term (months/a quarter), long_term (a year or more)
- success criteria: concrete, checkable statements of "done" or "achieved"
- target date, if stated

## Rules

- Do not invent success criteria the user has not provided or clearly implied. If none are available, ask a single concise clarifying question before finalizing.
- Do not assign a horizon that is not stated or clearly implied by the content.
- If the new goal substantively overlaps an existing Goal, update the existing object instead of creating a duplicate.

## Output

Create or update a Goal object in `ethan-life/domains/planning/goals/`.

Use schema `planning.goal` and version `1`. See `instructions/domains/planning/object-prompts/goal.md` for the full field list.

## Confirmation policy

- Auto-execute: creating a draft goal from a clear statement with at least one success criterion.
- Ask for confirmation: when no success criteria can be inferred, when horizon is ambiguous, or when marking a goal `achieved` or `abandoned`.

## Relationship types

- `related_to` — related goals
- `part_of` — sub-goal of a larger goal, if applicable
