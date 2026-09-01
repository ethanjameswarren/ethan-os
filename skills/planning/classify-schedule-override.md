# Skill: classify-schedule-override

## Purpose

Classify a schedule override as evidence of an exception, a preference, a baseline friction, or insufficient information.

## Input

- Natural-language change request.
- `target_block` (planned) and `block` (actual), if available.
- Recent override history for the same target, if available.

## Steps

1. Infer the override reason from the user's words.
2. Choose a `reason_category` from the `planning.schedule-override` schema:
   - `unusual_event`, `travel`, `appointment`, `concert`, `sporting_event`, `illness`, `family`, `work` for exceptions.
   - `preference` or `friction` for behavioral signals.
   - `other` or `unknown` when unclear.
3. Set `classification`:
   - `exception` for clearly temporary, one-off circumstances.
   - `preference` when the user or history shows a consistent voluntary change.
   - `friction` when the schedule appears unrealistic or repeatedly conflicts with real constraints.
   - `unknown` when there is not enough evidence.
4. Infer `change_effect` by comparing `target_block` to `block`:
   - `moved` — same label, different start/end.
   - `shortened` — same label, shorter duration.
   - `extended` — same label, longer duration.
   - `replaced` — different label.
   - `cancelled` — the planned block is removed.
   - `added` — no planned block was targeted.
5. Fill the `classification_reason` with a one-sentence justification.

## Output

- `classification`
- `classification_reason`
- `reason_category`
- `change_effect`
- `user_note` (optional)

## Rules

- Do not ask the user to fill a form. Infer these fields from the conversational request.
- One clearly unusual event is an exception. Two similar exceptions close together are still exceptions. Three or more may begin to look like a preference; escalate to `skills/planning/analyze-schedule-overrides.md`.
- Do not classify a single override as `friction` unless the reason explicitly says the plan is unrealistic.
- Preserve the original override text in `user_note` if it does not fit the structured fields.
