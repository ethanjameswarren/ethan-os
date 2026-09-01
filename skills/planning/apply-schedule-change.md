# Skill: apply-schedule-change

## Purpose

Interpret a schedule change request and apply it at the correct scope without collapsing one-off, temporary, and permanent changes.

## Input

- Natural language change request.
- Active `planning.baseline-schedule`.
- Existing `planning.schedule-override` objects.
- Target date or recurrence pattern, if known.
- Target weekly plan, if the change affects the current week.

## Determine scope

Infer scope from the user's language:

- **one_off**: "this week", "Thursday", "tomorrow", "on the 15th", "just once".
- **temporary**: "for the next two weeks", "until the end of the month", "while I'm on call".
- **permanent**: "from now on", "every Wednesday", "make it the new normal".

If the scope is ambiguous and materially affects the baseline, ask for clarification.

## Capture structured evidence

Before creating the override, populate every `planning.schedule-override` object with the structured evidence fields required for behavioral learning:

1. `target_block` — the original planned block (`label`, `day_of_week`, `start_time`, `end_time`, `category`, `source`).
2. `block` — the actual block that happened or will happen (`label`, `day_of_week`, `start_time`, `end_time`, `category`, `source`).
3. `change_effect` — infer from `target_block` vs `block` (`moved`, `shortened`, `extended`, `replaced`, `cancelled`, `added`).
4. `reason` and `reason_category` — capture the user's stated reason.
5. `classification` — run `skills/planning/classify-schedule-override.md` to produce `exception`, `preference`, `friction`, or `unknown`.
6. `classification_reason` and `user_note` — preserve the user's own words.
7. `provenance` — record agent version, source, and the related weekly-plan or baseline IDs.

If the user's request is ambiguous, make the smallest reasonable inference rather than asking for a form.

## Apply by scope

### one_off

1. Create a `planning.schedule-override` with `scope: one_off` and the specific date.
2. Populate the structured evidence fields as described above.
3. Generate or update the weekly plan for the affected week only.
4. Do not modify the baseline schedule.

### temporary

1. Create a `planning.schedule-override` with `scope: temporary`, `start_date`, and `end_date`.
2. Populate the structured evidence fields.
3. Generate or update weekly plans for each affected week.
4. Do not modify the baseline schedule.

### permanent

1. Confirm explicitly before updating the baseline schedule.
2. Update the `planning.baseline-schedule` recurring blocks.
3. Mark the override as `superseded` or remove it if it is fully absorbed.
4. Record the accepted change with the evidence that justified it for later validation.
5. Optionally regenerate the current-week plan using the updated baseline.

## Behavioral learning trigger

After saving any override, if the same block has accumulated several recent overrides, run `workflows/planning/analyze-schedule-overrides.md`. Do not block the current change on this; run it in the background or mention it if it is relevant.

## Output

- New or updated `planning.schedule-override` with structured evidence.
- Updated baseline schedule if scope is permanent.
- Updated weekly plan for the affected week.
- Classification (`exception`, `preference`, `friction`, or `unknown`).
- Clear statement of what changed and what did not.
- Optionally, a schedule-drift analysis if the same block has a pattern.

## Rules

- Never silently convert `one_off` or `temporary` into `permanent`.
- A permanent change should never delete downstream one-off plans unless they are explicitly superseded.
- Surface dependency implications (e.g., earlier departure → earlier wake → earlier bedtime).
