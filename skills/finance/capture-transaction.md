# Skill: capture-transaction

## Purpose

Convert a mentioned purchase, expense, income, or transfer into a Transaction object.

## Input

Natural language describing something Ethan spent, earned, or moved.

## Extract

- amount (as a positive magnitude) and direction: expense, income, or transfer
- date (default to today if not stated and the phrasing implies "just now")
- merchant, if mentioned
- category: infer from merchant/context using existing categories where possible; do not invent a new near-duplicate category if an equivalent one already exists
- account it was made from/to, if mentioned or inferable

## Rules

- `amount` is always a positive number; encode direction separately.
- Do not guess an account if none is mentioned or inferable; leave `account_id` unset rather than guessing wrong.
- If a Budget exists for the resulting category and period, link it via `budget_id`.

## Output

Create a Transaction object in `ethan-life/domains/finance/transactions/`.

Use schema `finance.transaction` and version `1`. See `instructions/domains/finance/object-prompts/transaction.md`.

## Confirmation policy

- Auto-execute: creating a transaction from a clear statement of amount and direction.
- Ask for confirmation: when the category is ambiguous between two plausible existing categories, or when the amount or direction is unclear.

## Relationship types

- `part_of` — transaction → budget
- `related_to` — related transactions (e.g. a refund tied to an earlier purchase)
