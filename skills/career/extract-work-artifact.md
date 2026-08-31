# Skill: extract-work-artifact

## Purpose

Convert a raw description of a professional project, initiative, or piece of work into a structured `career.work_artifact` object.

This skill captures evidence. It does not generate resume bullets or tailor language for a specific job.

## Inputs

Accept any combination of:

- User-described work
- Project summary or closeout
- Repository context
- Existing Ethan OS / Ethan Life context
- Uploaded document
- Work notes
- Analysis results
- Existing work artifacts

## Context resolution

Before extracting, resolve where possible:

- Employer / organization
- Role title
- Team / domain
- Project or initiative name
- Approximate timeframe
- Existing related work artifacts
- Existing role context
- Existing capability records

Use existing context from `ethan-life/domains/career/` before asking the user. Only ask for missing information when it cannot be reasonably inferred.

## Extract

Where supported by the input, capture:

- Context — business or operational situation
- Problem — what was slow, broken, ambiguous, or costly
- User's role — ownership, contribution, leadership, or support
- Actions — what the user personally did
- Architecture / methodology — approach, design, or analytical framework
- Technologies — tools, languages, platforms, ERPs, cloud services
- Scope — scale, teams affected, systems touched, time span
- Results — measurable or observable outcomes
- Business impact — decisions enabled, costs reduced, time saved, risks mitigated
- Decisions enabled — what stakeholders could do because of the work
- Reusable outputs — frameworks, libraries, dashboards, pipelines, documentation
- Evidence signals — skills and capabilities demonstrated

## Rules

- Clearly distinguish confirmed fact from reasonable inference and unknown.
- Never turn an inference into a confirmed accomplishment.
- Never invent metrics, ownership, scope, technologies, business impact, leadership, or outcomes.
- Preserve useful specifics when safe, but do not require unnecessary detail.
- Prefer updating an existing work artifact over creating duplicates.
- Generalize sensitive implementation details (table names, proprietary logic, confidential data) while preserving career-relevant evidence.
- Do not retain proprietary source code, SQL, credentials, internal dataset names, sensitive financial information, employee/customer data, or restricted documents.

## Output

Create or update a `career.work_artifact` object in `ethan-life/domains/career/evidence/`.

Use schema `career.work_artifact` and version `1`.

The object should contain:

- `id`: stable ID
- `schema`: `career.work_artifact`
- `schema_version`: `1`
- `title`: project or initiative name
- `employer`: organization name, if known
- `role`: role title, if known
- `project`: project or initiative name
- `timeframe`: approximate dates
- `status`: `draft` | `verified` | `generalized`
- `provenance`: capture ID, source, and agent information
- `facts`: bullet list of confirmed facts
- `inferences`: bullet list of reasonable inferences, clearly marked
- `unknowns`: open questions or missing details
- `evidence_summary`: short narrative of what the user did and why it mattered
- `skills`: skills demonstrated
- `technologies`: technologies or tools used
- `outcomes`: confirmed or estimated outcomes, with confidence
- `interview_stories`: short stories useful for interviews
- `resume_candidates`: suggested accomplishment bullets derived from the evidence, clearly marked as derivative and not canonical
- `links`: typed relationships to related sources, captures, role context, capabilities, or other artifacts

## Lightweight frontmatter convention

A work artifact may include a compact frontmatter block for graph traversal:

```yaml
---
type: career.work_artifact
id: example-retail-operations-ai-platform
employer: example-retail-co
role: example-data-platform-engineer
capabilities:
  - ai-platforms-agentic-systems
  - technical-architecture
  - developer-enablement
  - ai-governance
technologies:
  - mcp
  - python
  - sql
  - bigquery
evidence_strength: high
status: active
---
```

`evidence_strength` is one of `low`, `medium`, `high`.

## Relationship types

Use typed relationships where applicable:

- `sourced_from` — capture or source that contributed this artifact
- `derived_from` — prior evidence or artifact this record updates
- `related_to` — related projects, roles, or skills
- `part_of` — initiative that belongs to a larger program or role
- `revised_by` — later version of the same artifact record
- `demonstrates` — capability demonstrated by this artifact

## Confirmation policy

- Auto-execute: creating a draft work artifact from clearly provided information.
- Ask for confirmation: marking an item as verified, adding impact claims, changing status from `draft`, or when ownership/scope is ambiguous.
