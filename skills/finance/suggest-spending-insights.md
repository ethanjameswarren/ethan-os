# Skill: suggest-spending-insights

## Purpose

Surface budget and account items worth Ethan's attention.

## Input

- all Budget objects for the current or a specified period
- all Account objects
- all Transaction objects for the current or specified period

## Identify

- **over-budget categories**: `status: over` budgets, with amount over and largest contributing transactions
- **under-utilized budgets**: `status: under` with the period elapsed, worth reallocating
- **uncategorized or unlinked transactions**: transactions with no `category` or no matching budget
- **stale account snapshots**: accounts whose most recent `balance_snapshots` entry is significantly older than the others
- **goal-linked budgets falling behind**: budgets with `goal_id` set that are `over` or trending that way

## Rules

- Do not change any Budget, Account, or Transaction; only surface findings.
- Rank findings by: over-budget categories tied to a goal first, then other over-budget categories, then stale data, then under-utilized budgets.

## Output

A prioritized list of findings, each with:

- object ID and title
- why it was surfaced
- suggested next step (informational only — not auto-applied)

## Confirmation policy

- Read-only skill: no confirmation required to run. Any resulting change must go through `skills/finance/update-budget.md` or `workflows/core/revise.md`.
