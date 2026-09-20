# Workflow: generate-collection-report

## Purpose

Regenerate the Collection Overview home page for the current physical army.

## Trigger

- "Show me my current Necron collection."
- "Generate the collection overview."
- "What do I still need to paint or buy?"

## Inputs

- Project slug, defaulting to `warhammer-40k-necron-dynasty`.

## Outputs

- HTML at `ethan-life/reports/hobby/<project>/reports/collection-overview.html`.
- Summary of owned and planned models, verified points, build/paint progress, represented groups, and army-list readiness.

## Steps

1. Confirm the project if ambiguous.
2. Run `ethan-os/skills/hobby/generate-collection-report.md`.
3. Run `python scripts/hobby/generate_collection_overview.py --project <ethan-life>/domains/hobby/<project>`.
4. Report the output path and any points requiring verification or lists missing models.
