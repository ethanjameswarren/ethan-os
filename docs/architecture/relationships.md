# Relationship Model

Relationships are inline typed links.

## Typed relationships

| relationship | direction | meaning |
|--------------|-----------|---------|
| sourced_from | → | object derives from a source or capture |
| supports | → | one idea supports another |
| contradicts | → | one idea challenges another |
| related_to | ↔ | meaningful non-specific connection |
| derived_from | → | new idea built from existing idea |
| applies_to | → | application applies to an idea |
| tested_by | → | experiment tests an idea |
| revised_by | → | new version supersedes old |
| part_of | → | component of a larger structure |

## Storage

Inline in object frontmatter:

```yaml
links:
  - target: src-20260115-001
    relation: sourced_from
    note: extracted from chapter 4 notes
```

## Rules

- Keyword similarity alone is not sufficient.
- Relationships require contextual justification.
- No central relationship database in v0.1.
