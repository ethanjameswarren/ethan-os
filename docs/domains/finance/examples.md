# Finance Domain Examples

## Log a transaction

> spent $64 at trader joes today, groceries as usual

- Transaction: amount 64, direction expense, category "Groceries", merchant "Trader Joe's", date today
- If a Budget "Groceries — 2026-08" exists, `update-budget` recomputes `amount_actual` to include this transaction and re-evaluates `status`.

## Budget review

> how am i doing on groceries this month

`monthly-budget-review` recomputes the "Groceries — 2026-08" budget, finds `amount_actual` has exceeded `amount_planned`, and reports:

- Groceries is `over` by $42 this month, driven largely by two Trader Joe's visits and one Costco run.

## Account snapshot

> checking account is at $2,340 as of today

`capture-account` appends a new entry to `balance_snapshots` for the existing Checking account (source: user_stated) rather than creating a duplicate account.

## Capture income

> I make $85,000 salary, paid biweekly. I put 6% into my 401k pre-tax.

- Income Source: income_type salary, gross_amount $3,269.23/paycheck, frequency biweekly, effective_date today.
- Pre-tax deduction: 401k, $196.15/paycheck (6% of gross).

## Capture expense profile

> my rent is $1,800/month and car insurance is $140/month

- Expense Profile Item: "Rent", $1,800, monthly, fixed, essential.
- Expense Profile Item: "Car Insurance", $140, monthly, fixed, essential.

## Capture debt

> I owe $4,500 on my Chase Sapphire at 21.99%, minimum payment $90. I also have a 0% promo on my Citi card, $3,000 balance, expires in March.

- Debt: "Chase Sapphire", credit_card, $4,500, 21.99% APR, $90 minimum.
- Debt: "Citi Card", credit_card, $3,000, promo_rate 0%, promo_end_date 2027-03, regular_rate TBD (ask user).

## Set financial goal

> I want a $10,000 emergency fund by end of year. I can save $500/month toward it.

- Financial Goal: emergency_fund, target $10,000, monthly_contribution $500, target_date 2026-12-31.

## Debt payoff planning

> how should I pay off my debts?

`plan-debt-payoff` loads both debts and presents:

| Strategy | Order | Months to free | Total interest | Savings vs worst |
|----------|-------|----------------|---------------|-----------------|
| Avalanche | Chase Sapphire → Citi | 18 months | $1,240 | — |
| Snowball | Citi → Chase Sapphire | 19 months | $1,380 | -$140 |
| Promo-aware | Citi (before March) → Chase Sapphire | 18 months | $1,190 | +$50 |

"The promo-aware strategy pays off your Citi card before the 0% rate expires in March, avoiding the rate jump. It saves $50 in interest vs avalanche. **Recommendation**: consider the promo-aware approach given the March deadline."

## Cash flow allocation

> where should my next dollar go?

`allocate-next-dollar` applies the user's allocation policy:

1. Emergency fund: $500 (until $10k target reached)
2. Credit card payoff: $300
3. Extra 401k: $200
4. Remaining: $150 to discretionary

## 401k per-paycheck

> am I on track to max my 401k this year?

`compute-401k-target`: Annual target $23,500. YTD $10,000. 18 paychecks remaining. Need $750/paycheck (18.75% of gross). Current contribution: $196.15 (6%). **Calculation**: need to increase to 18.75% to max out. **Recommendation**: consider increasing gradually or choosing a target below the max.

## Financial review

> let's do my financial review for August

`financial-review` orchestrates a comprehensive assessment:

- **Net worth**: $32,400 (calculation), up $1,200 from July (comparison to prior snapshot).
- **Income**: $7,000/month gross (fact). No changes.
- **Spending**: $5,200 actual vs $5,000 budgeted. Groceries over by $42.
- **Debt**: $7,500 total, down $400 from July. On track.
- **Goals**: Emergency fund at $6,200 of $10,000 target. On track for December.
- **Allocation**: $800 surplus allocated as planned.
- **Action items**: (1) Review groceries spending. (2) Confirm Citi promo end date.
