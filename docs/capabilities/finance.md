# Finance

## What it does

Track accounts, log transactions, and compare spending against budgets so you can review your financial state without manual spreadsheet work.

## Why it exists

Money decisions are easier when the current picture is reliable and recent. Ethan OS makes transaction logging lightweight and turns budget status into a derived view, not a hand-maintained guess.

## What you do

- Mention an account, transaction, budget, or financial goal.
- Review balances and budget status when you ask for a monthly review.
- Flag discrepancies or corrections so the record stays accurate.

## What Ethan OS does

- Stores account metadata and balance snapshots.
- Logs immutable transactions with category and account links.
- Tracks budgets by period and category.
- Derives `amount_actual` and budget status from transactions.
- Surfaces overspending, underspending, missing transactions, and goals at risk.
- Treats corrections as new revision records, never silent edits.

## Key ideas

- **Transactions are immutable history.** Corrections go through a revision workflow.
- **Budgets are derived.** The system computes actuals from linked transactions.
- **Balance snapshots are additive.** Each new snapshot is recorded, not overwritten.
- **No sensitive numbers.** Account numbers, routing numbers, and credentials are never stored.

## Example interaction

> **You:** "I spent $86 on groceries from checking."  
> **OS:** "Got it. I'll log a transaction against your checking account and groceries budget. Anything else about it?"  
> **You:** "No."  
> **OS:** "Done. Your groceries budget for the month is now 80% used."

## What gets saved

- **Account** — name, type, current balance snapshot, and snapshot history.
- **Transaction** — amount, account, category, date, notes, and budget link if any.
- **Budget** — period, category, planned amount, and derived actual.

## Important behaviors

- Never store account numbers, routing numbers, or credentials.
- Never silently edit an existing transaction; use revision.
- Never derive budget actuals from hand-entered totals.
- Always surface significant deviations, not just totals.

## Related workflows

- [Monthly financial review](../workflows/finance.md)

## Technical implementation

- Workflows: `workflows/finance/`
- Skills: `skills/finance/`
- Schemas: `schemas/domains/finance/account.schema.yaml`, `transaction.schema.yaml`, `budget.schema.yaml`
