# History Strategy

## Ordinary history

Git provides ordinary file history.

## Semantic history

For meaningful semantic evolution, use an optional Markdown `## Evolution` section.

Example:

```markdown
## Evolution

- 2026-01-20: Initially captured from Atomic Habits Ch 4.
- 2026-02-03: Added counterargument after reading Fogg; confidence lowered.
```

## Structured revisions

Structured `revisions[]` arrays are reserved only for objects where machine-parseable history is proven necessary. They are not required in v0.1.

## No duplication

Do not mirror Git diffs in `## Evolution`. Only record semantic changes.
