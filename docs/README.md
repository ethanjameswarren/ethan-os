# Ethan OS Documentation

This documentation is organized as a ladder. Each level explains more; none require you to read implementation files.

For the high-level product and capability roadmap, see [Ethan OS Roadmap](ROADMAP.md).

## Getting started

- [Create your own OS](getting-started/create-your-own-os.md)
- [Updating your OS](getting-started/updating-your-os.md)

## How to read this repo

```
README
  → concepts        (what it is, why, principles, architecture)
    → capabilities  (what it can do)
      → workflows   (how a major capability behaves end-to-end)
        → architecture (technical design)
          → runtime / workflows / skills / schemas (implementation)
```

If you are new, start at the top and stop when you have enough detail. If you are debugging a workflow, you will end up at the bottom.

## For visitors and users

### Concepts

- [What is Ethan OS?](concepts/what-is-ethan-os.md)
- [Vision](VISION.md) — what Ethan OS is trying to become
- [Core principles](concepts/principles.md)
- [High-level architecture](concepts/architecture-overview.md)
- [Project naming and attribution](project-naming.md)

### Featured workflows

These are the most concrete ways to see Ethan OS in action:

- [Guided Reading](workflows/guided-reading.md)
- [Tailored Resume](workflows/tailored-resume.md)
- [Monthly Financial Review](workflows/monthly-financial-review.md)
- [Daily Schedule](workflows/daily-schedule.md)
- [DJ Set Building](workflows/music.md)

### Capabilities

| capability | description | human workflow |
|------------|-------------|----------------|
| [Guided Reading](capabilities/guided-reading.md) | Read and talk; the OS tracks progress, captures ideas, schedules retention, and recommends next reads. | [workflow](workflows/guided-reading.md) |
| [Knowledge & Learning](capabilities/knowledge.md) | Capture, connect, summarize, and review ideas from books, articles, conversations, and experience. | [workflow](workflows/knowledge.md) |
| [Planning & Projects](capabilities/planning.md) | Turn goals into projects and tasks; review what is happening next. | [workflow](workflows/planning.md) |
| [Finance](capabilities/finance.md) | Log transactions, track budgets, plan debt payoff, manage income/expenses/goals, allocate cash flow, and run financial reviews. | [workflow](workflows/finance.md) |
| [Health & Habits](capabilities/health.md) | Track habits, metrics, and medical notes. | [workflow](workflows/health.md) |
| [Career](capabilities/career.md) | Capture evidence, tailor resumes, prepare interviews. | [workflow](workflows/career.md) |
| [Music / DJ Workflows](capabilities/music.md) | Manage a collection, build sets, print labels, sync to Spotify. | [workflow](workflows/music.md) |
| [Schedule Planning](capabilities/schedule-planning.md) | Maintain a baseline schedule, adapt it with overrides, and generate weekly plans. | [workflow](workflows/schedule-planning.md) |

### Workflows

- [Guided Reading](workflows/guided-reading.md)
- [Tailored Resume](workflows/tailored-resume.md)
- [Monthly Financial Review](workflows/monthly-financial-review.md)
- [Daily Schedule](workflows/daily-schedule.md)
- [Build a DJ set](workflows/music.md)
- [Capture a learning note](workflows/knowledge.md)
- [Plan your week](workflows/planning.md)
- [Weekly health review](workflows/health.md)
- [Schedule your week](workflows/schedule-planning.md)

## For builders and contributors

- [Technical architecture](architecture/overview.md)
- [Runtime bootstrap](architecture/runtime.md)
- [Instruction precedence](architecture/instruction-precedence.md)
- [Relationship model](architecture/relationships.md)
- [Schema registry](architecture/schema-registry.md)
- [History strategy](architecture/history.md)
- [Integration boundaries](architecture/integration-boundaries.md)
- [Artifact design philosophy](architecture/design-philosophy.md)

## For the runtime / AI

- [`entrypoint/ethan-os.md`](../entrypoint/ethan-os.md)
- [`runtime/`](../runtime/)
- [`workflows/`](../workflows/)
- [`skills/`](../skills/)
- [`instructions/`](../instructions/)
- [`schemas/`](../schemas/)
