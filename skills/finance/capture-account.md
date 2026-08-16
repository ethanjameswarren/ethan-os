# Skill: capture-account

## Purpose

Register a new financial account or record a balance snapshot for an existing one.

## Input

Natural language mentioning an account and, optionally, a current balance.

## Extract

- institution name, if mentioned
- account type: checking, savings, credit_card, investment, loan, other
- currency, if not USD or otherwise implied
- current balance and date, if stated

## Rules

- If the account already exists, append a new `balance_snapshots` entry rather than creating a duplicate account or overwriting history.
- Do not store full account numbers, routing numbers, or credentials.
- Do not infer a balance that was not stated.

## Output

Create or update an Account object in `ethan-life/domains/finance/accounts/`.

Use schema `finance.account` and version `1`. See `instructions/domains/finance/object-prompts/account.md`.

## Confirmation policy

- Auto-execute: creating a new account or appending a balance snapshot from a clear statement.
- Ask for confirmation: when it is unclear whether this refers to an existing account or a new one, or before marking an account `closed`.

## Relationship types

- `related_to` — related accounts (e.g. a credit card linked to a checking account for autopay)
