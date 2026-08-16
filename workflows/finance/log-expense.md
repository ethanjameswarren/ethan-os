# Workflow: log-expense

## Purpose

Capture a single expense, income, or transfer and reconcile it against its budget in one pass.

## Steps

1. Run `skills/finance/capture-transaction.md` to create the Transaction.
2. If a Budget exists for the resulting category and current period, run `skills/finance/update-budget.md` to recompute `amount_actual` and `status` with the new transaction included.
3. If the update pushes the Budget to `status: over`, surface this clearly in the output.

## Output

- Transaction object ID
- Budget object ID and updated status, if applicable
- a one-line note if the budget just went over

## Confirmation policy

- Auto-execute: logging a clear transaction and recomputing an existing budget.
- Ask for confirmation: whenever the underlying skills would (ambiguous category, unclear amount/direction).
