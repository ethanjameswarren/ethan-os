# High-Level Architecture

Ethan OS is split into three conceptual layers: the behavior system, the private state, and optional downstream presentations.

```
         ┌─────────────┐
         │    User     │
         │  (chat,     │
         │   voice,    │
         │   scripts)  │
         └──────┬──────┘
                │
                │ natural language input
                ▼
  ┌──────────────────────────────────────┐
  │              Ethan OS                  │
  │                                        │
  │  ┌─────────────┐    ┌──────────────┐  │
  │  │   Intent    │───▶│   Domain &   │  │
  │  │  understanding   │   workflow   │  │
  │  └─────────────┘    │   selection  │  │
  │  ┌─────────────┐    └──────────────┘  │
  │  │   Skills    │         │              │
  │  │  & policies │◀────────┘              │
  │  └─────────────┘                       │
  │  ┌─────────────┐    ┌──────────────┐   │
  │  │   Context   │───▶│     Work     │   │
  │  │   (state)   │    │   performed  │   │
  │  └─────────────┘    └──────────────┘   │
  │                            │           │
  │  ┌─────────────┐    ┌──────┴───────┐   │
  │  │  Validation │◀───│   Output     │   │
  │  │             │    │   objects    │   │
  │  └─────────────┘    └──────────────┘   │
  └─────────────┬──────────────────────────┘
                │ structured objects
                ▼
  ┌──────────────────────────────────────┐
  │            ethan-life                │
  │         canonical state              │
  │                                      │
  │  sources, ideas, summaries,          │
  │  captures, reviews, state files,     │
  │  projects, tasks, habits, etc.       │
  └─────────────┬──────────────────────────┘
                │ optional projection
                ▼
  ┌──────────────────────────────────────┐
  │    Downstream interfaces/adapters    │
  │                                      │
  │  Notion, Spotify, future UI/API        │
  └──────────────────────────────────────┘
```

## Responsibilities

### Ethan OS (public behavior)

- Understands what the user is asking for.
- Selects the right domain and workflow.
- Loads relevant policies, skills, and context.
- Performs the work.
- Validates the output against schemas.
- Writes the result to `ethan-life`.

`ethan-os` contains no personal data. It is safe to publish, fork, or inspect.

### ethan-life (private state)

- Owns all canonical personal information.
- Stores objects as plain Markdown and YAML.
- Is the only place status, progress, and history are authoritative.

`ethan-life` contains no behavior logic. It only reacts to what `ethan-os` writes.

### ethan-notion and other integrations (optional projections)

- `ethan-notion` defines how `ethan-life` state can be projected into a Notion workspace.
- Live Notion updates happen only after `ethan-life` state is resolved.
- Spotify, future APIs, or UI layers work the same way: they read from or reflect `ethan-life`, they do not own it.

## Repository separation

| repository | visibility | owns |
|------------|------------|------|
| `ethan-os` | public | behavior, schemas, workflows, skills, policies, validation, docs, tests |
| `ethan-life` | private | captures, sources, ideas, summaries, state, personal context |
| `ethan-notion` | private | Notion database mappings and sync architecture |

## Execution flow

1. The user provides input.
2. Ethan OS classifies intent and picks a workflow.
3. It loads the relevant skills, policies, and context from `ethan-life`.
4. It performs the work.
5. It validates any new or changed objects.
6. It writes the validated result to `ethan-life`.
7. If needed, it updates downstream presentation layers like Notion.
8. It returns a concise summary.

This flow is the same regardless of domain. Whether the user is reading a book, logging a transaction, or building a DJ set, the pattern is identical.

## Why this shape

- **Continuity.** Because `ethan-life` is persistent and structured, future workflows can build on past state.
- **Privacy.** Personal data never has to be in the public repo.
- **Generality.** The behavior layer can be reused by different people or different private repositories.
- **Inspectability.** State is plain text; behavior is documented; there is no hidden database schema.
- **Testability.** `ethan-os` can be validated against fake demo fixtures without touching real personal data.

## What this document does not cover

For the technical details of bootstrap, intent routing, instruction precedence, schema registry, and validation, see the [technical architecture](../architecture/overview.md) docs.

## Next

- [Core principles](principles.md)
- [Guided Reading capability](../capabilities/guided-reading.md)
