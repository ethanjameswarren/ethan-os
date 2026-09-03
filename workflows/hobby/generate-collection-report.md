# Workflow: generate-collection-report

## Purpose

Regenerate the digital collection report for the current hobby project.

## Trigger

- "Show me my current Necron collection."
- "Generate the collection report."
- "What do I still need to buy?"

## Inputs

- Project slug (defaults to `warhammer-40k-necron-dynasty`).

## Outputs

- HTML file at `ethan-life/reports/hobby/<project>/reports/collection-report.html`.
- Summary of owned, planned, and acquired items, plus build/paint/magnetization progress.

## Steps

1. Confirm the project if ambiguous.
2. Run `ethan-os/skills/hobby/generate-collection-report.md`.
3. Run `scripts/hobby/generate_digital_report.py collection --project <project> --life-dir <ethan-life>`.
4. Report the output path and a brief summary.
