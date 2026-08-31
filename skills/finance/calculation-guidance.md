# Finance Calculation Guidance

## Purpose

Reusable reference for financial calculations used across finance skills and workflows. All formulas produce **calculations**, not facts. Every output must be labeled accordingly and must follow `instructions/policies/mandatory/financial-guidance.md`.

## Epistemological labels

Every number in a finance output must carry one of these labels:

| label | meaning | example |
|-------|---------|---------|
| **fact** | User stated this value directly. | "My rent is $1,800/month." |
| **calculation** | Derived from user-stated facts using a defined formula. | Net worth = total assets - total liabilities. |
| **assumption** | The OS filled in a value the user did not state; must be flagged for verification. | "Assuming 25% effective tax rate." |
| **recommendation** | A suggested action; never auto-applied. | "Consider increasing your emergency fund contribution." |

## Net worth

```
net_worth = total_assets - total_liabilities
total_assets = sum of balances for accounts where balance > 0 and account_type in
               (checking, savings, investment, brokerage, retirement_401k, retirement_ira,
                retirement_roth_ira, hsa, money_market, cd)
total_liabilities = sum of current_balance for all active finance.debt objects
```

## Monthly surplus

```
monthly_surplus = monthly_gross_income - monthly_taxes_and_deductions - monthly_expenses
```

To annualize different frequencies:

| frequency | multiply by |
|-----------|-------------|
| weekly | 52/12 |
| biweekly | 26/12 |
| semimonthly | 2 |
| monthly | 1 |
| quarterly | 1/3 |
| annual | 1/12 |

## Debt payoff — single debt

### Months to payoff (fixed rate, fixed payment)

```
If rate_monthly == 0:
    months = balance / monthly_payment
Else:
    rate_monthly = annual_rate_pct / 100 / 12
    months = -log(1 - (rate_monthly * balance / monthly_payment)) / log(1 + rate_monthly)
```

If `monthly_payment <= rate_monthly * balance`, the debt will never be paid off at that payment level. Flag this.

### Total interest paid

```
total_paid = monthly_payment * months
total_interest = total_paid - balance
```

### Promotional rate modeling

For debts with a promotional rate that expires:

1. Calculate payoff progress during the promo period at the promo rate.
2. If balance remains at promo expiration, switch to the regular rate for remaining calculations.
3. Present both scenarios: (a) paid off during promo, (b) remaining balance at regular rate.

## Debt payoff — multiple debts (strategy comparison)

For each strategy (avalanche, snowball, promo-aware, custom):

1. Set total_monthly_payment = sum of all minimum payments + available surplus.
2. Order debts according to the strategy's priority rule.
3. Simulate month-by-month: apply minimums to all debts, apply surplus to the priority debt.
4. When a debt is paid off, redirect its minimum + surplus to the next priority debt.
5. Track: months to each debt payoff, total interest per debt, total interest overall.

## 401k per-paycheck calculation

```
remaining_room = annual_target - ytd_contributions
per_paycheck_amount = remaining_room / remaining_paychecks
per_paycheck_pct = per_paycheck_amount / gross_pay_per_paycheck * 100
```

### Employer match (example formula: "100% of first X%, 50% of next Y%")

```
employee_contribution_pct = per_paycheck_pct
match_pct = min(employee_contribution_pct, X) * 1.0 + max(0, min(employee_contribution_pct - X, Y)) * 0.5
match_amount_per_paycheck = match_pct / 100 * gross_pay_per_paycheck
annual_match = match_amount_per_paycheck * total_paychecks
```

## Allocation waterfall

```
surplus = monthly_income - monthly_expenses - minimum_debt_payments
for tier in allocation_policy.tiers (sorted by priority):
    if tier.target_type == "fixed_amount":
        allocated = min(tier.amount, surplus)
    elif tier.target_type == "percentage":
        allocated = surplus * tier.amount / 100
    elif tier.target_type == "remainder":
        allocated = surplus
    surplus -= allocated
    record tier.label, allocated
```

## Time-sensitivity

All calculations are valid only as of the date of the input data. Always record:

- The `as_of_date` for balance-dependent calculations.
- The `effective_date` for income/expense-dependent calculations.
- The year for IRS-limit-dependent calculations.

When presenting results, include the date context so the user knows when the calculation was valid.
