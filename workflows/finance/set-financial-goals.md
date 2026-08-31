# Workflow: set-financial-goals

## Purpose

Help the user define, prioritize, and track specific financial goals.

## Steps

1. Ask the user what financial goal they want to set (emergency fund, debt payoff, savings, retirement, large purchase, etc.).
2. Run `skills/finance/capture-financial-goal.md` to create the goal.
3. If the user has multiple goals, help them prioritize (assign `priority` rank).
4. For debt payoff goals, link to the specific `finance.debt` via `related_debt_id`.
5. If an allocation policy exists, suggest updating it to include the new goal. If not, offer to create one.
6. Present the goal summary with target, current progress, and estimated time to achieve (if sufficient data exists).

## Output

- Financial Goal object ID
- Goal summary with target and progress
- Suggested allocation update, if applicable

## Confirmation policy

- Auto-execute: creating a goal from clear details.
- Ask for confirmation: when assigning priority or modifying an allocation policy.
