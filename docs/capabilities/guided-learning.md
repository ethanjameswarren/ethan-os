# Guided Learning

## What it does

Ethan OS helps you learn courses, certifications, and structured programs the same way it helps you read books: by tracking what you are learning, asking for recall, capturing durable ideas, and scheduling review — without turning learning into note-taking homework.

It supports:

- College and university courses
- LinkedIn Learning, Coursera, Udemy, and other online courses
- Certification programs
- Workplace training
- Self-study curricula

## Why it exists

Most learning materials generate a stream of notes and highlights that quickly disappear. Guided Learning turns that stream into durable, connected knowledge while adapting to the structure of each format.

The goal is not to collect every detail. The goal is to capture what you would want to remember and use later, and to support the specific shape of each kind of program.

## What you do

- Say what you are starting, continuing, or finishing.
- Answer a few conversational questions about what you remember and what stood out.
- Ask for review, weak-area help, or exam prep.
- Optionally provide a syllabus, module list, or exam objectives.

That is it. The OS handles structure, retention, progress, and study support.

## What Ethan OS does

- Creates a `knowledge.learning-program` for each course or program.
- Adapts questions and retention to the course type:
  - University: professor emphasis, lecture connections, weak concepts, exams.
  - Online: main concepts, practical application, module progress.
  - Certification: distinguishing concepts, scenarios, weak domains, mock-exam history.
- Begins sessions with active recall before explanation.
- Captures durable takeaways, meaningful mistakes, and real-world applications.
- Connects course ideas to your existing knowledge, projects, and work.
- Schedules important ideas for review.
- Builds targeted, user-grounded review for upcoming assessments.
- Produces a personal synthesis when you finish a program.
- Integrates with Planning and Sunday Weekly Planning for study time.

## Key ideas

### Format-adaptive, not one-size-fits-all

University courses, online courses, and certifications have different structures. Guided Learning does not force a university shape onto a LinkedIn Learning course or invent academic concepts where none exist.

### Active recall first

When you report completing a segment, the OS first asks what you remember. This makes retrieval happen in your own words before the OS adds context.

### User in control

You can set the intensity to `light`, `normal`, or `deep`. A light course gets minimal reflection; a deep one gets extensive discussion, application, and cross-source synthesis.

### Selective retention

Important ideas resurface later as conversational prompts. Not everything is scheduled.

### Connected to the same knowledge graph

Ideas from a course can link to books, projects, tasks, and other courses the same way ideas from reading do.

## Example interaction

> **You:** "I'm starting a LinkedIn Learning course on agentic AI."
> **OS:** "How familiar are you with AI agents already, and are you taking it for practical implementation, conceptual depth, or career development?"
> **You:** "I've used function calling. I want practical implementation."
> **OS:** "Got it. I'll keep this normal depth and watch for where you could apply it to existing projects."
>
> *(later)*
>
> **You:** "Finished the module on evaluation."
> **OS:** "Without looking back, what are the 1-3 things you remember most?"
> **You:** "The agent should check whether it actually made progress."
> **OS:** "Where could that fit into one of your existing workflows?"
> *(conversation continues; an insight is saved and connected to a project.)*

## What gets saved

- **Learning program** — course type, provider, goals, progress, modules, assessments, weak areas, target completion.
- **Learning sessions** — observations, recall, discussion, mistakes, insights, connections.
- **Durable ideas** — reusable insights promoted from sessions.
- **Retention schedule** — when to review which ideas.
- **Final synthesis** — a personal summary after finishing the program.

## Important behaviors

- No forms.
- No automatic capture of every detail.
- No full-text dumping of copyrighted syllabi or transcripts.
- No duplicate knowledge silos; everything lives in the same `ethan-life` knowledge domain.
- No conversion of a LinkedIn Learning course into a fake university structure.
- `ethan-life` remains the canonical personal state.

## Related capabilities

- [Guided Reading](guided-reading.md) — the reading counterpart.
- [Knowledge & Learning](../domains/knowledge/overview.md) — the broader domain.
- [Schedule Planning](schedule-planning.md) — for placing study time in the week.

## Technical implementation

- Workflows: `workflows/knowledge/guided-learning.md`
- Skills: `skills/knowledge/start-learning-program.md`, `pre-learning-assessment.md`, `capture-learning-session.md`, `review-learning-program.md`, `finish-learning-program.md`
- Schemas: `schemas/domains/knowledge/learning-program.schema.yaml`, `learning-session.schema.yaml`
- State: `ethan-life/domains/knowledge/learning-programs/`, `learning-sessions/`
