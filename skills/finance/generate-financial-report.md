# Skill: generate-financial-report

## Purpose

Generate a standalone, human-readable HTML financial report from the user's canonical `ethan-life` finance data.

## Input

Natural language request such as "Generate my financial report", "Make my monthly financial review", "Update my financial packet", "Show me how my finances have changed", or a command to generate a projection based on the current plan.

## Steps

1. Confirm the `ethan-life` repository path from `.ethan-os.yaml` or the environment.
2. Load finance objects from `ethan-life/domains/finance/accounts/`, `income-sources/`, `expenses/`, `debts/`, `goals/`, `snapshots/`, and `policies/`.
3. Run `scripts/finance/generate_report.py` with `--life-dir <ethan-life>`.
4. Save the HTML artifact to `ethan-life/reports/finance/financial-report-YYYY-MM-DD.html`.
5. Return the file path and a short summary of the headline metrics.

## Output

- The HTML report file path.
- A brief summary of: net worth, liquid cash, monthly income, monthly expenses, monthly debt payments, and available cash flow.
- The report itself is the primary artifact; it is not stored as a `finance.financial-review` object unless the user also asks for a review to be saved.

## Rules

- Do not expose account numbers, routing numbers, or credentials in the report.
- Distinguish user-entered facts, calculations, assumptions, and recommendations in the report text.
- If `ethan-life` has no finance data, generate an empty report that says so and lists what is missing.
- Projections are planning scenarios, not predictions. Label them as assumptions.
- Do not invent financial priorities not stored in `ethan-life`.

## Confirmation policy

- Auto-execute: generating a report from existing `ethan-life` data.
- Ask for confirmation: if the report would overwrite an HTML file generated on the same day, or if the user has not yet captured any finance data.

## Relationship types

- `generated_from` — report derived from `finance.financial-snapshot`, `finance.account`, `finance.income-source`, `finance.expense-profile-item`, `finance.debt`, `finance.financial-goal`, and `finance.allocation-policy` objects.
