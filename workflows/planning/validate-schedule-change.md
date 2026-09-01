# Workflow: validate-schedule-change

## Purpose

Check whether an accepted baseline schedule change actually reduced the need for overrides.

## Input

- The corrected baseline block.
- Override history for that block before the accepted change.
- Overrides that occurred after the accepted change.
- `instructions/policies/configurable/schedule-drift-detection.md` thresholds.

## Steps

1. Collect the `N` occurrences before the change, where `N = post_change_observations`.
2. Collect the first `N` occurrences after the change. If fewer than `N` have occurred, mark validation as `needs_more_data`.
3. Compute the override rate before and after the change for the same block.
4. Compare shift/duration patterns:
   - If the new baseline block now matches the observed actual behavior, post-change overrides should decrease.
5. If the post-change override rate is materially lower, mark the change as `validated`.
6. If the rate is not lower or the pattern remains, return the block to `workflows/planning/analyze-schedule-overrides.md` for continued learning.
7. Record the validation result on the recommendation record.

## Output

- A validation report with before/after override rates and a status:
  - `validated`
  - `not_validated`
  - `needs_more_data`

## Rules

- Do not declare a change successful after only one occurrence.
- Preserve all historical override evidence.
- Validation is continuous: a change can be re-evaluated as more data arrives.
