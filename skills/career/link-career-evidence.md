# Skill: link-career-evidence

## Purpose

Maintain typed relationships between career objects so the career knowledge graph stays traversable and downstream workflows can walk from roles to artifacts to capabilities to outcomes.

## Inputs

- New or updated `career.work_artifact`
- Existing `career.role_context`
- Existing `career.capability` records
- Existing `career.work_artifact` records

## Required relationships

After capturing or updating a work artifact, ensure these links exist where applicable:

### Role → Work Artifact

The role context links to every work artifact that belongs to that employer/role.

```yaml
links:
  - target: <work-artifact-id>
    relation: includes
    note: Brief description of how the artifact relates to the role.
```

### Work Artifact → Capability

The work artifact links to each capability it demonstrates.

```yaml
links:
  - target: <capability-id>
    relation: demonstrates
    note: Specific aspect of the artifact that demonstrates this capability.
```

### Capability → Work Artifact

The capability links back to each supporting work artifact.

```yaml
links:
  - target: <work-artifact-id>
    relation: demonstrated_by
    note: Brief description of what the artifact proves about the capability.
```

### Work Artifact → Role

The work artifact links back to its parent role context.

```yaml
links:
  - target: <role-context-id>
    relation: part_of
    note: Employer/role this artifact belongs to.
```

### Work Artifact → Source

The work artifact links to any capture, document, or prior evidence it was derived from.

```yaml
links:
  - target: <source-id>
    relation: sourced_from
    note: Description of the source.
```

## Optional but recommended relationships

- Work Artifact → related Work Artifact (`related_to`)
- Capability → related Capability (`related_to`)
- Work Artifact → Technology list (if a technology registry exists)
- Capability → Domain / Application area

## Rules

- Do not duplicate the full artifact content inside another object. Use links.
- Keep link notes concise and specific.
- Prefer stable IDs that match the object filenames.
- When updating a work artifact, also update the related capability records so the back-links remain current.
- When a capability is first created, link it to the artifact that justified its creation.
- If a link already exists with equivalent meaning, do not create a duplicate.

## Output

Updated `links` sections in the affected `career.work_artifact`, `career.role_context`, and `career.capability` objects.

## Confirmation policy

- Auto-execute: adding or updating links based on clear relationships.
- Ask for confirmation: when a relationship is ambiguous or could imply a scope/seniority claim that is not well supported.
