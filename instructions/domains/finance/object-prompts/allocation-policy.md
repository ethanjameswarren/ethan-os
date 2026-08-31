# Allocation Policy Object Prompt

## Purpose

Generate or update an Allocation Policy defining the user's priority hierarchy for surplus cash flow.

## Required fields

- `id`: stable ID
- `schema`: `finance.allocation-policy`
- `schema_version`: `1`
- `title`: e.g. "Cash Flow Allocation — September 2026"
- `effective_date`
- `tiers`: ordered list of allocation tiers
- `created_at`
- `provenance`

## Optional fields

- `supersedes_id`: ID of the policy this one replaces
- `notes`
- `links`: typed relationships
- `## Evolution` section

## Tier structure

Each tier has:

- `priority`: 1 = highest, funded first
- `label`: human-readable name
- `target_type`: `fixed_amount` | `percentage` | `remainder`
- `amount`: dollar amount or percentage depending on `target_type`
- `goal_id`, `debt_id`, `account_id`: optional links to what this tier funds
- `notes`

## Instructions

- The allocation policy reflects the user's stated priorities, not AI recommendations. Ask the user for their preferred order rather than assuming one.
- Higher-priority tiers are fully funded before lower tiers receive dollars.
- Within a tier, items are split by weight if multiple sub-items exist.
- When the user changes their allocation hierarchy, create a new policy with `supersedes_id` pointing to the old one, rather than overwriting the old policy.
- A common default hierarchy (for guidance only, must be confirmed by user):
  1. Minimum debt payments
  2. Essential expenses
  3. Emergency fund (to target)
  4. Employer 401k match
  5. High-interest debt payoff
  6. Additional retirement
  7. Other financial goals
  8. Discretionary spending
- Present this as a starting point; the user's actual priorities may differ.
