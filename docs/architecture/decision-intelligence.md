# Decision Intelligence

## Purpose

Decision Intelligence captures why a meaningful choice was made and what happened later. It is a durable, inspectable record of choice, reasoning, and outcome.

## Schema

`knowledge.decision` captures:

- `title`
- `status` (active, implemented, superseded, reversed, completed, abandoned)
- `decision_date`
- `context`
- `options_considered`
- `chosen_option`
- `reasoning`
- `assumptions`
- `risks`
- `expected_outcomes`
- `related_goal_ids`
- `related_object_ids`
- `confidence`
- `review_date`
- `actual_outcome` (captured later)
- `lessons_learned` (captured later)

## What counts as a decision

A durable decision usually has:

- alternatives
- future consequences
- reasoning that may be useful later
- testable assumptions
- impact on goals or resources

Examples: taking a job, choosing a course, pausing a project, selecting an architecture, permanently moving a schedule block.

Not usually captured: casual preferences like "I'll have chicken tonight."

## Distinctions

- **Fact:** "I chose Course A."
- **Reason:** "Course A is more relevant to the AI-engineering goal."
- **Assumption:** "I can finish it within four weeks."
- **Expected outcome:** "It improves agent-evaluation knowledge."
- **Actual outcome:** captured during review, not at creation.

## Lifecycle

A decision can be:

- `active` — being acted on
- `implemented` — fully put into practice
- `superseded` — replaced by a newer decision
- `reversed` — undone
- `completed` — reviewed and closed
- `abandoned` — no longer pursued

When a decision changes, the old decision is preserved. The new decision links to it as `superseded` or `reversed`.

## Relationship to goals

Decisions can link to goals through `related_goal_ids` and `related_object_ids`. A course decision can support an AI-engineering goal. A project can support a career target. These links feed Cross-Domain Reasoning.

## Review

A decision is revisited at its `review_date` or when new evidence appears. The review compares original reasoning, assumptions, and expected outcomes to what actually happened. It avoids hindsight bias: a reasonable decision can have a bad outcome.
