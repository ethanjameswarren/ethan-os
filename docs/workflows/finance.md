# Finance Workflows

## What you do

Mention an income, expense, debt, account, transaction, budget, financial goal, or ask for a review or analysis.

Examples:

> **You:** "I spent $86 on groceries from checking."
> **You:** "I make $85k salary, paid biweekly."
> **You:** "My rent is $1,800/month."
> **You:** "I owe $4,500 on my Chase card at 21.99%."
> **You:** "I want a $10k emergency fund."
> **You:** "How should I pay off my debts?"
> **You:** "Where should my next dollar go?"
> **You:** "How did I do financially this month?"

## What Ethan OS does

1. Routes to the appropriate finance workflow based on intent.
2. Captures or updates the relevant financial objects.
3. Derives computed values (budget actuals, net worth, payoff estimates) from user facts.
4. Labels every number as fact, calculation, assumption, or recommendation.
5. Dates all time-sensitive values.
6. Presents findings and options; never auto-applies changes.

## Available workflows

| Workflow | Purpose |
|----------|---------|
| [Log expense](../../workflows/finance/log-expense.md) | Capture a transaction and update its budget |
| [Capture financial snapshot](../../workflows/finance/capture-financial-snapshot.md) | Record a point-in-time financial position |
| [Capture income](../../workflows/finance/capture-income.md) | Register or update income sources |
| [Capture expense profile](../../workflows/finance/capture-expense-profile.md) | Build or update recurring expense profile |
| [Set financial goals](../../workflows/finance/set-financial-goals.md) | Define and prioritize financial goals |
| [Plan debt payoff](../../workflows/finance/plan-debt-payoff.md) | Compare avalanche/snowball/promo-aware/custom strategies |
| [Allocate cash flow](../../workflows/finance/allocate-cash-flow.md) | Define or apply cash-flow priority hierarchy |
| [Compute 401k target](../../workflows/finance/compute-401k-target.md) | Calculate per-paycheck 401k contributions |
| [Monthly budget review](../../workflows/finance/monthly-budget-review.md) | Budget-focused period review |
| [Financial review](../../workflows/finance/financial-review.md) | Comprehensive periodic financial assessment |

## Safeguards

- All workflows follow the [mandatory financial-guidance policy](../../instructions/policies/mandatory/financial-guidance.md): outputs are educational planning assistance, recommendations are qualified and explainable, and high-impact decisions surface verification and professional-review guidance.
- Budget actuals are always derived from transactions, never hand-set.
- Existing transactions are not edited silently; corrections use a revision workflow.
- Account numbers, routing numbers, and credentials are never stored.
- Debt payoff strategies are always presented with tradeoffs; the user chooses.
- Allocation priorities reflect user preferences; the OS does not override them.
- The review is read-only unless the user explicitly confirms a change.

## Technical details

- Workflows: `workflows/finance/`
- Skills: `skills/finance/`
- Calculation guidance: `skills/finance/calculation-guidance.md`
- Calculator: `scripts/finance/finance_calculator.py`
- Tests: `scripts/test-finance-calculator.py`
- Schemas: `schemas/domains/finance/`
