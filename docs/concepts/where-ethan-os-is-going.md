# Where Ethan OS Is Going

## Today

Ethan OS is a public behavior layer for personal AI systems. It provides reusable workflows, skills, schemas, and validation. `ethan-life` is the private companion that owns all canonical personal state.

Right now the system is strongest at **vertical capabilities** — specialized behaviors for specific domains:

- **Guided Reading** — books, retention, recommendations.
- **Guided Learning** — courses, sessions, assessments.
- **Planning / Projects** — goals, tasks, schedules.
- **Finance** — accounts, transactions, budgets.
- **Health** — habits, metrics, notes.
- **Career** — evidence, resumes, interview prep.
- **Music** — collection, DJ sets, Spotify sync.

These capabilities are already connected by shared state and a common execution pattern. They are not silos.

## Next

The next stage is to make Ethan OS behave like one coherent personal AI operating system. That means adding **horizontal services** that every vertical capability can use:

```
Vertical capabilities
  (Guided Reading, Planning, Finance, ...)

Horizontal services
  - Context Engine
  - Universal Retrieval
  - Cross-Domain Reasoning
  - Temporal State
  - Review Orchestrator
  - Decision Intelligence
  - Workflow Orchestration
  - Bounded Proactive Assistance
  - Privacy & Permissions
```

The idea is simple:

> **Vertical capabilities provide specialized behavior. Horizontal services allow those capabilities to work together.**

## What the horizontal services will do

### Personal Context Engine

Given a request, assemble only the personal context needed to handle it well. Not a giant user-profile document — selective, explainable, domain-safe retrieval.

### Universal Personal Retrieval

Answer questions like "What have I learned about systems?" without the user needing to know which domain owns the answer. Initially deterministic; semantic/vector search may come later as an optional layer.

### Cross-Domain Reasoning

An idea from a book can inform a project plan. A completed course can become career evidence. A goal can pull in reading, learning, and schedule time. Relationships and shared context make this possible without hard-coding every pair of domains.

### Temporal State

State changes over time. The system should know what is current, historical, superseded, temporary, or in effect until a date. This is needed for preferences, schedules, and decisions.

### Decision Intelligence

Keep meaningful decisions: the context, options considered, chosen path, assumptions, and review date. Later the OS can ask, "How did that decision work out?"

### Review Orchestrator

One review workflow decides what actually needs attention: schedule, priorities, projects, learning, admin. It skips domains with nothing meaningful to review and surfaces cross-domain patterns.

### Priority Alignment / Goal-to-Reality Loop

Stated priorities should connect to projects, scheduled time, and actual completion. The OS can neutrally surface mismatches: "This project has been high priority for three weeks with no scheduled time."

### Workflow Orchestration

A real-world event may need multiple capabilities. An interview might update Career, Planning, Schedule, and Knowledge. Orchestration is composed, not monolithic.

### Workflow Evaluation / Quality Harness

Beyond schema validation, evaluate behavioral properties: does Guided Reading ask active recall before explaining? Does Sunday Planning protect free time? Does the resume skill avoid inventing experience?

### Bounded Proactive Assistance

Proactive nudges are opt-in and carefully bounded. The OS may surface an upcoming exam or a missing resume block, but it does not generate notifications freely. Relevance, urgency, confidence, and user preference gate every proactive suggestion.

## What stays the same

- `ethan-os` remains the public behavior layer.
- `ethan-life` remains the private canonical state.
- File-based, portable, inspectable storage remains the default.
- Privacy, provenance, and user control remain non-negotiable.
- Integrations remain projections, not authorities.

## What this is not

- A SaaS product or a single-app platform.
- A replacement for the user's judgment.
- A background agent that acts without explicit boundaries.
- A database-first or vector-first redesign of the existing architecture.

## Direction for the next implementation window

The highest-leverage foundations are:

1. **Context Engine contract** — a small, reusable schema and skill for selective context assembly.
2. **Cross-Domain Reasoning path** — use typed relationships and shared retrieval, documented as the standard way to connect domains.
3. **Review Orchestrator contract** — a small skill that decides which domain reviews are relevant.
4. **Decision record** — a minimal object for meaningful decisions.
5. **Horizontal architecture documentation** — make the vertical/horizontal distinction clear to builders and the AI runtime.

Larger pieces — vector search, autonomous proactive agents, desktop apps, mobile apps, package managers — remain Planned or Exploring.
