# Validator

## Purpose

Validate objects before writing them to `ethan-life`.

## Deterministic checks

1. Valid YAML frontmatter.
2. Schema identifier resolves in `ethan-os/schemas/registry.yaml`.
3. Schema version is supported.
4. Required fields present: `id`, `schema`, `schema_version`, `title`, `created_at`.
5. Provenance present.
6. Relationship target IDs exist (no broken references).
7. Duplicate IDs not created.
8. Markdown body readable.

## AI-quality checks

Optional and documented separately:

- capture fidelity
- source/user belief separation
- relationship quality
- summary usefulness
- excessive object creation

## Failure handling

- Deterministic failures block writes and report the issue.
- AI-quality warnings are surfaced but do not block unless configured.
