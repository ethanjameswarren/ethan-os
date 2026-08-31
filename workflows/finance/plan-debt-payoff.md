# Workflow: plan-debt-payoff

## Purpose

Help the user understand their debt payoff options by comparing strategies (avalanche, snowball, promo-aware, custom) with explicit tradeoffs and estimated outcomes.

## Steps

1. Load all active `finance.debt` objects.
2. Ask the user how much they can put toward debt payments each month beyond minimums. If not stated, calculate from allocation policy or income/expense data.
3. Run `skills/finance/plan-debt-payoff.md` to compute payoff timelines and costs for each strategy.
4. Present a comparison table:
   - Strategy name
   - Order of payoff
   - Months to debt-free
   - Total interest paid
   - Interest savings vs. worst strategy
5. Highlight tradeoffs for each strategy (see skill for details).
6. If any debt has a promotional rate expiring, flag it prominently and show the impact of paying it off before vs. after the promo expires.
7. Ask the user which strategy they prefer.
8. If they choose, offer to update their allocation policy and create a debt payoff financial goal.

## Output

- Strategy comparison table
- Per-debt payoff timeline for chosen strategy
- Action items (update allocation policy, set financial goal)

## Confirmation policy

- Auto-execute: computing and presenting strategy comparisons.
- Ask for confirmation: before updating allocation policy or creating financial goals.
