# Skill: capture-debt

## Purpose

Create or update a Debt object from user-provided debt information.

## Input

Natural language describing a debt obligation (credit card, loan, mortgage, etc.).

## Extract

- Debt type
- Creditor/lender
- Current balance and date
- Interest rate (APR)
- Minimum monthly payment
- Promotional rate details, if stated (promo APR, expiration, regular rate after)
- Original balance, if stated

## Rules

- Record the debt as stated; do not infer interest rates, balances, or minimum payments.
- If an existing debt matches (same creditor and type), update it rather than creating a duplicate; append to `balance_history` and update `current_balance` / `balance_as_of`.
- Promotional rate details are critical for payoff planning; always capture `promo_end_date` and `regular_rate_after_promo_pct` when a promotional rate is mentioned.
- Do not store full account numbers or credentials.
- Ask for missing required fields rather than guessing.

## Output

Create or update a Debt object in `ethan-life/domains/finance/debts/`.

Use schema `finance.debt` and version `1`. See `instructions/domains/finance/object-prompts/debt.md`.

## Confirmation policy

- Auto-execute: creating from a clear statement of debt type, balance, rate, and minimum payment.
- Ask for confirmation: when updating an existing debt's balance or rate, or when the debt type is ambiguous.

## Relationship types

- `related_to` — related debt (e.g. refinanced loan replacing an older one)
- `part_of` — debt linked to a financial goal (payoff)
