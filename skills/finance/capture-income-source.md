# Skill: capture-income-source

## Purpose

Create or update an Income Source object from user-provided income information.

## Input

Natural language describing a source of income (salary, freelance, rental, etc.).

## Extract

- Income type (salary, hourly, freelance, etc.)
- Source and income type
- Gross amount, if known
- Net amount, if known
- Frequency and expected annual amount
- Variable/bonus component
- Stability: high, medium, or low
- Employer or payer, if mentioned
- Pre-tax deductions (401k, HSA, insurance), if stated
- Post-tax deductions (Roth 401k, etc.), if stated
- Effective date, if stated (default to today for a new income)

## Rules

- Record the income as stated; do not infer amounts, rates, or deductions.
- If an existing income-source matches (same employer/type/frequency), update it via an `## Evolution` entry with a new `effective_date` rather than creating a duplicate.
- `gross_amount` and `net_amount` are optional and are per-frequency-period when present. Preserve an explicitly stated expected annual amount as a fact; otherwise label annualization as calculated.
- Planning may count high-stability recurring net income as reliable. Keep medium/low-stability and variable/bonus income separate unless the user chooses an assumption.
- Do not store sensitive identifiers (SSN, EIN, etc.).
- Ask the user for missing required fields rather than guessing.

## Output

Create or update an Income Source object in `ethan-life/domains/finance/income-sources/`.

Use schema `finance.income-source` and version `1`. See `instructions/domains/finance/object-prompts/income-source.md`.

## Confirmation policy

- Auto-execute: creating from a clear statement of income type, amount, and frequency.
- Ask for confirmation: when updating an existing income source's amount, or when the frequency is ambiguous.

## Relationship types

- `related_to` — related income sources (e.g. primary salary and bonus)
- `part_of` — income tied to a specific financial goal
