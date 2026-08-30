# Skill: synthesize-role-context

## Purpose

Maintain a canonical, cumulative summary of each professional role based on the work artifacts associated with it.

Role context captures recurring responsibilities, operating environment, typical scope, and positioning signals that cut across individual projects. It is consumed later by resume, interview, and job-matching workflows.

## Inputs

- New or updated `career.work_artifact`
- Existing `career.role_context` for the same employer/role, if any
- Related work artifacts for the same employer/role
- Existing capability records that may be relevant

## When to update

Update the canonical role context when the new work artifact:

- Introduces a new responsibility not already represented
- Strengthens an existing responsibility with new evidence
- Establishes a new technical area or domain
- Changes the apparent seniority, scope, or independence of the role
- Demonstrates cross-functional ownership
- Suggests a different way the role should be positioned for future targets

Do not update the role context for one-off tasks that do not represent a recurring pattern.

## What to capture

- Role summary — one-paragraph synthesis of the role
- Operating environment — stack, tools, data sources, team shape
- Core responsibilities — recurring duties and ownership areas
- Typical work patterns — mix of recurring reporting, ad-hoc analysis, product development, etc.
- Career signals — dimensions the role demonstrates (e.g., end-to-end ownership, cross-functional partnership, technical architecture)
- Positioning guidance — how the role should be described relative to common job families
- Scope indicators — scale, independence, leadership, and stakeholder exposure

## Rules

- Summarize patterns across projects; do not duplicate full project details.
- Distinguish confirmed patterns from reasonable inferences.
- Do not inflate titles, seniority, or scope beyond what the artifacts support.
- Preserve historically meaningful role boundaries if the user's responsibilities changed materially during the role.
- Link back to the work artifacts that support each claim.

## Output

Create or update a `career.role_context` object in `ethan-life/domains/career/roles/`.

Use schema `career.role_context` and version `1`.

The object should contain:

- `id`: stable ID
- `schema`: `career.role_context`
- `schema_version`: `1`
- `title`: role context title
- `employer`: organization name
- `role`: role title
- `timeframe`: approximate dates
- `status`: `draft` | `verified`
- `summary`: concise role description
- `operating_environment`: tools, platforms, data sources, team context
- `core_responsibilities`: recurring duties
- `typical_work_patterns`: description of common work modes
- `career_signals`: demonstrated professional dimensions
- `positioning_guidance`: how to frame the role for different target families
- `scope_indicators`: scale, independence, leadership, stakeholder exposure
- `links`: relationships to work artifacts and capabilities
- `provenance`: capture ID, source, and agent information

## Relationship types

- `synthesized_from` — work artifacts used to build or update this role context
- `related_to` — related role contexts or capabilities

## Confirmation policy

- Auto-execute: updating role context from clearly provided work artifacts.
- Ask for confirmation: changing the role title, altering seniority/scope language, or when the synthesized context materially changes how the role would be presented.
