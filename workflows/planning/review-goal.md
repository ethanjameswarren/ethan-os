# Workflow: review-goal

## Purpose

Review how a goal is progressing and whether its strategies are producing useful evidence.

## Triggers

- "How am I doing on this goal?"
- "Review my AI-engineering goal."
- "Is this goal still worth it?"

## Steps

1. Resolve the goal by title or ID.
2. Build a `core.context-request` for intent `goal-review` around the goal and its linked objects.
3. Run `scripts/core/context_assembly.py` to produce a `core.context-bundle`.
4. Run `skills/core/cross-domain-reasoning.md` with the goal as `focal_id` and modes:
   - `connection` — what currently supports the goal
   - `gap` — what is missing
   - `tradeoff` — what conflicts with it
   - `priority_mismatch` — whether execution has stalled
5. Summarize:
   - goal and why it matters
   - active strategies
   - execution evidence
   - outcome evidence
   - gaps
   - conflicts
   - relevant decisions
   - possible adjustments
6. Return the summary to the user.

## Output

- concise goal review
- supporting objects
- gaps/conflicts
- neutral observations
- suggested adjustments, not applied automatically

## Activity vs outcome

- **Activity:** tasks completed, sessions held, schedule blocks executed.
- **Outcome:** artifacts, measurements, skill demonstrations, qualitative results.

Do not convert task counts into goal completion percentages.

## Confirmation policy

- Read-only review: no confirmation.
- Recommended adjustments require confirmation before any state change.
