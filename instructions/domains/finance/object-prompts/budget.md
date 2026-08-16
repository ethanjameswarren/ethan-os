# Finance Budget Object Prompt

## Purpose

Generate or update a Budget object.

## Required fields

- `id`: stable ID
- `schema`: `finance.budget`
- `schema_version`: `1`
- `title`
- `category`
- `period`: e.g. `2026-08` for a monthly budget
- `amount_planned`
- `created_at`
- `provenance`

## Optional fields

- `amount_actual`: recomputed from linked transactions, not hand-maintained
- `currency`
- `status`: on_track | over | under | unknown
- `goal_id`: related `planning.goal`, if any
- `links`: typed relationships
- `## Evolution` section

## Instructions

- Do not hand-edit `amount_actual` or `status`; both are recomputed by `skills/finance/update-budget.md` or the monthly review workflow from linked Transactions.
- One Budget per category per period; update the existing one rather than creating a duplicate for the same category/period.
