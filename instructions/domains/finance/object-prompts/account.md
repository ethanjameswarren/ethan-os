# Finance Account Object Prompt

## Purpose

Generate or update an Account object.

## Required fields

- `id`: stable ID
- `schema`: `finance.account`
- `schema_version`: `1`
- `title`
- `account_type`: checking | savings | credit_card | investment | loan | other
- `created_at`
- `provenance`

## Optional fields

- `institution`
- `status`: active | closed
- `currency`
- `balance_snapshots`: list of `{ date, balance }`
- `links`: typed relationships
- `## Evolution` section

## Instructions

- Append a new entry to `balance_snapshots` for each reported balance; never overwrite prior snapshots.
- Do not store full account numbers, routing numbers, or credentials in this object.
- Prefer updating an existing account over creating a duplicate for the same institution/account.
