# Career Interview Prep Object Prompt

## Purpose

Generate or update a Career Interview Prep object.

## Required fields

- `id`: stable ID
- `schema`: `career.interview-prep`
- `schema_version`: `1`
- `title`
- `target_id`: ID of the related `career.job-target`
- `status`: draft | validated | confirmed
- `created_at`
- `provenance`

## Optional fields

- `stories`: list of `{ category, framework, situation, task, obstacle, action, result, lessons_learned, evidence_ids, target_requirements, confidence }`
- `gaps`: story categories with no strong evidence
- `tailoring_notes`
- `links`: typed relationships
- `## Evolution` section

## Instructions

- Every story must carry `evidence_ids` tracing it back to Career Evidence.
- Choose the framework (STAR / CAR / SOAR) that best fits the evidence; do not force every story into STAR.
- If a category has no strong evidence, record it under `gaps` rather than inventing a story.
- Generalize confidential specifics (proprietary code, internal dataset names, credentials) while keeping stories truthful.
