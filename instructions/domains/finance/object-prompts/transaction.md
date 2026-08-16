# Finance Transaction Object Prompt

## Purpose

Generate or update a Transaction object.

## Required fields

- `id`: stable ID
- `schema`: `finance.transaction`
- `schema_version`: `1`
- `title`
- `amount`: positive magnitude
- `date`
- `direction`: expense | income | transfer
- `created_at`
- `provenance`

## Optional fields

- `account_id`
- `currency`
- `category`
- `merchant`
- `budget_id`
- `notes`
- `links`: typed relationships
- `## Evolution` section

## Instructions

- `amount` is always positive; express direction via the `direction` field, never a negative number.
- Reuse an existing `category` string rather than introducing a near-duplicate spelling/variant.
- Link `budget_id` when a Budget exists for this category and period.
- Treat transactions as immutable historical records; corrections go through `workflows/core/revise.md`.
