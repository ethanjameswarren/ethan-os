# Debt Object Prompt

## Purpose

Generate or update a Debt object representing a specific debt obligation.

## Required fields

- `id`: stable ID
- `schema`: `finance.debt`
- `schema_version`: `1`
- `title`: e.g. "Chase Sapphire Credit Card"
- `debt_type`: credit_card | student_loan | auto_loan | mortgage | personal_loan | medical | other
- `current_balance`: most recently reported outstanding balance
- `interest_rate_pct`: current annual interest rate as a percentage
- `minimum_payment`: required minimum monthly payment
- `created_at`
- `provenance`

## Optional fields

- `creditor`
- `account_id`: linked finance.account
- `original_balance`
- `balance_as_of`: date the current_balance was reported
- `interest_type`: fixed | variable
- `currency`
- `promo_rate_pct`, `promo_end_date`, `regular_rate_after_promo_pct`: promotional rate details
- `balance_history`: list of `{ date, balance }`
- `payoff_target_date`
- `status`: active | paid_off | deferred | in_collections
- `notes`
- `links`: typed relationships
- `## Evolution` section

## Instructions

- Record the debt as stated by the user; do not infer interest rates, balances, or payment amounts that were not stated.
- Append to `balance_history` rather than overwriting; each entry is a dated fact.
- Always record `balance_as_of` when updating `current_balance` to preserve temporal provenance.
- Promotional rate fields are important for payoff planning; capture them if stated, including the expiration date and the rate that follows.
- Do not store full account numbers or credentials; reference accounts by their `id`/title.
