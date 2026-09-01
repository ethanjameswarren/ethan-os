# Skill: capture-expense-profile

## Purpose

Create or update an Expense Profile Item from user-provided expense information.

## Input

Natural language describing a recurring or expected expense.

## Extract

- Category (Housing, Groceries, Subscriptions, etc.)
- Amount and frequency
- Whether fixed, variable, or discretionary
- Whether essential (need vs. want)
- Effective date, if stated

## Rules

- Record the expense as stated; do not infer amounts the user has not provided.
- Prefer reusing existing category strings from the user's profile over creating near-duplicates.
- If an existing expense-profile-item matches (same category, same payee/description), update it via `## Evolution` rather than creating a duplicate.
- Capture `classification` as `essential`, `committed`, or `discretionary`. Do not infer it when the treatment is materially ambiguous; ask the user. Optionally record fixed/variable behavior separately as `expense_type`.
- `essential` is a user judgment; suggest but always confirm.
- When the user provides an exact last payment and a rounded planned amount, store the rounded planned value in `amount` and record the exact figure and the buffer in `notes` (e.g., "Last payment $2,884; planned at $3,000, ~4% overestimate.").
- When the user gives a precise but non-round figure, offer to round up to a clean number they are comfortable with; if accepted, record the original and rounded values and the buffer percentage in `notes`.
- Do not silently round the user-stated amount unless the user agrees to the rounded value.
- Do not push rounding if the user says the budget is tight, if the rounded amount would exceed available income, or if the expense is large relative to income. In those cases, use the exact amount and explicitly note that no rounding buffer is being applied.
- If rounding an expense would leave significantly less room for other categories, surface the tradeoff and ask whether to use the exact amount instead.
- If the user is capturing multiple related expenses in one session and wants a clean group total, propose per-item roundings that sum to that total. Confirm the per-item and aggregate buffer before applying, and flag any item whose buffer is disproportionately large compared to the others.

## Output

Create or update an Expense Profile Item in `ethan-life/domains/finance/expense-profile/`.

Use schema `finance.expense-profile-item` and version `1`. See `instructions/domains/finance/object-prompts/expense-profile-item.md`.

## Confirmation policy

- Auto-execute: creating from a clear statement of category, amount, and frequency.
- Ask for confirmation: when the essential/committed/discretionary classification is ambiguous, or when updating an existing item's amount.

## Relationship types

- `part_of` — expense linked to a budget
- `related_to` — related expenses in the same category
