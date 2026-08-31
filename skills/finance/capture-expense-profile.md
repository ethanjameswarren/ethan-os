# Skill: capture-expense-profile

## Purpose

Create or update an Expense Profile Item from user-provided expense information.

## Input

Natural language describing a recurring or expected expense.

## Extract

- Category (Housing, Groceries, Subscriptions, etc.)
- Amount and frequency
- Whether fixed, variable, or discretionary
- Whether essential (need vs. want)
- Effective date, if stated

## Rules

- Record the expense as stated; do not infer amounts the user has not provided.
- Prefer reusing existing category strings from the user's profile over creating near-duplicates.
- If an existing expense-profile-item matches (same category, same payee/description), update it via `## Evolution` rather than creating a duplicate.
- Capture `classification` as `essential`, `committed`, or `discretionary`. Do not infer it when the treatment is materially ambiguous; ask the user. Optionally record fixed/variable behavior separately as `expense_type`.
- `essential` is a user judgment; suggest but always confirm.

## Output

Create or update an Expense Profile Item in `ethan-life/domains/finance/expense-profile/`.

Use schema `finance.expense-profile-item` and version `1`. See `instructions/domains/finance/object-prompts/expense-profile-item.md`.

## Confirmation policy

- Auto-execute: creating from a clear statement of category, amount, and frequency.
- Ask for confirmation: when the essential/committed/discretionary classification is ambiguous, or when updating an existing item's amount.

## Relationship types

- `part_of` — expense linked to a budget
- `related_to` — related expenses in the same category
