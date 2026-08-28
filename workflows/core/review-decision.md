# Workflow: review-decision

## Purpose

Revisit a meaningful decision and compare expectations with reality.

## Triggers

- "How did that decision work out?"
- "Review my decision to..."
- Decision review date reached

## Steps

1. Load the `knowledge.decision` object.
2. Build a `core.context-bundle` around the decision's linked goals, projects, learning, and objects.
3. Run `skills/core/cross-domain-reasoning.md` to find what changed.
4. Compare:
   - original reasoning
   - original assumptions
   - expected outcomes
   - actual outcomes now known
5. Identify lessons without applying hindsight bias.
6. Ask the user for actual outcome and lessons if not already recorded.
7. Update the decision with `actual_outcome` and `lessons_learned` if the user provides them.
8. Optionally change `status` to `completed`, `superseded`, `reversed`, or `abandoned` after confirmation.

## Output

- comparison of expectations vs actual
- lessons learned
- updated `knowledge.decision` object if the user confirms

## Confirmation policy

- Read-only review: no confirmation.
- Updating `actual_outcome` or `lessons_learned`: confirm if it contradicts the original record.
- Changing `status` to `superseded` or `reversed`: explicit confirmation.
