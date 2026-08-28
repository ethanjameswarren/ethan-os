# Beta Feedback / Friction Tracking

During Beta use, you can simply tell Ethan OS when something feels wrong or right. Ethan OS records it as a structured `core.friction-log` object in your private `ethan-life` repository.

## Examples

> "That was annoying; you already knew that."  
> "That review was too long."  
> "You should have connected this to my goal."  
> "That was actually really good."

## What happens

1. Ethan OS infers the feedback type and severity from your words.
2. It attaches current runtime context (workflow, skill, capability, context refs) without asking you.
3. It stores the entry in `ethan-life/domains/system/friction/`.
4. If the same problem is already open, it records another occurrence instead of duplicating.

## Expected vs observed

Each entry keeps these distinct:

- **Expected:** what you reasonably thought would happen.
- **Observed:** what actually happened.

This distinction is what makes later fixes and evaluation cases precise.

## Review

Ask:

- "What has been annoying lately?"
- "What should we fix next?"
- "Show repeated problems."

Ethan OS groups by capability, type, root cause, severity, and repetition, then surfaces the most important patterns.

## From friction to evaluation

A repeated pattern can become an evaluation expectation:

> "If exactly one active reading source exists, Guided Reading should not ask the user to identify it."

No GitHub issues, Jira, or dashboards are created automatically.

## Privacy

- Actual entries stay in `ethan-life` and are never published.
- Any public example requires your explicit approval and must be sanitized.

## Related files

- Schema: `schemas/core/friction-log.schema.yaml`
- Capture skill: `skills/core/capture-friction.md`
- Capture workflow: `workflows/core/capture-friction.md`
- Review workflow: `workflows/core/review-friction-log.md`
- Logic: `scripts/core/friction_log.py`
- Validation matrix: `ethan-life/domains/system/validation-matrix.yaml` + `scripts/core/validation_matrix.py`
