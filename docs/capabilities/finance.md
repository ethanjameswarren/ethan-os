# Finance

## What it does

Personal finance planning and tracking: accounts, transactions, budgets, income sources, expense profiles, debts, financial goals, cash-flow allocation, debt payoff strategies, 401k targeting, point-in-time snapshots, and orchestrated financial reviews. No bank APIs — all data is user-provided.

## Why it exists

Money decisions are easier when the current picture is reliable and recent. Ethan OS makes financial capture lightweight, turns budget status into a derived view, provides structured debt payoff analysis, and helps you direct surplus cash flow intentionally — without spreadsheets.

## Financial guidance notice

Ethan OS provides educational financial-planning assistance, not professional financial, investment, tax, accounting, or legal advice. Recommendations are possible strategies based on available user information and stated methodologies; outcomes are uncertain. Independently verify important calculations, contribution limits, taxes, and account rules, and consider an appropriately qualified professional for high-impact, complex, tax-sensitive, or legally significant decisions. See the [full mandatory financial-guidance policy](../../instructions/policies/mandatory/financial-guidance.md).

## What you do

- Tell the OS about your accounts, income, expenses, debts, and financial goals.
- Log transactions as they happen.
- Ask for a financial snapshot, debt payoff comparison, or cash-flow allocation.
- Ask for a periodic financial review.
- Flag discrepancies or corrections so the record stays accurate.

## What Ethan OS does

- Stores account metadata and balance snapshots (with provenance: user_stated, statement, estimated).
- Logs immutable transactions with category and account links.
- Tracks budgets by period and category; derives actuals from transactions.
- Records income sources with pay frequency, gross/net, and deductions.
- Records recurring expense profiles (fixed, variable, discretionary).
- Tracks debts with interest rates, minimum payments, promotional terms, and balance history.
- Manages financial goals with progress tracking and priority ranking.
- Maintains a priority-ordered cash-flow allocation policy.
- Captures point-in-time financial snapshots (assets, liabilities, net worth, surplus).
- Compares debt payoff strategies (avalanche, snowball, promo-aware, custom) with tradeoffs.
- Calculates per-paycheck 401k contributions to hit annual targets.
- Conducts orchestrated periodic financial reviews combining all of the above.
- Explicitly labels every number as fact, calculation, assumption, or recommendation.
- Dates every time-sensitive value.
- Treats corrections as new revision records, never silent edits.

## Key ideas

- **Transactions are immutable history.** Corrections go through a revision workflow.
- **Budgets are derived.** The system computes actuals from linked transactions.
- **Balance snapshots are additive.** Each new snapshot is recorded, not overwritten.
- **Facts vs. calculations vs. assumptions vs. recommendations.** Every number is explicitly categorized so you know what is yours, what is math, and what is advice.
- **Time-sensitive values are dated.** A balance without a date is not useful.
- **No sensitive numbers.** Account numbers, routing numbers, and credentials are never stored.
- **No bank APIs.** All data comes from the user.
- **History is never destroyed.** New policies/snapshots/reviews replace old ones via references, not overwrites.

## Example interactions

> **You:** "I spent $86 on groceries from checking."
> **OS:** "Got it. I'll log a transaction against your checking account and groceries budget. Anything else about it?"
> **You:** "No."
> **OS:** "Done. Your groceries budget for the month is now 80% used."

> **You:** "How should I pay off my debts?"
> **OS:** "You have three debts. Here's how they compare under different strategies:
> - Avalanche: debt-free in 28 months, $1,840 total interest (lowest cost).
> - Snowball: debt-free in 30 months, $2,120 total interest, but your smallest card is paid off in 4 months.
> - Your credit card has a 0% promo expiring in 6 months — the promo-aware strategy pays that off first to avoid the rate jump.
> Which approach appeals to you?"

> **You:** "Where should my next dollar go?"
> **OS:** "Based on your allocation policy, your $800 monthly surplus goes:
> 1. Emergency fund: $300 (until you reach your $10k target — currently at $6,200).
> 2. Credit card payoff: $250.
> 3. Extra 401k: $150.
> 4. Remaining $100 to discretionary.
> Your emergency fund should hit target in ~13 months (calculation)."

## What gets saved

- **Account** — name, type, institution, balance snapshot history with provenance.
- **Transaction** — amount, direction, account, category, date, notes, budget link.
- **Budget** — period, category, planned amount, derived actual.
- **Income Source** — type, gross/net amount, frequency, deductions, effective date.
- **Expense Profile Item** — category, amount, frequency, type (fixed/variable/discretionary).
- **Debt** — type, balance, rate, minimum payment, promo terms, balance history.
- **Financial Goal** — type, target amount, progress, priority, funding links.
- **Allocation Policy** — priority-ordered tiers with amounts/percentages and goal/debt links.
- **Financial Snapshot** — dated position: accounts, assets, liabilities, net worth, surplus.
- **Financial Review** — periodic assessment with labeled findings and action items.

## Important behaviors

- Never store account numbers, routing numbers, or credentials.
- Never silently edit an existing transaction; use revision.
- Never derive budget actuals from hand-entered totals.
- Never infer user facts; ask rather than assume.
- Never auto-select a debt payoff strategy or allocation priority; present options.
- Always label numbers as fact / calculation / assumption / recommendation.
- Always date time-sensitive values.
- Always surface significant deviations, not just totals.

## Related workflows

- [Monthly financial review](../workflows/finance.md)
- [Comprehensive financial review](../workflows/monthly-financial-review.md)

## Technical implementation

- Workflows: `workflows/finance/`
- Skills: `skills/finance/`
- Calculation guidance: `skills/finance/calculation-guidance.md`
- Calculator: `scripts/finance/finance_calculator.py`
- Tests: `scripts/test-finance-calculator.py`
- Schemas: `schemas/domains/finance/` (account, transaction, budget, financial-snapshot, income-source, expense-profile-item, debt, financial-goal, allocation-policy, financial-review)
