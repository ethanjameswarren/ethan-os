# Skill: orchestrate-financial-review

## Purpose

Assemble a comprehensive Financial Review by coordinating snapshot data, budget status, income, expenses, debt trajectory, goal progress, and allocation effectiveness into one structured assessment.

## Input

- Review period (e.g. "2026-08" or "2026-Q3")
- All active finance domain objects

## Steps

1. **Snapshot**: Run `skills/finance/capture-financial-snapshot.md` to ensure a current snapshot exists. If the most recent snapshot is older than 7 days, prompt the user to confirm or update account balances.
2. **Budget review**: Run `skills/finance/update-budget.md` for each active budget in the period to recompute actuals and statuses.
3. **Spending insights**: Run `skills/finance/suggest-spending-insights.md` for the period.
4. **Income assessment**: Compare current income sources to the prior period. Note any changes.
5. **Expense assessment**: Compare current expense profile to actual spending. Identify variances.
6. **Debt trajectory**: For each active debt, compare current balance to the prior snapshot. Determine if payoff is on track.
7. **Goal progress**: For each active financial goal, compare current progress to target. Note if ahead, on track, or behind.
8. **Allocation check**: If an allocation policy exists, determine whether surplus was allocated as planned.
9. **Synthesize findings**: Combine all sections into a prioritized findings list. Each finding must be categorized as `fact`, `calculation`, `assumption`, or `recommendation`.
10. **Generate action items**: Suggest specific follow-up actions based on findings.

## Rules

- Apply `instructions/policies/mandatory/financial-guidance.md` to the review summary and action items.
- Phrase recommendations as possible strategies based on currently available information, explain their reasoning and methodology, and identify facts that could change the conclusion.
- Every finding must be explicitly categorized (fact / calculation / assumption / recommendation).
- All monetary values must include the date they were recorded or calculated.
- Do not modify any underlying financial objects during the review; the review is read-only.
- When comparing to a prior period, reference the specific prior review or snapshot by ID.
- If data is missing (no recent snapshot, no income sources, etc.), note the gap as a finding rather than filling it with assumptions.
- Rank findings by priority: critical issues (negative surplus, missed minimums) first, then goal-related, then informational.

## Output

Create a Financial Review object in `ethan-life/domains/finance/reviews/`.

Use schema `finance.financial-review` and version `1`. See `instructions/domains/finance/object-prompts/financial-review.md`.

Return a human-readable summary to the user with:
- Net worth change
- Income and spending summary
- Debt progress
- Goal progress
- Top 3-5 prioritized action items

## Confirmation policy

- Auto-execute: generating the review summary from existing data.
- Ask for confirmation: before creating the review object if data seems stale or incomplete.

## Relationship types

- `derived_from` — review derived from snapshot and budget objects
- `related_to` — prior review for comparison
