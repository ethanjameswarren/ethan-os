# Workflow: generate-rules-reference

## Purpose

Regenerate the digital tabletop rules/points reference for the current hobby project.

## Trigger

- "Show me the current Necron rules reference."
- "Generate the rules report."

## Inputs

- Project slug (defaults to `warhammer-40k-necron-dynasty`).
- Optional current edition/points data if not yet stored.

## Outputs

- HTML file at `ethan-life/reports/hobby/<project>/reports/rules-report.html`.
- Snapshot of current rules, points, stats, and abilities.

## Steps

1. Confirm the project if ambiguous.
2. Run `ethan-os/skills/hobby/generate-rules-reference.md`.
3. Run `scripts/hobby/generate_digital_report.py rules --project <project> --life-dir <ethan-life>`.
4. If no rules data is stored, note what needs to be captured.
5. Report the output path.
