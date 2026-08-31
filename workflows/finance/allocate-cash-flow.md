# Workflow: allocate-cash-flow

## Purpose

Help the user define or apply their cash flow allocation policy — a priority-ordered hierarchy for where each next dollar goes.

## Steps

1. If no `finance.allocation-policy` exists:
   a. Present the common default hierarchy as a starting point (see `instructions/domains/finance/object-prompts/allocation-policy.md`).
   b. Walk the user through customizing it: confirm or reorder tiers, set amounts/percentages, link to goals and debts.
   c. Create the allocation policy.
2. If an allocation policy exists:
   a. Run `skills/finance/allocate-next-dollar.md` with current financial data.
   b. Present the allocation breakdown: how much goes where, which tiers are funded, which are not.
   c. Flag issues: negative surplus, stale data, fully funded goals.
3. If the user wants to change their allocation:
   a. Walk through modifications.
   b. Create a new policy with `supersedes_id` pointing to the old one.

## Output

- Allocation policy object ID
- Per-tier allocation breakdown
- Monthly surplus and how it is distributed
- Flags for issues

## Confirmation policy

- Auto-execute: computing allocation breakdown from existing policy.
- Ask for confirmation: before creating or replacing an allocation policy.
