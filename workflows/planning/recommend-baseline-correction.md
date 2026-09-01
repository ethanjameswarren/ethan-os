# Workflow: recommend-baseline-correction

## Purpose

Generate an evidence-backed baseline schedule correction and require explicit user approval before applying it.

## Input

- A `schedule-drift-report` from `workflows/planning/analyze-schedule-overrides.md` or a concentrated pattern.
- Active `planning.baseline-schedule`.
- IDs of supporting `planning.schedule-override` objects.

## Steps

1. For each drift-flagged block, compute a concrete proposed correction:
   - Use the median actual `start_time` and `end_time`.
   - Use the most common replacement `day_of_week` if the day changed consistently.
   - Use the most common replacement `label` if the activity changed.
2. Draft a recommendation containing:
   - **Baseline**: current recurring block (`day_of_week`, `start_time`, `end_time`, `label`).
   - **Observed**: counts, override rate, median shift, typical duration, and the most common actual values.
   - **Pattern**: one-sentence summary of the repeated deviation.
   - **Recommendation**: the new proposed baseline block.
   - **Evidence**: list of override IDs and a summary statistic.
3. Present the recommendation to the user and ask for approval.
4. If the user accepts:
   - Update the `planning.baseline-schedule` recurring block.
   - Create a record of the accepted recommendation with supporting evidence.
   - Optionally regenerate the current weekly plan.
5. If the user rejects:
   - Record the rejection with the reason given by the user, if any.
   - Store the rejected recommendation and the evidence that triggered it.
   - Do not make the same recommendation again unless new evidence materially changes the pattern.

## Output

- Proposed recommendation text for user review.
- Updated `planning.baseline-schedule` if accepted.
- A `recommendation-record` artifact (accepted or rejected).

## Rules

- Do NOT silently mutate the canonical baseline schedule.
- Always explain why the change is proposed.
- Record the user's decision explicitly.
- A rejected recommendation is itself evidence and prevents repetitive re-suggestion.
