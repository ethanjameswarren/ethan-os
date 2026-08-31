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
5. If the goal is the active strategic objective (a `long_term` planning goal with a linked career goal and milestone roadmap):
   a. Load the milestone roadmap (`ethan-life/domains/career/milestone-roadmap-*.md`) and identify the current horizon.
   b. For each of the eight dimensions (career position, capabilities, demonstrated evidence, assets/IP owned, professional network, public credibility, business/revenue experimentation, income trajectory), assess whether current state is **Ahead / On Track / At Risk / Off Track** relative to the horizon's expectations.
   c. Load the scorecard (`ethan-life/domains/career/scorecard-*.md`) and check for stale metrics (not updated within the review cadence).
   d. Include the structured trajectory assessment in the summary.
6. Summarize:
   - goal and why it matters
   - active strategies
   - execution evidence
   - outcome evidence
   - gaps
   - conflicts
   - relevant decisions
   - trajectory assessment (if strategic objective)
   - possible adjustments
7. Return the summary to the user.

## Output

- concise goal review
- supporting objects
- gaps/conflicts
- neutral observations
- trajectory assessment with per-dimension status (for strategic objectives)
- suggested adjustments, not applied automatically

## Activity vs outcome

- **Activity:** tasks completed, sessions held, schedule blocks executed.
- **Outcome:** artifacts, measurements, skill demonstrations, qualitative results.

Do not convert task counts into goal completion percentages.

## Confirmation policy

- Read-only review: no confirmation.
- Recommended adjustments require confirmation before any state change.
