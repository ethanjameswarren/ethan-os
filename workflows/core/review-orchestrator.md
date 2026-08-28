# Workflow: review-orchestrator

## Purpose

Decide which reviews are worth running right now, across all enabled domains.

## Triggers

- "What should I review this week?"
- "Is anything due for review?"
- Sunday Weekly Planning
- Monthly review

## Steps

1. Build a `core.context-request` for intent `review-orchestrate` over domains `[planning, knowledge, career, health, finance, music]`.
2. Run `scripts/core/context_assembly.py` to produce a `core.context-bundle`.
3. Run `scripts/core/review_orchestrator.py` with the current date.
4. Return the shortlist of recommended reviews and skipped domains with reasons.
5. Dispatch each recommendation to its delegated workflow.

## Delegated reviews

| review type | delegated workflow |
|-------------|--------------------|
| decision-review | `workflows/core/review-decision.md` |
| goal-review | `workflows/planning/review-goal.md` |
| learning-review | `workflows/knowledge/guided-learning.md` |
| knowledge-retention | `workflows/core/review.md` |
| finance-review | `workflows/finance/monthly-budget-review.md` |
| health-review | `workflows/health/weekly-review.md` |
| music-review | `workflows/music/review-spotify-matches.md` |

## Output

- concise shortlist of recommended reviews
- reasons for each
- domains skipped and why

## Rules

- Skip empty or low-value reviews.
- Never run a domain review just because the domain exists.
- Do not make material changes automatically.
- Keep normal user output bounded and conversational.
