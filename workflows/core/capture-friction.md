# Workflow: capture-friction

## Purpose

Capture Beta usage friction or positive signals from a single user statement without interrupting normal use.

## Triggers

- "That was annoying."
- "You already knew that."
- "Log this as friction."
- "That was wrong."
- "That workflow is too long."
- "That should have connected to my goal."
- "That was actually really good."

## Steps

1. Classify intent as `capture-friction`.
2. Load `skills/core/capture-friction.md`.
3. Assemble current runtime context (intent, workflow, skill, capability, domain, context bundle, object refs).
4. Run `scripts/core/friction_log.py` to prepare the `core.friction-log` object, applying context and checking for open duplicates.
5. Run `skills/core/validate-object.md`.
6. Write the object to `ethan-life/domains/system/friction/` (new or updated duplicate).
7. Respond briefly and continue the previous conversation.

## Output

- `core.friction-log` ID
- brief acknowledgment
- continuation of the current task

## Confirmation policy

- Auto-execute. Feedback capture should not add friction of its own.
- If the input is ambiguous between `capture-friction` and `revise` or `capture`, prefer `capture-friction` when the statement is about OS behavior.
