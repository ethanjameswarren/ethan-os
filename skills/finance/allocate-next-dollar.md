# Skill: allocate-next-dollar

## Purpose

Apply the user's allocation policy to determine where their next available dollar(s) should go, using a configurable priority hierarchy.

## Input

- The user's active `finance.allocation-policy`
- Current `finance.financial-snapshot` or account balances
- Active `finance.financial-goal` objects with current progress
- Active `finance.debt` objects with current balances
- Monthly surplus (from snapshot or income minus expenses)

## Steps

1. Load the active allocation policy and its tier list.
2. Determine the monthly surplus available for allocation.
3. Walk the tiers in priority order:
   a. For each tier, determine if its target is met (goal reached, debt paid off, fixed amount allocated).
   b. If the tier's target is not yet met, allocate dollars to it.
   c. When a tier is fully funded, move to the next.
4. For `remainder` tiers, allocate everything left after higher-priority tiers.
5. Present the allocation breakdown clearly.

## Rules

- Apply `instructions/policies/mandatory/financial-guidance.md`.
- Frame the result as one reasonable approach based on currently available information. Explain why the first unfunded tier appears higher priority and identify the policy, stale inputs, assumptions, and tradeoffs that drive the result.
- The allocation policy is a user-stated preference; do not override the user's tier ordering.
- If no Ethan-specific allocation policy exists, apply the OS default hierarchy: required obligations → minimum debt payments → starter safety reserve → employer retirement match → urgent/high-interest debt → larger safety reserve → annual retirement target → taxable investments → other goals → discretionary allocation. Clearly label it as the default policy and offer configuration without blocking the recommendation.
- All numbers are calculations derived from user-stated data; label them as such.
- If surplus is negative (expenses exceed income), flag this as a critical finding and do not attempt to allocate.
- If a goal has been reached or a debt paid off, note that its tier is complete and dollars flow to the next tier.
- Never auto-move money or create transactions; this skill is advisory.

## Output

A clear allocation breakdown showing:

- Monthly surplus available
- Per-tier: how much is allocated, what it funds, whether the target is met
- Any tiers that received $0 because higher tiers consumed all surplus
- Flags for any issues (negative surplus, stale data, unfunded priorities)

## Confirmation policy

- Read-only analysis: no confirmation needed.
- Confirmation required: if the user wants to update their allocation policy based on findings.
