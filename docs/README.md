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
- [Core principles](concepts/principles.md)
- [High-level architecture](concepts/architecture-overview.md)
- [Project naming and attribution](project-naming.md)

### Capabilities

| capability | description | human workflow |
|------------|-------------|----------------|
| [Guided Reading](capabilities/guided-reading.md) | Read and talk; the OS tracks progress, captures ideas, schedules retention, and recommends next reads. | [workflow](workflows/guided-reading.md) |
| Knowledge & Learning | Capture, connect, summarize, and review ideas from books, articles, conversations, and experience. | — |
| Planning | Turn goals into projects and tasks; review what is happening next. | — |
| Finance | Log transactions and track budgets. | — |
| Health | Track habits, metrics, and medical notes. | — |
| Career | Capture evidence, tailor resumes, prepare interviews. | — |
| Music / DJ Workflows | Manage a collection, build sets, print labels, sync to Spotify. | — |

The remaining capability docs are in progress. Domain overviews are still available in [`docs/domains/`](domains/).

### Workflows

- [Guided Reading workflow](workflows/guided-reading.md)

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
