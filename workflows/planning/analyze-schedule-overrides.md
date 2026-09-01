# Workflow: analyze-schedule-overrides

## Purpose

Analyze accumulated schedule overrides as longitudinal evidence to detect patterns and schedule drift.

## Input

- Active `planning.baseline-schedule`.
- All active `planning.schedule-override` objects.
- `instructions/policies/configurable/schedule-drift-detection.md` thresholds.

## Steps

1. Load overrides with `status: active` and `scope: one_off` or `temporary`.
2. Group overrides by `target_block` (`label` + `day_of_week`). Blocks added without a target are grouped by their `block.label`.
3. For each group, compute:
   - `baseline_occurrences`: how many times the block has occurred in the lookback window.
   - `override_count` and `override_rate`.
   - `cancellation_rate`.
   - `median_start_shift_minutes`: `actual_start` − `planned_start`.
   - `median_duration_delta_minutes`: `actual_duration` − `planned_duration`.
   - `most_common_replacement`: label and time/day used most often.
   - `most_common_reason_category`.
   - `classification_distribution`: counts of exception / preference / friction / unknown.
4. Score each group:
   - Ignore isolated `exception` overrides.
   - A pattern is `emerging` when it crosses `observe_threshold` with `confidence_min`.
   - A pattern is `drift` when it crosses `drift_threshold` with `confidence_min` and `min_occurrences_for_baseline_proposal`.
5. Produce a `schedule-drift-report`:
   - `patterns` with confidence, effect, and statistics.
   - `drift_flags` for blocks that may need baseline correction.
   - `recent_exceptions` for information only.
   - `recommended_next_step`: none, observe, or recommend-correction.

## Output

- `schedule-drift-report` artifact.
- List of blocks to pass to `workflows/planning/recommend-baseline-correction.md`.

## Rules

- Use robust, simple statistics: counts, medians, and proportions. No ML.
- Require consistency, not just frequency. Five random overrides mean less than five overrides that all move the block 60 minutes later.
- One-off exceptions should have little or no influence on baseline recommendations.
- Do not modify the baseline schedule or any raw override files.
