# Workflow: ask

## Purpose

Answer a natural-language question from stored knowledge.

## Steps

1. Parse question.
2. Load global context and knowledge domain context.
3. Use `skills/knowledge/answer-question.md` to find relevant sources, captures, ideas, summaries.
4. Compose concise answer with citations.
5. Return answer, citations, and confidence.

## Output

- answer text
- cited object IDs
- confidence
- follow-up suggestions

## Confirmation policy

- Read-only workflow: no confirmation required.
