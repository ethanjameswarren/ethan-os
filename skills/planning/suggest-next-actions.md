# Skill: suggest-next-actions

## Purpose

Identify what is actionable now across active Goals, Projects, and Tasks, and surface planning items that need attention.

## Triggers

- "What should I work on today?"
- "I have two free hours. What should I do?"
- "What should I work on at work?"
- "What's the highest-value thing I can do next?"

## Input

- all Goal objects with `status: active`
- all Project objects with `status: planned` or `status: active`
- all Task objects with `status` other than `done` or `dropped`
- relevant career context, active strategic objective and milestone horizon, learning programs, decisions, reviews, weekly plan, schedule constraints, and user-stated available time/context

## Identify

- **unblocked tasks**: `status: todo` or `in_progress` tasks with no stated blocker
- **blocked tasks**: `status: blocked`, and whether the blocker still applies
- **stale projects**: `status: active` projects with no task activity or milestone progress in a while, based on `updated_at`
- **goals without momentum**: `status: active` goals with no active project or task linked to them
- **completed milestones not reflected**: milestones that appear done based on linked task completion but are not yet marked `done` on the Project
- **strategic objective gaps**: if a strategic objective is active (see `instructions/policies/configurable/strategic-objective-alignment.md`), check the current milestone horizon's expectations against active projects, tasks, and evidence. Surface any horizon expectation that has no linked active execution.

## Work-type distinctions

Apply every label that materially describes a candidate; the labels are non-exclusive:

- **maintenance work** — preserves an existing system, responsibility, relationship, or level of performance without materially expanding it
- **necessary work** — satisfies a real commitment, deadline, dependency, risk, or obligation; maintenance may also be necessary
- **skill-building work** — deliberately develops a capability through practice, feedback, or application
- **career-advancing work** — strengthens role performance, positioning, demonstrable evidence, scope, or ownership
- **leverage-building work** — makes future work easier, faster, broader, or less dependent on Ethan's repeated effort
- **asset-creating work** — produces a durable reusable artifact such as a tool, system, template, dataset, process, library, or publishable work
- **compounding work** — produces benefits that accumulate through reuse, feedback, distribution, relationships, data, or repeated learning

Do not force unsupported labels. State uncertainty when the available objects do not establish a work type.

## Ranking

Use the existing task `priority`, goal/project relationships, strategic-objective alignment policy, deadlines, context bundle, schedule, and career/learning evidence as inputs. Do not create or calculate a separate numeric score.

1. Filter to actions that are unblocked and feasible in the user's available time, work context, tools, and energy. If duration is unknown, say so rather than pretending the fit is known.
2. Protect genuine commitments by considering deadline proximity, consequences, dependencies, and promises to other people. A deadline raises importance but does not automatically win.
3. Compare remaining candidates qualitatively across business impact, career impact, strategic relevance, learning value, evidence created, durable/reusable assets, usefulness to other people, increased scope or ownership, compounding value, opportunity cost, effort, and available time.
4. Prefer actions that unlock multiple valuable follow-on actions, remove a binding dependency, combine delivery with learning/evidence/asset creation, or create reusable value for others.
5. Treat maintenance as capacity-consuming but legitimate. Surface it first only when deferral creates meaningful risk or violates a commitment; otherwise identify it as useful but lower leverage and offer a higher-leverage alternative.
6. Use strategic objective gaps, goals without momentum, blocked items, and stale projects as diagnostic signals, not as an automatic ranking order. When a strategic objective is active, apply its configured `weight_boost` without allowing it to override hard commitments or user context automatically.
7. Break a large high-value candidate into a concrete action that fits the available time instead of replacing it with a smaller low-value task.

## Rules

- Do not close, reprioritize, or change status of any object; only surface findings.
- Distinguish genuinely stale items from those that are intentionally paused (`on_hold` goals, `blocked` tasks with an active blocker).
- Distinguish facts from inference and ground material claims in the loaded context.
- Do not claim business impact, career impact, reuse, ownership, or compounding value without supporting evidence.
- If a necessary commitment dominates, say why. If a lower-leverage task is still recommended, name the constraint that makes it the right choice now.

## Output

Return a short ranked recommendation, not an undifferentiated task dump. For each leading candidate include:

- object ID and concrete action
- applicable work-type labels
- why it is valuable now, including the strongest supported impact/leverage factors
- deadline, dependency, feasibility, or opportunity-cost considerations
- what it unlocks, when applicable

Lead with one explicit recommendation and rationale, using language such as "Do X first because it unlocks Y and Z." When relevant, explicitly say "This task is useful but low leverage" and provide a higher-leverage alternative. Include at most 3 alternatives unless the user asks for a broader list.

## Confirmation policy

- Read-only skill: no confirmation required to run. Any resulting status change must go through `workflows/core/revise.md`.
