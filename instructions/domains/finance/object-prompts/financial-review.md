# Financial Review Object Prompt

## Purpose

Generate a Financial Review object summarizing a periodic assessment of the user's financial position.

## Required fields

- `id`: stable ID
- `schema`: `finance.financial-review`
- `schema_version`: `1`
- `title`: e.g. "Financial Review — August 2026"
- `review_date`: date the review was conducted
- `review_period`: e.g. "2026-08"
- `created_at`
- `provenance`

## Optional fields

- `review_type`: monthly | quarterly | annual | ad_hoc
- `snapshot_id`: linked financial snapshot
- `sections`: structured review sections (net_worth, income, spending, debt, goals, allocation)
- `findings`: prioritized list of observations
- `action_items`: suggested follow-ups
- `notes`
- `links`: typed relationships

## Instructions

- Each finding must be explicitly categorized as `fact`, `calculation`, `assumption`, or `recommendation`.
  - `fact` = something the user stated.
  - `calculation` = a number derived from user-stated facts using defined formulas.
  - `assumption` = something the OS assumed that the user should verify.
  - `recommendation` = a suggested action; never auto-applied.
- All monetary values in the review must be dated; never present a value without indicating when it was recorded or calculated.
- Findings are ranked by priority: high → medium → low.
- The review is a read-only summary; it does not modify any underlying financial objects.
- When comparing to a prior period, cite the specific prior review or snapshot by ID.
- Never infer user facts; if data is missing, note the gap as a finding rather than filling it with assumptions.
