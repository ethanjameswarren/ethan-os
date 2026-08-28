# Skill: schedule-review

## Purpose

Maintain lightweight spaced-review state for durable reading takeaways.

## Deterministic schedule

Base intervals in days:

```
INTERVALS = [1, 3, 7, 14, 30, 60, 120]
```

A retention item starts at `interval_index: 0`, with `next_review_due_at` = `first_learned_at + INTERVALS[0]`.

## Recall outcomes

When a review occurs, classify the result:

- `strong`: user accurately reconstructs the core idea with little or no prompting.
- `partial`: user recalls part but misses an important piece, or is shaky.
- `failed`: user cannot recall, or recall is substantially wrong.
- `skipped`: user opts out of this review ("not now", "skip").

## Interval adjustment

Given outcome and current `interval_index`:

- `strong`: `interval_index = min(len(INTERVALS) - 1, interval_index + 1)`
- `partial`: `interval_index = max(0, interval_index - 1)`
- `failed`: `interval_index = 0`
- `skipped`: do not change interval; keep `next_review_due_at` within the next 1-3 days or leave unchanged based on user preference.

Then:

```
next_review_due_at = today + INTERVALS[interval_index]
```

## Confidence / strength

- `current_confidence` starts at `medium`.
- `strong` review → `high` (if not already).
- `partial` review → `medium`.
- `failed` review → `low`.

## Counters

- Increment `successful_recalls` for `strong` and `partial`.
- Increment `failed_recalls` for `failed`.

## Priority adjustments

- `retention_priority` is normally set during compression.
- User may explicitly override: "this one is important" → `high`; "I don't care about remembering this" → pause/archive.
- High-priority items may be surfaced more often, but the interval schedule is the default.

## Status values

- `active`: item is in the review loop
- `paused`: user said "not now" or temporarily skipped
- `archived`: user opted out permanently

## Output

- Updated retention item with `last_reviewed_at`, `next_review_due_at`, `interval_index`, `current_confidence`, `last_recall_result`, counters, status.
