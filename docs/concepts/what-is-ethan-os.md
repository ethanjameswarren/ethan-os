# What is Ethan OS?

Ethan OS is a reusable behavior layer for personal AI systems.

It provides the instructions, workflows, skills, schemas, and validation that turn a chat into a persistent, structured personal system. You talk naturally; Ethan OS decides what to do, performs the work, and saves the result in a standard form.

The actual data lives in a separate, private repository called `ethan-life`. Ethan OS is public because it contains no personal information — only generic behavior.

## The problem

A typical AI conversation looks like this:

```
conversation → useful response → nothing is saved
```

A few sessions later, the insight, decision, or connection is gone. Even when notes are kept, they live in different apps, formats, and search silos. The AI starts from zero every time.

Ethan OS makes conversation durable:

```
conversation → workflow → structured output → persistent state → future retrieval/use
```

The same idea captured while discussing a book can later appear in a summary, a review question, a project plan, or a recommendation for what to read next.

## What Ethan OS provides

- **Workflows** for common personal tasks: reading, planning, finance, health, career, music, and more.
- **Skills** that handle specific behaviors: classify intent, extract ideas, schedule reviews, build DJ set candidates, assess resumes.
- **Schemas** that define what saved objects look like, so different workflows can share and connect data.
- **Validation** that checks outputs before they are written, so the system stays consistent.
- **Policies** for provenance, privacy, spoiler protection, confirmation, and source/belief separation.

## What `ethan-life` provides

`ethan-life` is the private companion repository. It owns all canonical personal state:

- captures (raw inputs)
- sources (books, articles, people, experiences)
- ideas (durable reusable insights)
- summaries (personal syntheses)
- reviews (items flagged for reconsideration)
- state files (active reading, retention queues, project status)

Ethan OS reads from and writes to `ethan-life`. It never treats integrations like Notion or Spotify as the source of truth.

## Why this separation matters

1. **Privacy.** Personal data never has to live in a public repository.
2. **Portability.** You can replace, move, or archive `ethan-life` without changing the behavior system.
3. **Generality.** The same `ethan-os` logic can run against different private repositories or different users.
4. **Inspectability.** Your canonical state is plain Markdown and YAML, readable outside any AI tool.

## Examples

### Guided Reading

You say, "I finished pages 1-15 of Thinking in Systems." Ethan OS asks what stood out, discusses the idea with you, saves a structured session note, and schedules a retention review. When you finish the book, it synthesizes your actual sessions and notes into a personal summary.

### Planning

You say, "I want to get better at system design this year. I freeze up in those interviews." Ethan OS turns that into a goal with success criteria, breaks it into a project with milestones, and creates the first task.

### Music / DJ workflows

You say, "Build me a 90-minute hypnotic techno set around 140 BPM from records I've rated highest." Ethan OS reads your collection state, selects candidates, and produces a set you can audition, refine, export to Spotify, and print record labels for.

## What it is not

- It is not a chatbot that starts fresh every session.
- It is not a single app with a hardcoded UI.
- It is not a replacement for your judgment; it organizes and surfaces information so your judgment can work with continuity.
- It is not a black box; saved state is plain text and structured by schemas.

## How to think about it

Ethan OS is a personal operating system whose programs are workflows, whose files are schemas and state, and whose interface is natural language. The goal is continuity: the system should remember what matters, connect it, and bring it back at the right time, while you remain in control.

For where the project is today and where it is headed, see the [Roadmap](../ROADMAP.md).

## Next

- [Core principles](principles.md)
- [High-level architecture](architecture-overview.md)
- [Guided Reading capability](../capabilities/guided-reading.md)
