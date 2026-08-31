# Workflow: capture-expense-profile

## Purpose

Build or update the user's recurring expense profile through a conversational flow, walking through major spending categories.

## Steps

1. If no expense profile exists yet, offer to walk through common categories: Housing, Utilities, Insurance, Transportation, Groceries, Subscriptions, Debt payments (captured separately as debts), and Discretionary.
2. For each expense the user mentions, run `skills/finance/capture-expense-profile.md`.
3. Classify each as fixed, variable, or discretionary; confirm with the user if ambiguous.
4. After all items are captured, present a summary: total monthly fixed, variable, discretionary, and overall.
5. Compare total expenses to known income and show the implied surplus.

## Output

- Expense Profile Item object IDs
- Monthly expense summary by type
- Implied monthly surplus, if income is known

## Confirmation policy

- Auto-execute: creating expense items from clear details.
- Ask for confirmation: when classifying expense type or essential/non-essential status.
