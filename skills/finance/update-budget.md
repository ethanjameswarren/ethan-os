# Skill: update-budget

## Purpose

Create or update a Budget for a category and period, and recompute its actual spend/status from linked Transactions.

## Input

- category and period (explicit, e.g. "Groceries for August 2026"), or a request to review an existing budget
- `amount_planned`, if creating or changing a plan
- all Transaction objects with matching `category` and `date` within the `period`

## Steps

1. Resolve or create the Budget for the given category and period. One Budget per category per period; update the existing one rather than duplicating.
2. Sum linked and matching Transactions to compute `amount_actual`.
3. Set `status`:
   - `on_track` if `amount_actual` is at or below `amount_planned` with the period not yet elapsed
   - `under` if the period has elapsed and `amount_actual` is below `amount_planned`
   - `over` if `amount_actual` exceeds `amount_planned`
   - `unknown` if there is insufficient transaction data
4. Link matching Transactions to this Budget via `budget_id` if not already linked.

## Rules

- Never hand-set `amount_actual` or `status`; both must be derived from linked Transactions.
- Do not invent a `amount_planned` the user has not stated when creating a new Budget.

## Output

Create or update a Budget object in `ethan-life/domains/finance/budgets/`.

Use schema `finance.budget` and version `1`. See `instructions/domains/finance/object-prompts/budget.md`.

## Confirmation policy

- Auto-execute: recomputing `amount_actual`/`status` from existing transactions, and creating a new budget when `amount_planned` is explicitly given.
- Ask for confirmation: when no `amount_planned` has been stated for a new category, or before changing an existing `amount_planned`.

## Relationship types

- `part_of` — budget → planning.goal (via `goal_id`)
- `related_to` — related budgets
