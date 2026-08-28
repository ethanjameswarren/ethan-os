# Workflow: Monthly Financial Review

## What you do

Ask for a financial review or mention a transaction, account, or budget you want to check.

Example:

> **You:** "How am I doing against my budgets this month?"

## What Ethan OS does

1. Loads accounts, balance snapshots, transactions, and budgets for the period.
2. Derives actual spending from linked transactions.
3. Compares actuals to planned budgets by category and period.
4. Surfaces significant deviations, missing transactions, and budget goals at risk.
5. Presents a concise summary with trends and notable items.

## Conceptual stages

- **Aggregate** — collect transactions and balance snapshots.
- **Derive** — compute budget actuals from the data.
- **Compare** — actuals vs. planned by category.
- **Surface** — flag deviations and patterns.
- **Summarize** — present a human-readable review.

## Outputs

- A review summary with budget status and notable transactions.
- Flags for missing, miscategorized, or unusual items.
- Suggested corrections or follow-ups, not applied automatically.

## Safeguards

- Budget actuals are always derived from transactions, never hand-set.
- Existing transactions are not edited silently; corrections use a revision workflow.
- Account numbers, routing numbers, and credentials are never stored.

## Technical details

- Workflows: `workflows/finance/monthly-review.md`
- Skills: `skills/finance/aggregate-transactions.md`, `skills/finance/check-budget-health.md`
- Schemas: `schemas/domains/finance/account.schema.yaml`, `transaction.schema.yaml`, `budget.schema.yaml`
