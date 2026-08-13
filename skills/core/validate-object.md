# Skill: validate-object

## Purpose

Validate a generated object against the schema registry.

## Input

- object frontmatter and Markdown body
- schema identifier and version

## Output

- valid: true | false
- errors: list of deterministic issues
- warnings: list of quality issues

## Deterministic checks

1. Frontmatter parses as valid YAML.
2. `schema` resolves in `schemas/registry.yaml`.
3. `schema_version` is supported.
4. Required fields present.
5. Field values match schema types/enums.
6. `provenance` present.
7. Relationship `target` IDs exist (if checkable).
8. `id` is unique within repository.

## Instructions

- Block writes on deterministic failures.
- Surface warnings without blocking unless configured.
