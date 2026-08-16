# Finance Domain Examples

## Capture

> spent $64 at trader joes today, groceries as usual

## Resulting objects

- Transaction: amount 64, direction expense, category "Groceries", merchant "Trader Joe's", date today
- If a Budget "Groceries — 2026-08" exists, `update-budget` recomputes `amount_actual` to include this transaction and re-evaluates `status`.

## Budget review

> ## how am i doing on groceries this month

`monthly-budget-review` recomputes the "Groceries — 2026-08" budget, finds `amount_actual` has exceeded `amount_planned`, and reports:

- Groceries is `over` by $42 this month, driven largely by two Trader Joe's visits and one Costco run.

## Account snapshot

> checking account is at $2,340 as of today

`capture-account` appends a new entry to `balance_snapshots` for the existing Checking account rather than creating a duplicate account.
