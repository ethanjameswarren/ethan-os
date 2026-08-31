# Financial Goal Object Prompt

## Purpose

Generate or update a Financial Goal representing a specific monetary objective.

## Required fields

- `id`: stable ID
- `schema`: `finance.financial-goal`
- `schema_version`: `1`
- `title`: e.g. "Emergency Fund — 6 Months"
- `goal_type`: starter_safety_reserve | three_month_safety_reserve | six_month_safety_reserve | debt_payoff | annual_401k_contribution | taxable_investment | major_purchase_savings | custom
- `target_amount`: dollar amount to reach
- `status`: active | achieved | abandoned | on_hold
- `created_at`
- `provenance`

## Optional fields

- `current_amount` and `current_amount_as_of`: latest progress
- `currency`
- `target_date`
- `monthly_contribution`: planned monthly amount
- `funding_account_id`
- `related_debt_id`: linked debt for payoff goals
- `planning_goal_id`: linked planning.goal
- `priority`: user-assigned rank (1 = highest)
- `progress_history`: list of `{ date, amount }`
- `completion_criteria`
- `dependencies`
- `target_basis`: user_stated | calculated
- `why_it_matters`
- `notes`
- `links`: typed relationships
- `## Evolution` section

## Instructions

- Record the goal as stated by the user; do not infer target amounts or dates. For safety-reserve goals, calculate the target from essential and committed monthly expenses when coverage is sufficient, set `target_basis: calculated`, and identify the source expense records.
- Append to `progress_history` rather than overwriting; each entry is a dated fact.
- `current_amount` is the latest snapshot of progress; always record `current_amount_as_of` when updating it.
- For debt payoff goals, link to the specific `finance.debt` via `related_debt_id`.
- `priority` is user-stated; the OS may suggest a priority but never assigns one silently.
- `monthly_contribution` is a plan, not a fact; distinguish it from actual contributions tracked in transactions.
