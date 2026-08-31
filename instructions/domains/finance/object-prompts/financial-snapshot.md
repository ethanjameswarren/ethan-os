# Financial Snapshot Object Prompt

## Purpose

Generate or update a point-in-time Financial Snapshot capturing the user's overall financial position.

## Required fields

- `id`: stable ID
- `schema`: `finance.financial-snapshot`
- `schema_version`: `1`
- `title`: e.g. "Financial Snapshot — 2026-09-01"
- `as_of_date`: the date this snapshot represents
- `created_at`
- `provenance`

## Optional fields

- `accounts_summary`: list of `{ account_id, balance, balance_source }`
- `total_assets`
- `total_liabilities`
- `net_worth` and `net_worth_type`
- `monthly_income_total`
- `monthly_expense_total`
- `monthly_surplus`
- `notes`
- `links`: typed relationships
- `## Evolution` section

## Instructions

- Each snapshot is immutable; create a new snapshot rather than editing an old one.
- Mark each calculated field explicitly as `calculated` vs `user_stated` where the schema provides a type distinction.
- `total_assets`, `total_liabilities`, `net_worth`, and `monthly_surplus` are calculated from component data; label them as calculations, not user facts.
- Do not infer account balances the user has not stated; leave `accounts_summary` incomplete rather than guessing.
- Reference accounts by `account_id`, never by sensitive identifiers.
