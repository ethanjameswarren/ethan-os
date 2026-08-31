# Workflow: capture-income

## Purpose

Capture or update the user's income sources through a conversational flow.

## Steps

1. Ask the user about their income source (type, gross amount, frequency, employer).
2. Run `skills/finance/capture-income-source.md` to create or update the Income Source.
3. If the user mentions pre-tax deductions (401k, HSA, insurance), capture those.
4. If the user mentions post-tax deductions, capture those.
5. Calculate and present the net amount per paycheck if deductions are provided.
6. Ask if there are additional income sources.

## Output

- Income Source object ID(s)
- Summary of gross and net income per pay period and per month

## Confirmation policy

- Auto-execute: creating from clear income details.
- Ask for confirmation: when updating an existing income source's amounts or when deduction details are ambiguous.
