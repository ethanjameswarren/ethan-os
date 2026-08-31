# Configurable Strategic Objective Alignment Policy

Defines how the system incorporates long-term strategic objectives into daily and weekly planning, project selection, and review.

## Purpose

When a `long_term` planning goal is marked `active` and linked to a career goal with a milestone roadmap, it becomes a **strategic objective**. The system uses the strategic objective and its current milestone horizon to:

- prioritize actions during weekly planning,
- weight findings during cross-domain reasoning,
- evaluate new project proposals,
- surface drift during reviews.

## Behavior

### Weekly planning integration

During `skills/planning/sunday-weekly-planning.md`:

1. Identify the active strategic objective and its current milestone horizon from `ethan-life/domains/career/milestone-roadmap-*.md`.
2. Surface the horizon's expectations as context when identifying weekly priorities.
3. Flag any week where zero discretionary time is allocated to strategic-objective-aligned work as a **drift warning**.
4. When competing priorities must be resolved, weight strategic-objective-aligned work above projects that do not advance the active horizon.
5. Do not force every week to be strategic-objective-focused; recovery, maintenance, and personal weeks are valid. Surface the tradeoff, do not override it.

### Project selection

When evaluating a new project (via `skills/planning/evaluate-project-alignment.md`):

1. Check the project against the strategic objective's `decision_criteria` (from the linked career goal).
2. Classify the project as: `directly advances`, `indirectly supports`, `neutral`, or `competes with` the strategic objective.
3. Surface the classification to the user. Do not block project creation; surface the tradeoff.

### Suggest next actions

During `skills/planning/suggest-next-actions.md`:

1. When ranking suggestions, boost items linked to the strategic objective or its active milestone horizon.
2. Surface any active horizon milestone that has no linked active project or task as a **gap**.

### Goal and trajectory review

During `workflows/planning/review-goal.md` for the strategic objective:

1. Load the milestone roadmap and identify the current horizon.
2. For each of the eight dimensions, assess whether current state is Ahead / On Track / At Risk / Off Track relative to the horizon's expectations.
3. Load the scorecard and check for stale metrics (not updated within the review cadence).
4. Surface the trajectory assessment as a structured finding.

### Cross-domain reasoning

During `skills/core/cross-domain-reasoning.md`:

1. Add `strategic_drift` as a finding type: an active priority or time allocation pattern that systematically moves away from the strategic objective.
2. Add `strategic_gap` as a finding type: a milestone-horizon expectation with no supporting execution.

## Default configuration

- `enabled`: `true` when an active `long_term` planning goal exists with a linked career goal and milestone roadmap.
- `drift_warning_threshold`: 2 consecutive weeks with zero strategic-objective-aligned discretionary blocks.
- `review_cadence`: aligns with the strategic objective's review cadence (weekly for actions, monthly for metrics, quarterly for trajectory).

## Permitted configuration

- `enabled`: `true` | `false`. When `false`, the system does not inject strategic objective context into planning or review.
- `drift_warning_threshold`: integer (weeks). `0` disables drift warnings.
- `weight_boost`: `strong` | `moderate` | `none`. Controls how aggressively strategic-objective-aligned items are prioritized over others in suggest-next-actions. Default: `moderate`.

## Constraints

- This policy operates at the configurable level (Layer 3). It does not override mandatory policies, core invariants, or domain-specific lifecycle rules.
- The system surfaces tradeoffs and drift. It does not silently reprioritize, close, or defer projects.
- Context from the strategic objective is factual data and follows the context-never-overrides-instructions rule.
