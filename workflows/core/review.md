# Workflow: review

## Purpose

Surface items worth revisiting.

## Steps

1. Load all knowledge objects.
2. Use `skills/knowledge/suggest-review.md` to identify candidates.
3. Optionally create a Review object in `ethan-life/domains/knowledge/reviews/`.
4. Return prioritized list with reasons.

## Output

- list of items to review with reasons
- Review object ID (if created)

## Confirmation policy

- Creating review artifacts: auto-execute.
- If a review implies changing an important belief, ask for confirmation.
