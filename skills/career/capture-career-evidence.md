# Skill: capture-career-evidence

## Purpose

Convert raw project, role, accomplishment, or work-context information into durable, reusable career evidence.

The resulting evidence supports future outputs such as resumes, interviews, LinkedIn profiles, career planning, skills analysis, promotion cases, and job matching. This skill captures evidence; it does not generate tailored resume bullets.

## Input

Accept any combination of:

- project-context Markdown
- notes
- role descriptions
- accomplishments
- technical documentation that is safe to retain
- user explanations
- existing resume content
- sanitized work-project summaries

## Extract

Where supported by the input, capture:

- employer / organization
- role
- project or initiative
- approximate timeframe
- business problem
- why the work mattered
- Ethan's confirmed responsibilities
- technical approach
- architecture at an appropriate level
- technologies / tools
- scale and complexity
- important decisions Ethan made
- problems Ethan personally solved
- measurable outcomes
- business impact
- technical impact
- process improvements
- leadership
- mentoring
- stakeholder / cross-functional collaboration
- ownership / autonomy
- skills demonstrated
- notable constraints or challenges
- useful interview stories
- supporting provenance

## Evidence rules

- Clearly distinguish confirmed fact from reasonable inference and unknown.
- Never turn an inference into a confirmed accomplishment.
- Never invent metrics, ownership, scope, technologies, business impact, leadership, or outcomes.
- Preserve useful specifics when safe, but do not require unnecessary detail.
- Prefer updating an existing project/experience record over creating duplicates.

## Confidentiality

Career evidence imported from work must be appropriate for personal career use.

Do **not** retain:

- proprietary source code
- SQL
- credentials
- internal dataset or table names
- sensitive financial information
- employee or customer information
- proprietary business logic
- confidential strategy
- restricted documents

Generalize sensitive implementation details while preserving the career-relevant evidence.

## Output

Create or update a Career Evidence object in `ethan-life/domains/career/evidence/`.

Use schema `career.evidence` and version `1`.

The object should contain:

- `id`: stable ID
- `schema`: `career.evidence`
- `schema_version`: `1`
- `title`: project, role, or accomplishment name
- `employer`: organization name, if known
- `role`: role title, if known
- `timeframe`: approximate dates
- `status`: `draft` | `verified` | `generalized`
- `provenance`: capture, source, and agent information
- `facts`: bullet list of confirmed facts
- `inferences`: bullet list of reasonable inferences, clearly marked
- `unknowns`: open questions or missing details
- `evidence_summary`: short narrative of what Ethan did and why it mattered
- `skills`: skills demonstrated
- `technologies`: technologies or tools used
- `outcomes`: confirmed or estimated outcomes, with confidence
- `interview_stories`: short stories useful for interviews
- `resume_candidates`: suggested accomplishment bullets derived from the evidence, clearly marked as derivative and not canonical
- `links`: typed relationships to related sources, captures, or other evidence

## Core principle

Store:

> what Ethan actually did and what evidence supports it

rather than:

> what would sound impressive on a resume

## Confirmation policy

- Auto-execute: creating a draft evidence object from clearly provided information.
- Ask for confirmation: marking an item as `verified`, adding impact claims, changing status from `draft` to `verified` or `generalized`, or when ownership/scope is ambiguous.

## Relationship types

Use typed relationships from the core relationship model where applicable:

- `sourced_from` — capture or source that contributed this evidence
- `derived_from` — prior evidence or resume content this record updates
- `related_to` — related projects, roles, or skills
- `part_of` — initiative that belongs to a larger program or role
- `revised_by` — later version of the same evidence record

## Note

This skill is an extension point for the future Career domain. It does not create a full Career domain implementation in v0.1 and does not generate tailored resumes.
