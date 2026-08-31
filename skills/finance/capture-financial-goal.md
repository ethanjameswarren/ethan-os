# Skill: capture-financial-goal

## Purpose

Create or update a Financial Goal representing a specific monetary objective.

## Input

Natural language describing a financial goal (emergency fund, debt payoff, savings target, etc.).

## Extract

- Goal type
- Target amount
- Target date, if stated
- Monthly contribution plan, if stated
- Current progress, if stated
- Priority relative to other goals, if stated
- Why it matters to the user, if stated

## Rules

- Record the goal as stated; do not infer target amounts, dates, or priorities.
- If an existing financial goal matches (same type and target), update it rather than creating a duplicate.
- Append to `progress_history` when updating `current_amount` rather than overwriting.
- `monthly_contribution` is a plan; distinguish it from actual transaction history.
- For debt payoff goals, link to the specific `finance.debt` via `related_debt_id`.
- `priority` is user-stated; if the user does not state a priority, leave it unset rather than guessing.
- Goals may link to a `planning.goal` if the user wants integration with their broader planning system.

## Output

Create or update a Financial Goal in `ethan-life/domains/finance/goals/`.

Use schema `finance.financial-goal` and version `1`. See `instructions/domains/finance/object-prompts/financial-goal.md`.

## Confirmation policy

- Auto-execute: creating from a clear statement of goal type and target amount.
- Ask for confirmation: when the goal type or target is ambiguous, or when changing priority.

## Relationship types

- `part_of` — goal linked to a planning.goal
- `related_to` — related financial goals
- `supports` — goal supporting a debt payoff
