# Career Evidence Object Prompt

## Purpose

Generate or update a Career Evidence object.

## Required fields

- `id`: stable ID
- `schema`: `career.evidence`
- `schema_version`: `1`
- `title`
- `status`: draft | verified | generalized
- `created_at`
- `provenance`: `capture_id`, `source_id`, `agent_version`, `provenance_note`

## Optional fields

- `employer`, `role`, `project`, `timeframe`
- `facts`: confirmed facts
- `inferences`: reasonable inferences, clearly marked
- `unknowns`: open questions
- `evidence_summary`
- `skills`, `technologies`
- `outcomes`: confirmed or estimated, with confidence
- `interview_stories`
- `resume_candidates`: derivative, not canonical
- `links`: typed relationships
- `## Evolution` section

## Instructions

- Never turn an inference into a confirmed accomplishment.
- Never invent metrics, ownership, scope, technologies, business impact, leadership, or outcomes.
- Prefer updating an existing evidence record over creating duplicates for the same role/project.
- Strip confidential implementation details before saving (see `instructions/domains/career/instructions.md`).
