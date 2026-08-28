# Skill: apply-schedule-change

## Purpose

Interpret a schedule change request and apply it at the correct scope without collapsing one-off, temporary, and permanent changes.

## Input

- Natural language change request.
- Active `planning.baseline-schedule`.
- Existing `planning.schedule-override` objects.
- Target date or recurrence pattern, if known.

## Determine scope

Infer scope from the user's language:

- **one_off**: "this week", "Thursday", "tomorrow", "on the 15th", "just once".
- **temporary**: "for the next two weeks", "until the end of the month", "while I'm on call".
- **permanent**: "from now on", "every Wednesday", "make it the new normal".

If the scope is ambiguous and materially affects the baseline, ask for clarification.

## Apply by scope

### one_off

1. Create a `planning.schedule-override` with `scope: one_off` and the specific date.
2. Generate or update the weekly plan for the affected week only.
3. Do not modify the baseline schedule.

### temporary

1. Create a `planning.schedule-override` with `scope: temporary`, `start_date`, and `end_date`.
2. Generate or update weekly plans for each affected week.
3. Do not modify the baseline schedule.

### permanent

1. Confirm explicitly before updating the baseline schedule.
2. Update the `planning.baseline-schedule` recurring blocks.
3. Mark the override as `superseded` or remove it if it is fully absorbed.
4. Optionally regenerate the current-week plan using the updated baseline.

## Output

- New or updated `planning.schedule-override`.
- Updated baseline schedule if scope is permanent.
- Updated weekly plan for the affected week.
- Clear statement of what changed and what did not.

## Rules

- Never silently convert `one_off` or `temporary` into `permanent`.
- A permanent change should never delete downstream one-off plans unless they are explicitly superseded.
- Surface dependency implications (e.g., earlier departure → earlier wake → earlier bedtime).
