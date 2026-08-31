# Skill: capture-financial-snapshot

## Purpose

Create a point-in-time Financial Snapshot of the user's overall financial position.

## Input

Natural language or structured data describing current account balances, income, and expenses.

## Extract

- Date of the snapshot (default to today if not stated)
- Per-account balances and how they were obtained (user_stated, statement, estimated)
- Total income and expenses, if stated or calculable from existing objects

## Steps

1. Load all active `finance.account` objects and their most recent `balance_snapshots` entries.
2. Load all active `finance.income-source` objects and sum to `monthly_income_total`.
3. Load all active `finance.expense-profile-item` objects and sum to `monthly_expense_total`.
4. If the user provides updated balances, record those. For a time-sensitive balance that is stale, ask for an update rather than treating it as current. Existing dated values may be included only with their original date and an explicit stale/unchanged-data label.
5. Calculate `total_assets` (sum of positive-balance accounts), `total_liabilities` (sum of debt/credit balances), and `net_worth`.
6. Calculate `monthly_surplus` = `monthly_income_total` - `monthly_expense_total`.
7. Mark each calculated value explicitly as a calculation.

## Rules

- Do not infer balances the user has not stated; use existing snapshots or leave fields empty.
- Every calculated number must be distinguishable from a user-stated fact.
- Each snapshot is immutable; create a new object rather than editing an existing one.
- Accept partial conversational input. Ask only for missing information necessary to identify an account, date the balances, or avoid a materially misleading result. Record coverage gaps so a partial snapshot is not presented as complete.
- If prior snapshots exist, the skill may note the change from the last snapshot but must not modify the prior snapshot.

## Output

Create a Financial Snapshot object in `ethan-life/domains/finance/snapshots/`.

Use schema `finance.financial-snapshot` and version `1`. See `instructions/domains/finance/object-prompts/financial-snapshot.md`.

## Confirmation policy

- Auto-execute: creating a snapshot from clearly stated or existing balances.
- Ask for confirmation: when account balances are stale (>30 days) and the user has not confirmed them.

## Relationship types

- `derived_from` — snapshot derived from account balance snapshots
- `related_to` — related to prior snapshot for comparison
