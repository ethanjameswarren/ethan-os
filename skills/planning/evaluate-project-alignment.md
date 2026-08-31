# Skill: evaluate-project-alignment

## Purpose

Evaluate a proposed or existing project against the active strategic objective to surface how it relates to long-term priorities. This skill informs project selection decisions without blocking project creation.

## Triggers

- "Should I take on this project?"
- "How does this project fit my five-year plan?"
- "Is this worth my time?"
- Creating a new `planning.project` when a strategic objective is active.

## Input

- The project (proposed or existing) with its description, goals, and expected outcomes.
- The active strategic objective's `decision_criteria` (from the linked career goal).
- The active milestone roadmap's current horizon expectations.

## Sequence

### 1. Load strategic context

- Identify the active strategic objective (`long_term` planning goal with a linked career goal and milestone roadmap).
- Load the career goal's `decision_criteria` and `positioning_strategy`.
- Load the current milestone horizon from the roadmap.

### 2. Evaluate against decision criteria

- Check the project against each decision criterion from the career goal.
- For each criterion, note whether the project: advances it, is neutral, or works against it.

### 3. Classify alignment

Assign one of:

- **directly advances** — the project closes a gap in the current milestone horizon or explicitly advances a decision criterion.
- **indirectly supports** — the project builds a capability, relationship, or asset that will be useful for a future horizon, but is not the highest-leverage action for the current one.
- **neutral** — the project neither advances nor hinders the strategic objective. It may serve other valid life priorities (health, relationships, hobbies).
- **competes with** — the project consumes significant time or attention that would otherwise go to strategic-objective-aligned work, without producing comparable leverage.

### 4. Surface tradeoffs

- If classified as `neutral` or `competes with`, note what strategic-objective work would be displaced and whether that tradeoff is acceptable.
- If classified as `directly advances` or `indirectly supports`, note which milestone-horizon expectations it serves.

## Output

A concise evaluation containing:

- project title and description
- alignment classification
- decision criteria addressed (or not)
- milestone-horizon expectations served (or displaced)
- tradeoff summary
- recommendation (proceed / defer / reduce scope / reject), presented as a suggestion

## Rules

- Do not block project creation. Surface the tradeoff and let the user decide.
- Do not apply this skill to projects already classified as personal/reward (e.g., music, automotive, home). Those are valid life priorities and are evaluated differently.
- Do not penalize maintenance, health, or relationship projects. The strategic objective does not supersede basic life functioning.
- When no strategic objective is active, this skill is a no-op.

## Confirmation policy

- Read-only skill: no confirmation required to run.
- The user decides whether to proceed, defer, or reject the project.
