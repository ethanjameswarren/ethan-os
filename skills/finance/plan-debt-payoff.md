# Skill: plan-debt-payoff

## Purpose

Analyze the user's debts and present payoff strategies with tradeoffs, estimated payoff dates, and total interest cost comparisons.

## Input

- All active `finance.debt` objects
- Total monthly amount available for debt payments (user-stated or from allocation policy)
- User preference for strategy, if any

## Strategies

Present the following strategies with explicit tradeoffs. Never auto-select a strategy; present all applicable options and let the user choose.

### Avalanche (lowest total interest)

- Order debts by interest rate, highest first.
- Pay minimums on all debts; apply surplus to the highest-rate debt.
- **Tradeoff**: mathematically optimal for total interest cost; first payoff may take longer, which can reduce motivation.

### Snowball (fastest first win)

- Order debts by balance, smallest first.
- Pay minimums on all debts; apply surplus to the smallest balance.
- **Tradeoff**: may cost more in total interest, but the early wins can sustain motivation.

### Promo-aware (deadline-driven)

- Prioritize debts with expiring promotional rates, ordering by promo end date.
- Pay off the promo-rate balance before the promo expires to avoid the rate jump.
- After promo debts are handled, fall back to avalanche ordering.
- **Tradeoff**: prevents rate-jump surprises; may not be globally optimal if promo balances are small relative to high-rate debts.

### Custom

- The user defines their own payoff order and monthly allocation.
- The OS calculates payoff dates and interest costs for the user's chosen order.

## Calculation guidance

For each strategy, compute and present:

1. **Payoff timeline** — estimated month/year each debt reaches $0.
2. **Total interest paid** — across all debts from today to full payoff.
3. **Monthly payment schedule** — how much goes to each debt each month.
4. **Comparison** — show the interest-cost difference between the user's chosen strategy and the avalanche strategy.

Use the formulas in `skills/finance/calculation-guidance.md` or `scripts/finance/finance_calculator.py` for amortization and payoff math.

## Rules

- Apply `instructions/policies/mandatory/financial-guidance.md`.
- Introduce conclusions with qualified language such as "Under the selected debt-payoff methodology..." and explain that avalanche, snowball, promotional-expiration-aware, and custom approaches optimize different concerns.
- All outputs are calculations or recommendations, never facts. Label them explicitly.
- Use the user's stated balances, rates, and minimums; do not look up or estimate rates.
- If a debt has a promotional rate, model the rate change at `promo_end_date` in the payoff projection.
- If the user's available payment amount is not enough to cover all minimums, flag this clearly as a critical finding.
- Present the interest-cost difference between strategies so the user can make an informed choice.
- Never auto-apply a strategy; present options and wait for the user's decision.

## Output

A structured payoff plan comparison presented to the user, including:

- Per-strategy: ordered debt list, monthly allocation, estimated payoff dates, total interest
- Strategy comparison table
- Recommendation (labeled as `recommendation`, not `fact`)

The user's chosen strategy can then be captured as allocations in their `finance.allocation-policy`.

## Confirmation policy

- Read-only analysis: no confirmation required to compute and present strategies.
- Confirmation required: before updating allocation policy or financial goals based on the chosen strategy.
