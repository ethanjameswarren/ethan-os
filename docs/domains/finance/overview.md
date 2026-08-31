# Finance Domain

## Purpose

Personal finance planning and tracking — accounts, transactions, budgets, income sources, expense profiles, debts, financial goals, cash-flow allocation policies, periodic snapshots, debt payoff strategies, 401k targeting, and orchestrated financial reviews. No bank APIs; all data is user-provided.

## Guidance boundary

Finance outputs are educational planning assistance rather than professional financial, investment, tax, accounting, or legal advice. Recommendations identify their methodology, assumptions, reasoning, uncertainty, and meaningful tradeoffs under the [mandatory financial-guidance policy](../../../instructions/policies/mandatory/financial-guidance.md).

## Objects

- Account (`finance.account`) — financial accounts with typed categories and dated balance snapshots with provenance.
- Transaction (`finance.transaction`) — immutable records of income, expenses, and transfers.
- Budget (`finance.budget`) — period/category budgets with derived actuals.
- Financial Snapshot (`finance.financial-snapshot`) — point-in-time position: assets, liabilities, net worth, surplus.
- Income Source (`finance.income-source`) — recurring or one-time income with pay frequency, deductions, and effective dates.
- Expense Profile Item (`finance.expense-profile-item`) — recurring expenses classified as fixed, variable, or discretionary.
- Debt (`finance.debt`) — obligations with balances, rates, minimums, promo terms, and payoff tracking.
- Financial Goal (`finance.financial-goal`) — monetary targets with progress tracking and priority ranking.
- Allocation Policy (`finance.allocation-policy`) — priority-ordered cash-flow hierarchy.
- Financial Review (`finance.financial-review`) — periodic assessment combining all finance data.

## Object flow

```
Income Source ─┐
               ├─→ Financial Snapshot (monthly income/expense totals, net worth)
Expense Profile ┘         │
                          ├─→ Financial Review (periodic assessment)
Account → Transaction ──→ Budget ──→ Financial Review
                                         │
Debt ──→ Financial Goal ──→ Allocation Policy ──→ Financial Review
```

## Design principles

- Transactions are immutable historical records; corrections go through `workflows/core/revise.md`, not silent edits.
- `amount_actual` and `status` on a Budget are always derived from linked Transactions, never hand-set.
- Balance history is additive (`balance_snapshots`), never overwritten.
- Every number is explicitly labeled as fact, calculation, assumption, or recommendation.
- Every time-sensitive value is dated.
- No account numbers, routing numbers, or credentials are stored, even though `ethan-life` is private.
- Review surfaces findings; it never silently changes a budget's plan or an account's status.
- Debt payoff strategies are always presented with tradeoffs; the OS never auto-selects a strategy.
- Allocation policies reflect user priorities; the OS does not override the user's ordering.
- Snapshots, policies, and reviews are immutable; new versions replace old ones via references.
- No bank APIs or external data providers; all data comes from the user.
- Recommendations are qualified possible strategies, explain their reasoning, and identify the methodology and assumptions driving them.
- Substantial or tax-sensitive decisions prominently surface verification needs and professional-review guidance.
