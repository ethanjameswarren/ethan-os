# Workflow: generate-financial-report

## Purpose

Fulfill requests to generate, update, or view the user's personal financial report packet.

## Triggers

- "Generate my financial report."
- "Make my monthly financial review."
- "Update my financial packet."
- "Show me how my finances have changed."
- "Generate a projection based on my current plan."

## Steps

1. Confirm the intent is to generate an HTML report artifact (as opposed to a textual answer or a `finance.financial-review` object).
2. Run `skills/finance/generate-financial-report.md`.
3. Run `scripts/finance/generate_report.py --life-dir <ethan-life>`.
4. Report the generated file path and a concise summary of the headline metrics.

## Output

- Path to `ethan-life/reports/finance/financial-report-YYYY-MM-DD.html`.
- One- or two-line summary of the major findings: net worth, liquid cash, available monthly cash flow, and the top next-dollar recommendation.

## Confirmation policy

- Auto-execute: when the user clearly asks for a report, packet, or projection.
- Ask for confirmation: if the request is ambiguous between a generated HTML report, a conversational summary, or a saved `finance.financial-review` object.
