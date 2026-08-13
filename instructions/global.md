# Global Instructions

Apply to all workflows unless a domain or workflow instruction overrides them without violating invariants or mandatory policies.

## Principles

1. Capture first, organize second.
2. Preserve raw input where appropriate.
3. Minimize manual maintenance: assign IDs, filenames, relationships, and structure automatically.
4. Prefer plain Markdown and YAML frontmatter.
5. Distinguish source claims from Ethan's interpretation.
6. Only create meaningful relationships.
7. Keep summaries personal, not generic.
8. Preserve evolution without duplicating Git history.

## Default behaviors

- Auto-execute low-risk, reversible organization.
- Ask for confirmation on material ambiguity or important semantic changes.
- Use stable IDs derived from timestamp and short hash.
- Use typed inline relationships.
- Write objects to `ethan-life/domains/<domain>/<type>/`.
