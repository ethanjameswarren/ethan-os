# Workflow: compute-401k-target

## Purpose

Help the user determine the right per-paycheck 401k contribution to hit their annual target.

## Steps

1. Load the user's primary `finance.income-source` to get gross pay and pay frequency.
2. Ask for: annual contribution target, year-to-date contributions, and employer match formula (if not already captured).
3. Run `skills/finance/compute-401k-target.md` to calculate per-paycheck amount and percentage.
4. Present results with all assumptions labeled.
5. If the user wants to update their income source pre-tax deductions, run `skills/finance/capture-income-source.md`.

## Output

- Per-paycheck contribution amount and percentage
- Employer match amount (if formula known)
- Total annual contribution (employee + employer)

## Confirmation policy

- Auto-execute: calculating from stated data.
- Ask for confirmation: before updating income source deductions.
