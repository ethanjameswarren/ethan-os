# Skill: suggest-next-actions

## Purpose

Identify what is actionable now across active Goals, Projects, and Tasks, and surface planning items that need attention.

## Input

- all Goal objects with `status: active`
- all Project objects with `status: planned` or `status: active`
- all Task objects with `status` other than `done` or `dropped`

## Identify

- **unblocked tasks**: `status: todo` or `in_progress` tasks with no stated blocker
- **blocked tasks**: `status: blocked`, and whether the blocker still applies
- **stale projects**: `status: active` projects with no task activity or milestone progress in a while, based on `updated_at`
- **goals without momentum**: `status: active` goals with no active project or task linked to them
- **completed milestones not reflected**: milestones that appear done based on linked task completion but are not yet marked `done` on the Project

## Rules

- Do not close, reprioritize, or change status of any object; only surface findings.
- Distinguish genuinely stale items from those that are intentionally paused (`on_hold` goals, `blocked` tasks with an active blocker).
- Rank suggestions by: goals with no momentum first, then blocked items worth revisiting, then unblocked next actions.

## Output

A prioritized list of findings, each with:

- object ID and title
- why it was surfaced
- suggested next step (informational only — not auto-applied)

## Confirmation policy

- Read-only skill: no confirmation required to run. Any resulting status change must go through `workflows/core/revise.md`.
