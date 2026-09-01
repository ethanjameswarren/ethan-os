# Configurable Schedule Drift Detection Policy

Defines how accumulated schedule overrides become evidence that the baseline schedule should change.

## Default configuration

- `observe_threshold`: 3 similar overrides within the last 8 occurrences of a recurring block triggers an emerging pattern.
- `drift_threshold`: 5 similar overrides within the last 8 occurrences triggers a schedule-drift flag.
- `confidence_min`: 0.6 (60% of relevant occurrences must share the same effect to count as a pattern).
- `time_window_weeks`: 12 (look back at most 12 weeks when computing rates).
- `min_occurrences_for_baseline_proposal`: 5 total baseline occurrences before a correction can be proposed.
- `consecutive_exception_limit`: 2 recent exceptions before exceptions are treated as preference if no strong reason.
- `median_shift_minutes_for_recommendation`: 15 (median time shift must exceed 15 minutes to propose a baseline move).
- `post_change_observations`: 3 (number of occurrences after an accepted change before validating).

## Permitted configuration values

- `strict`: drift_threshold 7, observe_threshold 5, confidence_min 0.75.
- `default`: as above.
- `aggressive`: drift_threshold 3, observe_threshold 2, confidence_min 0.5.

## v0.1 default

`default`.
