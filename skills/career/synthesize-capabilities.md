# Skill: synthesize-capabilities

## Purpose

Identify reusable professional capabilities demonstrated by career evidence and maintain a cumulative evidence-backed representation of those capabilities.

A capability is not a keyword extracted from a project. A capability represents something the person has repeatedly or materially demonstrated they can do.

## What is and is not a capability

Bad capabilities (these are technologies):

- BigQuery
- Python
- Power BI

Good capabilities (these are reusable professional competencies):

- Experimentation & Causal Measurement
- Analytics Engineering
- AI Platform Architecture
- Forecasting
- BI Architecture
- Technical Leadership
- Data Quality & Reconciliation

## Inputs

- New `career.work_artifact`
- Existing `career.capability` records
- Existing `career.role_context`
- Related career evidence

## Evaluation

For each potential capability, determine:

### Evidence strength

- `0` — Mentioned only
- `1` — Assisted
- `2` — Independently applied
- `3` — Designed solution
- `4` — Repeatedly demonstrated
- `5` — Architected / established reusable organizational capability

### Evidence dimensions

- Complexity
- Independence
- Scale
- Repetition
- Business importance
- Technical depth
- Architectural ownership
- Cross-functional scope
- Reusability
- Decision impact

## Behavior

If the capability exists:

- Link the new evidence.
- Update demonstrated methods.
- Update domains / applications.
- Strengthen evidence level when justified.
- Add new scale or scope evidence.

If the capability does not exist:

- Create it only when materially demonstrated.
- Do not create capabilities from incidental tool usage or one-line mentions.

## Rules

- Every capability claim must be traceable to one or more work artifacts.
- Do not make unsupported capability claims.
- Do not create capabilities solely because a technology was used.
- Prefer broadening an existing capability to creating a near-duplicate.
- Keep capability names stable and reusable across roles.

## Output

Create or update `career.capability` objects in `ethan-life/domains/career/capabilities/`.

Use schema `career.capability` and version `1`.

The object should contain:

- `id`: stable ID
- `schema`: `career.capability`
- `schema_version`: `1`
- `title`: capability name
- `description`: concise definition of the capability
- `status`: `draft` | `verified`
- `evidence_level`: current highest evidence strength (`0`–`5`)
- `demonstrated_methods`: list of methods, approaches, or patterns observed across artifacts
- `domains`: professional domains where the capability has been applied
- `applications`: specific projects or contexts where it has been used
- `related_technologies`: technologies typically associated with the capability in this person's experience
- `evidence`: list of work artifact IDs that demonstrate the capability
- `outcomes`: observable results linked to the capability
- `notes`: any caveats, growth trajectory, or context
- `links`: relationships to work artifacts, role contexts, or other capabilities
- `provenance`: capture ID, source, and agent information

## Lightweight frontmatter convention

A capability may include a compact frontmatter block for graph traversal:

```yaml
---
type: career.capability
id: experimentation-causal-measurement
evidence:
  - example-checkout-messaging-test
  - example-delivery-messaging-test
  - example-payroll-pilot-analysis
  - example-product-pickup-analysis
---
```

## Relationship types

- `demonstrated_by` — work artifact that demonstrates this capability
- `strengthened_by` — newer work artifact that raises the evidence level
- `related_to` — related capabilities
- `applied_in` — role context or domain where the capability has been applied

## Confirmation policy

- Auto-execute: updating an existing capability from clearly provided evidence.
- Ask for confirmation: creating a new capability, raising the evidence level to `4` or `5`, or when the evidence is indirect or inferential.
