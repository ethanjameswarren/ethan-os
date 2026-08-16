# Career Job Target Object Prompt

## Purpose

Generate or update a Job Target object.

## Required fields

- `id`: stable ID
- `schema`: `career.job-target`
- `schema_version`: `1`
- `title`
- `company`
- `role_title`
- `created_at`
- `provenance`

## Optional fields

- `seniority`
- `hiring_intent`: the business problem this role is hired to solve
- `candidate_archetype`
- `responsibilities`: list
- `requirements`: list of `{ text, category, priority, notes }`
- `themes`
- `vocabulary`
- `evaluation_criteria`
- `links`: typed relationships
- `## Evolution` section

## Instructions

- Classify each requirement as critical / important / supporting / incidental based on emphasis in the posting, not keyword frequency alone.
- Distinguish direct requirement statements from reasonable inference.
- Do not assume Ethan has or lacks any requirement; that judgment belongs to the resume/interview-prep workflows.
- Remove or generalize confidential job-posting details (internal team names, unreleased products, recruiter-only notes).
