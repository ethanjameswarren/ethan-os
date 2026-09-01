# Workflow: weekly-review

## Purpose

Periodically surface what needs attention across active Goals, Projects, and Tasks, and on Sunday build the upcoming week's concrete plan.

## Steps

1. Build a `core.context-request` with intent `sunday-review` and domains `[planning, knowledge, career, health, finance]`.
2. Run `scripts/core/context_assembly.py` to produce a `core.context-bundle` of active goals, projects, tasks, learning programs, schedule constraints, and relevant reviews.
3. Run `scripts/core/review_orchestrator.py` to determine which reviews are actually worth running this week.
4. Run `skills/core/cross-domain-reasoning.md` to surface cross-domain patterns in the bundle.
5. Run the delegated reviews returned by the orchestrator (e.g., `workflows/planning/review-goal.md`, `workflows/core/review-decision.md`).
6. Run `skills/planning/suggest-next-actions.md` to identify unblocked tasks, blocked items, stale projects, and goals without momentum, then compare actionable work by commitment risk, impact, strategic relevance, learning, evidence, leverage, ownership, compounding value, opportunity cost, and realistic capacity.
7. Run `workflows/planning/analyze-schedule-overrides.md` on the most recent overrides. Surface meaningful schedule drift, not every isolated override.
8. If the intent is "sunday-review" or the user asks to plan next week, run `skills/planning/sunday-weekly-planning.md` on the bundle and the review findings to build a draft `planning.weekly-plan`.
9. Otherwise, optionally create a summary artifact of the findings (plain text; no new schema required for v0.1).
10. Return the prioritized findings or the candidate weekly plan to the user.

## Output

- prioritized list of findings with reasons, or
- a draft `planning.weekly-plan` for the upcoming week

## Confirmation policy

- Read-only review: no confirmation required to run.
- Sunday weekly plan: present the draft; only save as `accepted` after the user confirms.
- Any status change the user decides to make based on the findings goes through `workflows/core/revise.md`.
