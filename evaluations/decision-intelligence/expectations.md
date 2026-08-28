# Decision Intelligence Evaluation Expectations

Static behavioral expectations for `knowledge.decision` and `skills/knowledge/capture-decision.md`.

## Capture

- Trivial decisions are not captured by default.
- Capture preserves alternatives, reasoning, assumptions, and expected outcomes.
- `actual_outcome` is not set at capture time.
- Expected and actual outcomes remain distinct.
- Decisions can link to goals and related objects.

## Lifecycle

- `status` reflects the decision's current state.
- A changed decision creates a new object; the old one is linked, not edited.
- `superseded`, `reversed`, and `abandoned` statuses preserve history.

## Review

- The review workflow loads the original decision and surrounding context.
- Comparison is made between expected and actual outcomes.
- Hindsight bias is avoided.
- The user can update `actual_outcome` and `lessons_learned` without rewriting original reasoning.

## Cross-domain

- Cross-Domain Reasoning recognizes decisions as supporting or related to goals and projects.
- Decision review dates can trigger the Review Orchestrator.

## No autonomous action

- The system does not create, schedule, or purchase anything automatically.
- Status changes require confirmation.
