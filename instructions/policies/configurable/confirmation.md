# Configurable Confirmation Policy

Defines when the system asks for human confirmation before acting.

## Default configuration

- **Auto-execute**: creating captures, creating obvious sources, extracting ideas, adding low-risk relationships, updating summaries.
- **Ask for confirmation**: Ethan's meaning is materially ambiguous; an important interpretation is being changed; the system may change Ethan's stated position; confidence is low; the operation has meaningful semantic consequences.

## Permitted configuration values

- `auto`: system acts without confirmation for all reversible low-risk operations.
- `ask-on-ambiguity`: ask when meaning is unclear.
- `ask-on-belief-change`: ask when belief or interpretation may materially change.
- `ask-all`: ask before all non-trivial writes.

## v0.1 default

`auto` for low-risk, `ask-on-ambiguity` and `ask-on-belief-change` for semantic operations.
