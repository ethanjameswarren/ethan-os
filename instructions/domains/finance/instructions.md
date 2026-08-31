# Finance Domain Instructions

## Scope

Personal finance planning and tracking: accounts, transactions, budgets, income, expenses, debts, financial goals, cash-flow allocation, and periodic financial reviews. No bank API integrations; all data is user-provided.

## Mandatory guidance policy

- Load and apply `instructions/policies/mandatory/financial-guidance.md` to every Finance skill, workflow, recommendation, document, and generated output.
- Treat outputs as educational planning assistance, not professional financial, investment, tax, accounting, or legal advice.
- Qualify recommendations, explain their reasoning, name material methodologies and assumptions, and show meaningful tradeoffs where reasonable approaches disagree.
- Use a concise notice for ordinary recommendations when appropriate; prominently surface the disclaimer and verification/professional-review guidance for substantial, complex, tax-sensitive, investment-specific, or legally significant decisions.
- Do not dilute useful analysis with repetitive long disclaimers during routine factual capture.

## Object flow

```
Account → Transaction (linked to account, optionally to a budget)
Budget → aggregates Transactions by category and period
Budget → optionally linked to a planning.goal or finance.financial-goal

Income Source → feeds Financial Snapshot monthly_income_total
Expense Profile Item → feeds Financial Snapshot monthly_expense_total
Debt → tracked for payoff planning, linked to financial goals
Financial Goal → target amount with progress tracking
Allocation Policy → priority-ordered cash-flow hierarchy
Financial Snapshot → point-in-time position (assets, liabilities, net worth)
Financial Review → periodic assessment combining all of the above
```

## Account handling

- Use `skills/finance/capture-account.md` to register a new account or record a balance snapshot.
- Store Accounts in `ethan-life/domains/finance/accounts/`.
- Append to `balance_snapshots` rather than overwriting history; each snapshot is a dated fact.
- Each balance snapshot records a `source` (user_stated, statement, estimated) for provenance.
- Account types include checking, savings, cash, credit_card, taxable_investment, investment, brokerage, retirement_401k, retirement_ira, retirement_roth_ira, hsa, loan, mortgage, auto_loan, student_loan, money_market, cd, other_asset, other_debt, and other.

## Transaction handling

- Use `skills/finance/capture-transaction.md` to convert a mentioned purchase, expense, income, or transfer into a Transaction object.
- Store Transactions in `ethan-life/domains/finance/transactions/`.
- `amount` is always a positive magnitude; `direction` (`expense` | `income` | `transfer`) carries the sign.
- Categorize consistently; prefer reusing an existing category over inventing a near-duplicate (e.g. "Groceries" vs "Grocery").
- Link a transaction to a Budget (`budget_id`) when one exists for its category and period.

## Budget handling

- Use `skills/finance/update-budget.md` to create or update a Budget for a category and period.
- Store Budgets in `ethan-life/domains/finance/budgets/`.
- `amount_actual` and `status` are recomputed from linked Transactions during review; do not hand-edit them outside that process.
- A Budget may link to a `planning.goal` via `goal_id` when it supports a broader financial objective (e.g. "Save for a house down payment").

## Income handling

- Use `skills/finance/capture-income-source.md` to register or update an income source.
- Store Income Sources in `ethan-life/domains/finance/income-sources/`.
- When income changes, create a new record or add an `## Evolution` entry with the new `effective_date`; never silently overwrite.
- Pre-tax deductions (401k, HSA, insurance) and post-tax deductions are captured on the income source when stated.

## Expense profile handling

- Use `skills/finance/capture-expense-profile.md` to register or update a recurring expense.
- Store Expense Profile Items in `ethan-life/domains/finance/expense-profile/`.
- Classify each as `essential`, `committed`, or `discretionary`; confirm with the user if ambiguous. Fixed/variable behavior may be recorded separately when useful.
- Debt minimum payments are tracked on the `finance.debt` object, not as expense profile items.

## Debt handling

- Use `skills/finance/capture-debt.md` to register or update a debt.
- Store Debts in `ethan-life/domains/finance/debts/`.
- Append to `balance_history` rather than overwriting; each entry is a dated fact.
- Promotional rate details (`promo_rate_pct`, `promo_end_date`, `regular_rate_after_promo_pct`) are critical for payoff planning; always capture when stated.

## Financial goal handling

- Use `skills/finance/capture-financial-goal.md` to register or update a financial goal.
- Store Financial Goals in `ethan-life/domains/finance/goals/`.
- Append to `progress_history` when updating progress.
- For debt payoff goals, link to the specific `finance.debt` via `related_debt_id`.

## Cash-flow allocation

- Use `skills/finance/allocate-next-dollar.md` to apply the user's allocation policy.
- Store Allocation Policies in `ethan-life/domains/finance/policies/`.
- The allocation policy is a user-stated preference; the OS does not override the user's tier ordering.
- When the policy changes, create a new one with `supersedes_id`; never overwrite.

## Financial snapshot

- Use `skills/finance/capture-financial-snapshot.md` to capture a point-in-time position.
- Store Snapshots in `ethan-life/domains/finance/snapshots/`.
- Each snapshot is immutable; create a new one rather than editing an existing one.
- Calculated values (net_worth, surplus) must be explicitly labeled as calculations.

## Debt payoff planning

- Use `skills/finance/plan-debt-payoff.md` to analyze strategies (avalanche, snowball, promo-aware, custom).
- Always present tradeoffs; never auto-select a strategy.
- Use `skills/finance/calculation-guidance.md` or `scripts/finance/finance_calculator.py` for payoff math.

## 401k planning

- Use `skills/finance/compute-401k-target.md` to calculate per-paycheck contribution targets.
- All outputs are calculations; label them explicitly.

## Review

- Use `skills/finance/suggest-spending-insights.md` to identify categories over/under budget, accounts with stale snapshots, and budgets with no recent transaction activity.
- `workflows/finance/monthly-budget-review.md` runs budget-only reviews per period.
- `workflows/finance/financial-review.md` runs comprehensive reviews including snapshot, income, expenses, debt, goals, and allocation.
- `skills/finance/orchestrate-financial-review.md` coordinates the comprehensive review.
- Reviews do not silently alter any finance objects.

## Epistemological discipline

Every number in a finance output must be labeled as one of:

- **fact**: user stated this value directly.
- **calculation**: derived from user facts using a defined formula.
- **assumption**: the OS filled in a value the user did not state; must be flagged.
- **recommendation**: a suggested action; never auto-applied.

All time-sensitive values must include the date they were recorded or calculated.

## Confidentiality

- `ethan-life` is private, but avoid storing full account numbers, card numbers, routing numbers, credentials, or security codes in any Finance object. Reference accounts by their own `id`/title, not by sensitive identifiers.

## Relationships

- Use inline typed links (see `docs/architecture/relationships.md`).
- Common relations: `part_of` (transaction → budget, budget → goal, debt → financial goal), `related_to`, `revised_by`, `derived_from`, `supports`.

## Lifecycle

- Account: `active` → `closed`.
- Budget: `unknown` → `on_track` | `over` | `under`, recomputed on review.
- Income Source: `active` → `ended`.
- Expense Profile Item: `active` → `ended`.
- Debt: `active` → `paid_off` | `deferred` | `in_collections`.
- Financial Goal: `active` → `achieved` | `abandoned` | `on_hold`.
- Transactions are immutable records of what happened; corrections go through `workflows/core/revise.md` with an `## Evolution` note rather than silent edits.
- Snapshots, Allocation Policies, and Financial Reviews are immutable records; new versions replace old ones via `supersedes_id` or new objects.
