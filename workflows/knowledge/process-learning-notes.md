# Workflow: process-learning-notes

## Purpose

Turn messy learning input into structured knowledge.

## Steps

1. Create/update Capture object in `ethan-life/domains/knowledge/captures/`.
2. Identify or create Source object in `ethan-life/domains/knowledge/sources/`.
3. Use `skills/knowledge/extract-ideas.md` to extract candidate ideas.
4. Use `skills/knowledge/resolve-ideas.md` to match existing ideas or create new ones.
5. Use `skills/knowledge/suggest-relationships.md` to propose typed links.
6. Create/update Idea objects in `ethan-life/domains/knowledge/ideas/`.
7. Use `skills/knowledge/generate-summary.md` to create or refresh canonical Summary.
8. Update review state (flag uncertain items, contradictions, etc.).
9. Validate all objects.
10. Write to `ethan-life`.

## Output

- created/updated object IDs
- brief synthesis of what was processed
- any items needing review

## Confirmation policy

- Creating captures, sources, and extracting ideas: auto-execute.
- Creating relationships: auto-execute for low-risk links; ask if relation implies contradiction or belief change.
- Updating an existing summary or idea with material semantic change: ask for confirmation.
