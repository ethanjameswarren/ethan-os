# Schema Registry

Ethan Life objects reference schemas by logical identifier, not filesystem path.

## Registry location

`ethan-os/schemas/registry.yaml`

## Example object frontmatter

```yaml
---
id: idea-20260115-001
schema: knowledge.idea
schema_version: 1
title: Habits are votes for identity
---
```

## Resolution

`schema: knowledge.idea` + `schema_version: 1` maps through the registry to `ethan-os/schemas/domains/knowledge/idea.schema.yaml`.

## Rules

- `ethan-life` never stores physical paths to `ethan-os` schemas.
- Schema registry is versioned independently of the `ethan-os` release version.
- Backwards compatibility: `ethan-os` supports at least one previous schema version.
