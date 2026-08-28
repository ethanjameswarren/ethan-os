# Ethan OS

A reusable behavior layer for personal AI systems.

Ethan OS turns natural-language conversation into structured, persistent, connected personal state. You talk. It remembers, organizes, and surfaces what matters.

It is designed to run alongside a private companion repository, `ethan-life`, which owns all actual personal data. `ethan-os` is the public, generic system: workflows, skills, schemas, policies, validation, and documentation.

## What problem it solves

Most AI conversations are isolated sessions. Useful context, decisions, and insights either disappear or become scattered across chats, notes, and apps.

Ethan OS makes conversation durable:

```
conversation → workflow → structured output → persistent state → future retrieval/use
```

A note about a book, a project plan, a health log, or a DJ set all flow through the same system. The same idea captured from a conversation can later appear in a book summary, a resume bullet, or a weekly review without being copied by hand.

## What makes it different

- **Behavior and data are separate.** `ethan-os` is public and generic. `ethan-life` is private and personal. The boundary is enforced by design, not by configuration.
- **Plain Markdown and YAML.** No required database, cloud service, or mobile app. Data stays in files you can inspect, version, and move.
- **Structured, not just summarized.** Inputs become typed objects with relationships, provenance, and validation rather than free-form transcripts.
- **Continuity.** Later conversations can build on earlier ones because prior state is canonical and retrievable.
- **Human control.** The system asks before important changes and does not silently overwrite useful history.

## What it can do

- **Guided Reading** — read and talk about books; track progress, capture ideas, schedule retention, recommend next reads, and respect spoiler boundaries.
- **Knowledge & Learning** — capture ideas from books, articles, podcasts, conversations, and experience; connect them; summarize; review.
- **Planning** — turn goals into projects and tasks; review what is happening next.
- **Finance** — log transactions and track budgets.
- **Health** — track habits, metrics, and medical notes.
- **Career** — capture evidence, analyze roles, build tailored resumes, prepare interviews.
- **Music / DJ Workflows** — manage a collection, build DJ sets, print record labels, sync to Spotify.

## Example interaction

> **You:** "I finished pages 1-15 of Thinking in Systems."  
> **OS:** "Before we dig in, what do you remember standing out?"  
> *(you answer)*  
> **OS:** "That connects to something you noticed last month about labor planning. Want me to save it as a durable idea?"  
> *(conversation continues, a session note is saved, a retention item is scheduled)*

## Conceptual architecture

```
┌─────────────┐
│    User     │
└──────┬──────┘
       │ natural language
       ▼
┌──────────────────────────────────┐
│           Ethan OS                 │
│  intent → workflow → skills → work │
└──────┬───────────────────────────┘
       │ structured output
       ▼
┌──────────────────────────────────┐
│          ethan-life              │
│   canonical personal state       │
└──────┬───────────────────────────┘
       │ optional projection
       ▼
┌──────────────────────────────────┐
│   Notion, Spotify, future UIs    │
└──────────────────────────────────┘
```

`ethan-os` decides what to do. `ethan-life` owns what is true. Integrations are read-only or downstream projections; they are never the source of truth.

## Repository separation

| repository | purpose | visibility |
|------------|---------|------------|
| `ethan-os` | behavior, schemas, workflows, skills, validation, docs, tests | public |
| `ethan-life` | captures, sources, ideas, state, personal context | private |
| `ethan-notion` | optional Notion presentation/sync architecture | private |

## Project status

Ethan OS is actively developed. Several capabilities are usable today, while newer workflows and documentation are being tested in real use.

See the [Roadmap](docs/ROADMAP.md) for capability readiness and planned direction.

## Make it yours

Ethan OS is designed to serve as an upstream foundation for personalized systems.

You can create your own downstream OS, give it its own identity, customize it freely, and continue adopting compatible Ethan OS improvements. Applicable license and attribution notices remain with downstream distributions.

- [Create your own OS](docs/getting-started/create-your-own-os.md)
- [Updating your OS](docs/getting-started/updating-your-os.md)
- [Project naming and attribution](docs/project-naming.md)

## License

Ethan OS is licensed under the [Apache License 2.0](LICENSE).

You may use, modify, and distribute it subject to the license. Downstream systems are encouraged, but they should use their own project identity rather than imply they are the official Ethan OS project. See [NOTICE](NOTICE) and [project naming guidance](docs/project-naming.md).

## Where to go next

- **New here?** Start with [What is Ethan OS?](docs/concepts/what-is-ethan-os.md).
- **Want to see a capability?** Read about [Guided Reading](docs/capabilities/guided-reading.md).
- **Want the lifecycle?** See the [Guided Reading workflow](docs/workflows/guided-reading.md).
- **Curious how it works under the hood?** See the [technical architecture](docs/architecture/overview.md).
- **Want to run it?** See the [entrypoint](entrypoint/ethan-os.md) and validation tests in `scripts/`.
