# Career Resume Content Object Prompt

## Purpose

Generate or update a Career Resume Content object.

## Required fields

- `id`: stable ID
- `schema`: `career.resume`
- `schema_version`: `1`
- `title`
- `target_id`: ID of the `career.job-target` this resume is built for
- `created_at`
- `provenance`

## Optional fields

- `status`: draft | validated | confirmed
- `narrative`: selected resume strategy/persona
- `summary`, `skills`
- `experience`: list of `{ employer, role, timeframe, bullets, evidence_ids }`
- `projects`: list of `{ name, bullets, evidence_ids }`
- `education`
- `match_analysis`: `{ strongest_matches, transferable_matches, genuine_gaps, evidence_used, evidence_omitted, rationale }`
- `confirmation_needed`: claims requiring Ethan's confirmation
- `links`: typed relationships
- `## Evolution` section

## Instructions

- Every bullet must carry `evidence_ids` tracing it back to Career Evidence.
- Do not alter employer, title, dates, or education facts here; corrections belong in the underlying Career Evidence via the `revise` workflow.
- Do not distort `match_analysis` to hide genuine gaps.
- Keep canonical content separate from LaTeX presentation (see `workflows/career/build-tailored-resume.md` step 12).
