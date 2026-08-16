# Finance Domain

The fourth fully implemented domain in Ethan OS.

## Purpose

Track accounts, log transactions, and maintain budgets against categories and financial goals.

## v0.1 objects

- Account (`finance.account`)
- Transaction (`finance.transaction`)
- Budget (`finance.budget`)

## Object flow

```
Account → Transaction (linked to account, optionally a budget)
Budget → aggregates Transactions by category and period
Budget → optionally linked to a planning.goal
```

## Design principles

- Transactions are immutable historical records; corrections go through `workflows/core/revise.md`, not silent edits.
- `amount_actual` and `status` on a Budget are always derived from linked Transactions, never hand-set.
- Balance history is additive (`balance_snapshots`), never overwritten.
- No account numbers, routing numbers, or credentials are stored, even though `ethan-life` is private.
- Review surfaces findings; it never silently changes a budget's plan or an account's status.
