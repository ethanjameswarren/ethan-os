# Review Orchestrator

## Purpose

The Review Orchestrator decides which reviews are worth running right now. It prevents review fatigue by skipping empty or low-value domain reviews and surfacing only the items that matter.

## Responsibility

The orchestrator answers:

> "What deserves attention?"

It does not ask every possible review question. It does not run a full life audit. It delegates domain-specific review logic to the appropriate workflow.

## Flow

```
USER REQUEST
→ INTENT (sunday-review / monthly-review / review-orchestrate)
→ CONTEXT ASSEMBLY
→ CROSS-DOMAIN REASONING
→ REVIEW ORCHESTRATOR
→ DELEGATED DOMAIN REVIEWS
→ NEXT WEEK / SUMMARY
```

## What it considers

- Decisions that have reached `review_date`
- Active learning programs with approaching `target_completion_date` or `assessment_date`
- Goals with `priority_mismatch` (active but no supporting execution)
- Due `knowledge.review` items
- Cross-domain tradeoffs and conflicts
- Domains with no meaningful state are skipped

## Priority

Higher priority:

1. time-sensitive or deadline-related
2. decision review date reached
3. goal blocked or conflicted
4. repeated execution mismatch
5. domain review explicitly due
6. retention due
7. optional reflection

## Delegation

Each recommendation includes a `delegated_workflow`. The orchestrator does not run the review itself.

## Boundedness

The orchestrator returns a shortlist, defaulting to 3–7 high-value recommendations. It also reports skipped domains so the user can see what was considered and omitted.

## Anti-fatigue

The orchestrator:

- skips empty domains
- reuses known answers
- avoids duplicate questions
- combines related prompts
- allows the user to skip or ignore
- never makes material changes automatically
