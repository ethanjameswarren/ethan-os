# Planning & Projects

## What it does

Turn goals into concrete plans, track projects and tasks, and surface what you should do next without reorganizing lists by hand.

## Why it exists

Goals become vague unless they are broken into trackable pieces. Ethan OS keeps the link between a goal, the projects serving it, and the next actionable task, so you can focus on doing rather than on reorganizing.

## What you do

- State a goal or intention.
- Optionally break it into a project with milestones.
- Add tasks as they come up.
- Ask "what should I do next?" or request a weekly review.
- Mark things done, blocked, or dropped when you update the system.

## What Ethan OS does

- Stores goals with success criteria so they can be reviewed meaningfully.
- Creates projects and milestones only when a goal needs multiple coordinated steps.
- Links every task back to its project or goal.
- Surfaces unblocked next actions, blocked items, stale projects, and goals without momentum.
- Distinguishes maintenance, necessary, skill-building, career-advancing, leverage-building, asset-creating, and compounding work when recommending what to do next.
- Balances deadlines with impact, strategic relevance, learning, evidence, reuse, ownership, compounding value, opportunity cost, and available time instead of treating urgency as value.
- Runs a weekly review of your active planning landscape.
- Projects authoritative cross-domain goals into planning without duplicating their full strategy, using explicit synchronization rules.
- Detects strategic drift and milestone gaps and can export plans to ICS or explicitly write selected blocks to Google Calendar.
- Treats repeated schedule overrides as behavioral evidence and uses them to propose baseline corrections through `workflows/planning/analyze-schedule-overrides.md`.
- Does not silently close, reprioritize, change status, or write to an external calendar without your confirmation.

## Key ideas

- **Goals need success criteria.** A goal without a way to know it is achieved cannot be reviewed.
- **Not every goal needs a project.** Small goals can link directly to one or two tasks.
- **Tasks are linked.** A standalone to-do is allowed, but it is flagged as a candidate for goal alignment during review.
- **Review is read-only until you confirm.** The system surfaces findings; it does not reorganize your plan automatically.

## Example interaction

> **You:** "I want to finish my home office by the end of the month."  
> **OS:** "What does 'finished' mean here?"  
> **You:** "Desk assembled, cables managed, and the monitor mounted."  
> **OS:** "Got it. I'll create a goal with those three success criteria and a project with milestones for each."

## What gets saved

- **Goal** — the outcome, horizon, success criteria, and status.
- **Project** — the plan, milestones, and linked goal.
- **Task** — the concrete action, status, priority, and due date.
- **Review findings** — prioritized suggestions surfaced during weekly review.

## Important behaviors

- Do not create projects for goals that fit in a single task.
- Do not close or drop tasks without explicit confirmation.
- Distinguish genuine staleness from intentionally paused work.
- Link every project and task back to the goal it serves.

## Related workflows

- [Plan your week](../workflows/planning.md)

## Technical implementation

- Workflows: `workflows/planning/`
- Skills: `skills/planning/`
- Schemas: `schemas/domains/planning/goal.schema.yaml`, `project.schema.yaml`, `task.schema.yaml`
