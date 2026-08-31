# Workflow: financial-review

## Purpose

Conduct a comprehensive periodic review of the user's financial position, combining all finance domain data into one orchestrated assessment.

## Steps

1. Load the latest accounts, snapshot, income sources, expenses, debts, goals, retirement targets, and active allocation-policy override.
2. Identify stale or missing balances and ask only for updates needed to avoid a materially misleading review.
3. Record a new immutable dated financial snapshot, including explicit coverage gaps.
4. Calculate liquid cash, total assets, total liabilities, and net worth where supported.
5. Normalize reliable recurring income and active expenses to monthly and annual values; keep variable income separate.
6. Estimate available monthly cash flow.
7. Evaluate starter, three-month, and six-month safety-reserve coverage using essential and committed monthly expenses.
8. Evaluate debt payoff progress, minimum-payment coverage, high APR exposure, and promotional expirations.
9. Evaluate retirement contribution pace and employer-match capture when plan data exists.
10. Evaluate every other active financial goal and deadline.
11. Compare the new snapshot with prior snapshots: cash, debt, investments, net worth, safety-net months, essential/committed expense ratio, and savings/investment rate where calculable.
12. Run `skills/finance/allocate-next-dollar.md` to recommend allocation of available cash under the configured or default hierarchy.
13. Produce concrete next actions through the next review date.
14. Save a dated `finance.financial-review` object whose findings are labeled fact, calculation, assumption, or recommendation and cite source object IDs/dates. Recommendations never alter source facts or move money.

## Output

- Financial Review object ID
- Human-readable review summary
- Prioritized action items

## Confirmation policy

- Auto-execute: recording clearly supplied balance updates, the new dated snapshot, calculations, and the review record.
- Ask for confirmation: before changing a user policy or acting on any recommendation.

## Relationship to monthly-budget-review

This workflow supersedes `monthly-budget-review` for comprehensive reviews. The budget-focused review remains available for quick budget-only checks. This workflow adds snapshot, income, expense profile, debt, goal, and allocation analysis.
