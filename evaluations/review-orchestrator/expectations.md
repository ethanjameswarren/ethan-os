# Review Orchestrator Evaluation Expectations

Static behavioral expectations for `scripts/core/review_orchestrator.py`.

## Selection

- Empty or low-value domains are skipped.
- Time-sensitive items are surfaced first.
- Decision review dates are respected.
- Goal mismatches and conflicts trigger reviews.
- Learning assessment / target dates trigger reviews.
- Due retention items trigger reviews.

## Delegation

- Each recommendation has a `delegated_workflow`.
- Domain-specific review logic is not duplicated inside the orchestrator.

## Boundedness

- The shortlist is limited by default.
- The user sees what was skipped and why.
- Normal output is concise.

## Fatigue

- The orchestrator does not run a full life audit by default.
- It skips domains with no new evidence.
- It does not repeat questions the user already answered.

## User control

- The orchestrator only recommends; it does not make material changes.
- Domain workflows handle their own confirmation rules.
