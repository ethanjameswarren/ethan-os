# Workflow: generate-battle-chronicle

## Purpose

Regenerate the digital battle chronicle for the current hobby project.

## Trigger

- "Show me my Necron battle history."
- "Generate the battle chronicle."
- "What battles have I played?"

## Inputs

- Project slug (defaults to `warhammer-40k-necron-dynasty`).

## Outputs

- HTML file at `ethan-life/reports/hobby/<project>/reports/battles-report.html`.
- Chronological list of battles with outcomes and lore-candidate status.

## Steps

1. Confirm the project if ambiguous.
2. Run `ethan-os/skills/hobby/generate-battle-chronicle.md`.
3. Run `scripts/hobby/generate_digital_report.py battles --project <project> --life-dir <ethan-life>`.
4. Report the output path and a brief summary.
