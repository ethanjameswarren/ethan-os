# Workflow: ask

## Purpose

Answer a natural-language question from stored knowledge.

## Steps

1. Parse the question and classify intent.
2. Build a `core.context-request` for the question.
3. Run `scripts/core/context_assembly.py` to retrieve a `core.context-bundle` across relevant domains.
4. Use `skills/knowledge/answer-question.md` to reason over the bundle and compose a concise answer with citations.
5. Return answer, cited object IDs, and confidence.

## Output

- answer text
- cited object IDs
- confidence
- follow-up suggestions

## Confirmation policy

- Read-only workflow: no confirmation required.
