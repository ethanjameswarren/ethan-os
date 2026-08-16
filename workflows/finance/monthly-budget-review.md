# Workflow: monthly-budget-review

## Purpose

Reconcile the past period's budgets against actual transactions and surface what needs attention.

## Steps

1. For each Budget in the specified (default: just-elapsed) period, run `skills/finance/update-budget.md` to recompute `amount_actual` and `status`.
2. Run `skills/finance/suggest-spending-insights.md` across the updated Budgets, all Accounts, and the period's Transactions.
3. Return the prioritized findings to the user.

## Output

- updated Budget statuses for the period
- prioritized list of findings with reasons
- no Account or Transaction objects are modified by this workflow

## Confirmation policy

- Auto-execute: recomputing budget actuals/status from existing transactions.
- Read-only beyond that: any planned-amount change or reallocation the user decides on goes through `skills/finance/update-budget.md` or `workflows/core/revise.md`.
