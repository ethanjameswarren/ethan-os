# Skill: suggest-habit-insights

## Purpose

Surface habit and medical items worth Ethan's attention.

## Input

- all Habit objects with `status: active`
- all Log Entry objects for the relevant period
- all Medical Note objects with `status: active` or `status: monitoring`

## Identify

- **broken streaks**: active habits whose `current_streak` recently dropped to zero
- **habits with no recent logs**: active habits with no Log Entry in a while relative to their `target_frequency`
- **follow-ups coming due**: Medical Notes with a `follow_up` that implies a near-term action
- **habits with strong momentum**: worth acknowledging, not just flagging problems

## Rules

- Do not change any Habit, Log Entry, or Medical Note; only surface findings.
- Rank findings by: overdue medical follow-ups first, then broken streaks tied to a goal, then other broken streaks, then habits with no recent logs.

## Output

A prioritized list of findings, each with:

- object ID and title
- why it was surfaced
- suggested next step (informational only — not auto-applied)

## Confirmation policy

- Read-only skill: no confirmation required to run. Any resulting change must go through `skills/health/log-metric.md`, `skills/health/capture-medical-note.md`, or `workflows/core/revise.md`.
