# Skill: capture-friction

## Purpose

Capture a single, low-friction Beta feedback statement and turn it into a `core.friction-log` object. The user should be able to mention a problem in normal conversation and keep talking.

## Triggers

- "That was annoying."
- "You already knew that."
- "You should already know that."
- "Log this as friction."
- "That was wrong."
- "That workflow is too long."
- "That should have connected to my career goal."
- "Save this as Beta feedback."
- "That was actually really good."
- "That was exactly right."
- "Good, you didn't ask me anything unnecessary."

Any statement about how Ethan OS behaved can be treated as friction or a positive signal.

## Inputs

- user statement
- runtime context (current intent, workflow, skill, capability, domain, context bundle, object refs)
- existing open `core.friction-log` objects in `ethan-life/domains/system/friction/`

## Outputs

- a concise acknowledgment
- a saved `core.friction-log` object
- the entry ID

## Steps

1. Identify whether the statement is positive or negative.
2. Extract:
   - a one-sentence `summary`
   - `user_expectation` if the user expresses what should have happened
   - `observed_behavior` if the user says what actually happened
3. Infer `feedback_type` from the user's words. Use `other` when nothing fits.
4. Infer `severity` from the type and phrasing. Do not ask the user for a severity rating.
5. Apply the current runtime context to `affected_capability`, `affected_workflow`, `affected_skill`, `relevant_domain`, `context_refs`, and `context_bundle_id`. Do not ask for workflow/capability if they are already known from context.
6. Infer a tentative `root_cause_inferred` from the feedback type. Mark it as inferred, not confirmed.
7. Check for a substantially similar open entry (same `feedback_type`, `affected_capability`, and `affected_workflow`). If one exists, update it: increment `occurrence_count`, append the date, and add the new context refs.
8. If no similar open entry exists, create a new `core.friction-log` object in `ethan-life/domains/system/friction/`.
9. Respond briefly and continue the previous conversation.

## Distinctions

- **Expected:** what the user reasonably thought would happen.
- **Observed:** what the OS actually did.
- Keep these separate even when the user blurs them in one sentence.

## Rules

- Do not turn feedback capture into another interview.
- Do not ask: "What workflow was this?", "What capability was this?", or "What severity is this?" unless the context is genuinely missing.
- Preserve the original user phrasing in `source_phrase` or `description`.
- Store only `ethan-life/domains/system/friction/`. Never publish actual entries to public docs, roadmaps, or GitHub.
- Positive signals are captured the same way, with `is_positive: true` and `feedback_type: worked_well`.
- If the same open problem is reported again, update the existing entry rather than duplicating.
