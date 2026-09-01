# Workflow: onboarding

## Purpose

Seed a new or empty finance domain by capturing the foundational objects in the right order: accounts first, then income, expenses, budgets, debts, goals, and allocation strategy. Transactions and bank CSV import are explicitly out of scope for this workflow.

## Steps

1. Load finance domain instructions, schemas, and the mandatory financial-guidance policy.
2. Capture accounts. Use `skills/finance/capture-account.md` for each account. Continue until the user indicates they are done. Do not store account numbers, routing numbers, or credentials.
3. Capture income sources. Use `skills/finance/capture-income-source.md` for each recurring or expected income stream.
4. Capture expense profile items. Use `skills/finance/capture-expense-profile.md` for each known recurring bill or expense.
   - Ask for the exact last payment when the user has it, then ask for the rounded/planned amount they want to budget.
   - Record known amounts as facts.
   - When rounding, store the rounded planned value as `amount` and keep the exact payment and buffer percentage in `notes`.
   - Do not push rounding if the user says the budget is tight or the rounded amount would leave too little room for other categories; use the exact amount and surface the tradeoff instead.
   - For bills the user knows exist but cannot yet quantify, create an estimated item and label the amount as an `assumption`; mark it for later update.
5. Build initial budgets. Use `skills/finance/update-budget.md` for each expense category and period, using the expense profile's planned amount as `amount_planned`.
6. Capture debts. Use `skills/finance/capture-debt.md` for each credit card, loan, mortgage, or other obligation.
7. Capture financial goals. Use `skills/finance/capture-financial-goal.md` for targets such as emergency fund, debt payoff, or savings.
8. If the user wants payoff or allocation guidance, run `skills/finance/plan-debt-payoff.md` and/or `skills/finance/allocate-next-dollar.md`. Present options; do not auto-apply a strategy.
9. Capture an initial financial snapshot. Use `skills/finance/capture-financial-snapshot.md` to record the starting position.

## Output

- New or updated Account, Income Source, Expense Profile, Budget, Debt, Financial Goal, and Financial Snapshot objects in `ethan-life/domains/finance/`.
- A summary of:
  - accounts captured
  - income and expense totals
  - budget categories established
  - debts and goals recorded
  - any items marked as estimated or incomplete
  - the chosen payoff/allocation strategy, if any

## Out of scope

- Transaction logging and bank CSV import are not part of this workflow. They are addressed separately by `workflows/finance/log-expense.md` and future import tooling.

## Confirmation policy

- Auto-execute: creating objects from clear, complete statements.
- Ask for confirmation: when an item could update an existing object, when a category or classification is ambiguous, or when a value is explicitly an estimate.
