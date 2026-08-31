# Expense Profile Item Object Prompt

## Purpose

Generate or update an Expense Profile Item representing a recurring or expected expense.

## Required fields

- `id`: stable ID
- `schema`: `finance.expense-profile-item`
- `schema_version`: `1`
- `title`: expense name, e.g. "Rent — Main St Apartment"
- `category`: spending category
- `amount`: expected amount per frequency period
- `frequency`: weekly | biweekly | semimonthly | monthly | quarterly | annual | one_time | irregular
- `classification`: essential | committed | discretionary
- `effective_date`
- `created_at`
- `provenance`

## Optional fields

- `due_date`: recurring due day or full date at the precision stated
- `monthly_equivalent` and `annual_equivalent`: labeled calculated values
- `expense_type`: fixed | variable | discretionary behavior, separate from planning classification
- `currency`, `end_date`, `account_id`, `budget_id`, `status`, `notes`, `links`
- `## Evolution` section

## Instructions

- Record the expense as stated; do not infer missing amounts, dates, or classifications.
- Prefer existing category strings over near-duplicates.
- Use essential and committed monthly expenses when calculating safety-reserve targets.
- When an expense changes, preserve the prior dated fact in `## Evolution` and add the new effective value rather than silently replacing history.
- One Expense Profile Item represents one distinct expense.
