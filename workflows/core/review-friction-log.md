# Workflow: review-friction-log

## Purpose

Periodically review captured Beta friction, identify patterns, and turn the strongest repeated problems into evidence for fixes or evaluation cases.

## Triggers

- "Review my Ethan OS friction."
- "What has been annoying lately?"
- "What should we fix next?"
- "Show repeated problems."
- "What's the biggest problem with Ethan OS right now?"
- "Which workflow causes the most friction?"

## Steps

1. Load `core.friction-log` objects from `ethan-life/domains/system/friction/`.
2. Run `scripts/core/friction_log.py` to group by capability, feedback type, root-cause area, severity, and repetition.
3. Count open vs resolved.
4. Surface the highest-severity open issues first.
5. Highlight repeated patterns (occurrence_count > 1).
6. For the strongest repeated pattern, generate a draft evaluation expectation using `scripts/core/friction_log.py`.
7. Optionally mark an entry as `triaged` or `planned` if the user decides to act on it. Status changes go through `workflows/core/revise.md`.
8. Return a concise summary.

## Output

- open issue count and resolved count
- top high-severity/repeated issues
- grouped pattern summary
- draft evaluation expectation for any repeated pattern

## Rules

- Keep product/system maintenance separate from Sunday life planning unless the user explicitly asks to mix them.
- Do not surface every low-severity annoyance.
- Do not publish personal examples without explicit user approval.
- Positive signals can be included if the user asks, but are kept separate from problem reporting.
