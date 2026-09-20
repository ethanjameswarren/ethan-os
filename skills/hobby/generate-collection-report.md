# Skill: generate-collection-report

## Purpose

Render the clean, regeneratable Collection Overview home page for a physical Warhammer army.

## Input

- Canonical `collection/inventory.yaml` records.
- Append-only `rules/points.yaml` records.
- `purchases/plan.yaml`.
- `army-lists/lists.yaml`.
- `painting/scheme-references.yaml`.

## Output

- HTML at `ethan-life/reports/hobby/<project>/reports/collection-overview.html`.
- Dynamic summaries of ownership, current verified points, assembly, painting, energy classes, planned expansion, represented groups, projected collection size, and list readiness.

## Steps

1. Run `python scripts/hobby/generate_collection_overview.py --project <project-path>`.
2. Use only canonical source files; never parse totals back from the generated HTML.
3. Use the newest verified points record for each unit and unit size. Show `Needs verification` when an exact quantity cannot be calculated from verified records.
4. Group owned units using each inventory record's `collection_group`; keep planned purchases separate.
5. Mark an empty list `DRAFT`, a list exceeding owned quantities `MISSING MODELS`, and a fully owned list at its target with complete verified points `READY`.
6. Return the generated path and a concise summary.

## Rules

- The overview is a derived view, never a source of truth.
- Never hard-code quantities, points, progress, purchase state, or list readiness in the page.
- Do not mix planned or ordered models into owned totals.
- Regenerate after collection, points, painting, purchase, or army-list changes.
- This operational page is separate from the annual print lore book.
