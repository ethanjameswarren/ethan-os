# Finance Domain Instructions

## Scope

Track accounts, log transactions, and maintain budgets against categories and financial goals.

## Object flow

```
Account → Transaction (linked to account, optionally to a budget)
Budget → aggregates Transactions by category and period
Budget → optionally linked to a planning.goal
```

## Account handling

- Use `skills/finance/capture-account.md` to register a new account or record a balance snapshot.
- Store Accounts in `ethan-life/domains/finance/accounts/`.
- Append to `balance_snapshots` rather than overwriting history; each snapshot is a dated fact.

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

## Review

- Use `skills/finance/suggest-spending-insights.md` to identify categories over/under budget, accounts with stale snapshots, and budgets with no recent transaction activity.
- `workflows/finance/monthly-budget-review.md` runs this per period and surfaces findings; it does not silently alter budgets.

## Confidentiality

- `ethan-life` is private, but avoid storing full account numbers, card numbers, routing numbers, credentials, or security codes in any Finance object. Reference accounts by their own `id`/title, not by sensitive identifiers.

## Relationships

- Use inline typed links (see `docs/architecture/relationships.md`).
- Common relations: `part_of` (transaction → budget, budget → goal), `related_to`, `revised_by`.

## Lifecycle

- Account: `active` → `closed`.
- Budget: `unknown` → `on_track` | `over` | `under`, recomputed on review.
- Transactions are immutable records of what happened; corrections go through `workflows/core/revise.md` with an `## Evolution` note rather than silent edits.
