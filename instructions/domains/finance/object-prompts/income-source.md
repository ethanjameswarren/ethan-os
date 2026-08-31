# Income Source Object Prompt

## Purpose

Generate or update an Income Source object representing a recurring or one-time source of income.

## Required fields

- `id`: stable ID
- `schema`: `finance.income-source`
- `schema_version`: `1`
- `title`: e.g. "Primary Salary — Acme Corp"
- `income_type`: salary | hourly | freelance | rental | investment | side_business | bonus | other
- `gross_amount`: gross amount per frequency period
- `frequency`: weekly | biweekly | semimonthly | monthly | quarterly | annual | one_time
- `effective_date`: when this income level became effective
- `created_at`
- `provenance`

## Optional fields

- `employer`
- `net_amount`: after-tax/deduction amount if known
- `currency`
- `end_date`
- `pre_tax_deductions`: list of `{ label, amount, per_paycheck }`
- `post_tax_deductions`: list of `{ label, amount, per_paycheck }`
- `account_id`: deposit account
- `status`: active | ended | expected
- `notes`
- `links`: typed relationships
- `## Evolution` section

## Instructions

- Record the income as stated by the user; do not infer amounts, frequencies, or deductions that were not stated.
- When income changes (raise, job change), create a new income-source or add an `## Evolution` entry with the new effective_date rather than silently overwriting the old amount.
- `gross_amount` and `net_amount` are per-frequency-period values (e.g. per paycheck for biweekly).
- Pre-tax deductions (401k, HSA, health insurance) reduce gross to net; capture them if the user provides them, but do not guess.
- Do not store Social Security numbers, bank routing numbers, or other sensitive identifiers.
