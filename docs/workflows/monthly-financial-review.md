# Monthly Financial Review

## What you do

Ask Ethan OS to review a budget period.

Examples:

> **You:** "How did I do financially this month?"  
> **You:** "Let's review my budget for August."  
> **You:** "What should I look at in my spending this month?"

## What Ethan OS does

1. **Loads the canonical data** — accounts, budgets, and transactions for the period you specify.
2. **Recomputes budget status** — every `amount_actual` and `status` is derived from the linked transactions. Nothing is hand-set.
3. **Surfaces what needs attention** — identifies over-budget categories, under-utilized categories, uncategorized or unlinked transactions, stale account snapshots, and goal-linked budgets falling behind.
4. **Presents a prioritized summary** — findings are ranked so you see the most consequential items first.
5. **Suggests next steps** — for example, re-examining a missing category, updating a planned amount, or logging a missed transaction.

## Example interaction

> **You:** "How did I do in August?"  
> **OS:** "For August, three categories need attention:  
> - Groceries: $540 actual vs. $500 planned.  
> - Dining: $120 actual vs. $200 planned — you have $80 left.  
> - One transaction of $150 has no category.  
> Groceries is tied to your household budget goal, so that's the highest priority to review."

## What gets saved

- Updated `finance.budget` objects with recomputed `amount_actual` and `status`.
- The review summary itself is returned to you; it is not persisted unless you ask.
- No existing account, transaction, or budget is edited automatically.

## Core principle

**The OS helps interpret financial state. It does not turn the user into a spreadsheet maintainer.**

The canonical records are your financial facts. The OS recomputes results from those facts and adds observations. You decide what to change.

## Distinctions

- **Recorded facts** — the accounts, transactions, and balance snapshots you provided.
- **Calculated results** — budget actuals and statuses, derived from transactions.
- **AI observations/recommendations** — what the OS suggests you look at, not applied automatically.

## Current capabilities and known gaps

What works now:

- Recomputing budget actuals from linked transactions.
- Surfacing over-budget, under-utilized, uncategorized, and goal-linked items.
- Prioritizing findings for human review.

Now also available — the comprehensive financial review (`workflows/finance/financial-review.md`) extends this budget-focused review with:

- Financial snapshot comparison (net worth change).
- Income source assessment.
- Expense profile vs. actual spending.
- Debt trajectory and payoff progress.
- Financial goal progress.
- Allocation policy effectiveness.
- Explicitly labeled findings (fact / calculation / assumption / recommendation).

Not yet implemented:

- Automatic detection of recurring vs. one-off expenses.
- Carrying explicit observations forward into next-period planning.

## Safeguards

- Budget actuals are always derived, never hand-set.
- Existing transactions are not edited; corrections go through a revision workflow.
- No account numbers, routing numbers, or credentials are stored.
- The review is read-only unless you explicitly confirm a change.

## Technical details

- Workflow: `workflows/finance/monthly-budget-review.md`
- Skills: `skills/finance/update-budget.md`, `skills/finance/suggest-spending-insights.md`
- Schemas: `schemas/domains/finance/account.schema.yaml`, `transaction.schema.yaml`, `budget.schema.yaml`
- For the broader Finance domain, see [Finance](../capabilities/finance.md).
- For comprehensive financial reviews, see `workflows/finance/financial-review.md`.
