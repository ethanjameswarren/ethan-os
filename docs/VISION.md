# Ethan OS Vision

## What Ethan OS is trying to become

Ethan OS is a personal AI operating system.

It began as:

```
persistent personal state
+ reusable domain workflows
```

It is evolving into:

```
a coherent personal AI operating system
that understands direction,
assembles relevant context,
coordinates specialized capabilities,
helps allocate time and attention,
learns from results,
and remains under the user's control.
```

The concise framing is:

- **Goals provide direction.**
- **Domains provide specialized capabilities.**
- **Context and orchestration connect them.**
- **Planning allocates resources.**
- **Execution produces evidence.**
- **Reviews determine whether it is working.**

## The problem

Ordinary AI interaction is helpful in the moment and then forgets. A typical session looks like this:

```
conversation
→ useful response
→ context fragments across chats
→ user repeats information
→ plans, knowledge, and decisions become disconnected
```

The result is that the user ends up re-explaining goals, re-listing projects, re-finding prior decisions, and manually carrying information between different tools.

Ethan OS is designed for continuity:

```
conversation
→ understand intent
→ retrieve relevant personal context
→ run reusable behavior
→ save structured state
→ connect related information
→ use it later
→ review what happened
```

The system should become more useful over time because it retains structured knowledge, state, decisions, and relationships.

## Personal AI without a giant profile

Personalization should not mean loading everything known about the user into every prompt. The correct flow is:

```
USER REQUEST
→ INTENT
→ RELEVANT CONTEXT ASSEMBLY
→ WORKFLOW
```

The system should know how to retrieve the right context for the job and leave the rest out.

For example, "Should I take this course?" may require:

- current career goals
- active learning programs
- related prior knowledge
- current projects
- schedule capacity

It should not require:

- music collection
- medical notes
- unrelated finances

This is both an intelligence principle and a privacy principle.

## Goals as direction

A personal operating system needs direction. Goals are the natural source of that direction.

Broad goals often require multiple capabilities. For example, the goal "become healthier" may touch:

- **Health** — workout plan, metrics, habits
- **Nutrition** — food strategy, meal preparation
- **Schedule Planning** — protect workout and recovery time
- **Guided Reading** — a relevant book
- **Guided Learning** — a structured course
- **Knowledge** — useful concepts to retain
- **Review** — whether the strategy is working

The system should be able to trace:

```
GOAL
→ OUTCOME
→ STRATEGY
→ PROJECT / PLAN / LEARNING / HABIT
→ ACTION / SESSION / SCHEDULE BLOCK
→ EVIDENCE
→ REVIEW
```

Not every goal requires every layer. The architecture should allow the right layers for the goal, no more.

## Goal graph, not a rigid tree

Goals are not a strict tree. Real life is a graph.

- One course may support a career goal and a project goal.
- One workout habit may support health, energy, and recreation.
- One project may support learning, career, and financial goals.

The system should allow many-to-many relationships and not force users to manually maintain the graph. Relationships should emerge naturally from workflows and conversation.

## Vertical capabilities vs horizontal intelligence

**Vertical capabilities** are specialized systems for specific domains:

- Knowledge
- Guided Reading
- Guided Learning
- Planning
- Schedule Planning
- Finance
- Health
- Career
- Music / DJ

They understand their own domain deeply.

**Horizontal intelligence** is the shared services layer that lets those domains behave as one operating system:

- context assembly
- universal retrieval
- temporal understanding
- cross-domain reasoning
- goal relationships
- decision intelligence
- review orchestration
- priority alignment
- workflow orchestration
- permissions and privacy
- bounded proactive assistance

The central architectural principle is:

> **Vertical capabilities provide specialized behavior. Horizontal intelligence allows those capabilities to work together.**

## Cross-domain reasoning

The user should not have to manually carry information from domain to domain.

Concrete examples:

1. A user learns about feedback loops through **Guided Reading**. Later, when diagnosing a project in **Planning**, the OS can recognize that concept as relevant.
2. A user completes a technical course in **Guided Learning**. When preparing for a role in **Career**, the OS can recognize the new skill as evidence.
3. A user sets the goal of completing a certification. **Guided Learning** tracks course progress, **Schedule Planning** allocates study time, **Knowledge** tracks weak concepts, and **Career** uses the credential after completion.

This is enabled by shared state, typed relationships, and selective context assembly. It is not enabled by hard-coding every pair of domains.

## Orchestration

A single real-world event may touch multiple capabilities. For example:

> "I got an interview next Thursday."

Coordinated behavior may include:

- **Career** — capture the interview, retrieve relevant evidence, prepare likely topics
- **Planning** — create preparation actions
- **Schedule Planning** — reserve preparation time
- **Calendar** — account for the interview event
- **Knowledge** — retrieve relevant technical and project information
- **Review** — capture the outcome afterward

This is not uncontrolled autonomous behavior. The OS coordinates capabilities and suggests material actions; the user remains in control.

## Planning as resource allocation

Planning is not merely a task list. Goals compete for finite resources:

- time
- attention
- energy
- money

The OS should help reconcile that reality. If a career goal wants six hours this week, a health goal wants four, and only seven realistic flexible hours exist, the system should surface the conflict and help prioritize rather than pretending everything fits.

Schedule Planning becomes the mechanism that translates priorities into realistic time allocation.

## Execution and evidence

The system distinguishes activity from outcome.

- **Activity:** "I did the task."
- **Outcome:** "Did it move the goal?"

Three workouts completed does not automatically mean a health goal is achieved. The system should capture evidence over time and use it during review. Evidence may be:

- metrics
- observations
- completed work
- qualitative evidence
- user judgment

It should not invent quantified progress where no meaningful metric exists.

## Review as the feedback loop

Reviews close the loop:

```
GOAL
→ STRATEGY
→ PLAN
→ EXECUTION
→ EVIDENCE
→ REVIEW
→ ADJUST
```

The system should ask:

- Is this still important?
- Is the strategy being executed?
- Is it producing the expected result?
- What keeps getting blocked?
- Does the strategy need to change?
- Should the goal remain active?

Sunday, monthly, course, book, project, and domain reviews may eventually participate in a broader review orchestrator.

## Decisions as learning opportunities

Meaningful decisions are worth recording. A decision record may include:

- what was decided
- alternatives considered
- assumptions
- reasoning
- expected result
- risks
- eventual outcome
- lessons learned

This enables later questions such as:

- "Why did I choose this?"
- "How did that decision turn out?"
- "What assumptions do I keep getting wrong?"

The goal is not to record every minor choice. Only decisions meaningful enough to benefit from future review.

## Temporal awareness

People change. A personal OS must understand that state evolves. Preferences, priorities, goals, projects, and circumstances may be:

- current
- historical
- temporary
- superseded
- uncertain

If "Wednesday is Learning night" later becomes "Wednesday is Reading night," the system should not retrieve both as equally current. It should preserve history without confusing history with the present.

## Proactive but bounded

The OS should be able to surface useful nudges:

- "Your exam is next week and two weak concepts are due for review."
- "This project is high priority but has no time allocated this week."
- "You planned to apply Friday but the resume is not ready."

It should not:

- send constant notifications
- optimize without being asked
- silently create tasks
- act without authority
- treat every goal as urgent

Proactive behavior should consider relevance, urgency, confidence, interruption cost, user preference, and domain permissions.

The principle is:

> **Helpful when needed. Quiet when not.**

## User control

Ethan OS should:

- suggest before making significant changes
- preserve provenance
- keep important state inspectable
- allow correction, deletion, and export
- make uncertainty visible
- avoid silent rewriting of history
- avoid hidden optimization objectives

The user owns the system.

## Privacy by architecture

The core separation is:

- **ethan-os** — public behavior and framework
- **ethan-life** — private personal state
- **integrations** — projections and adapters with the least privilege they need

Future clients and integrations should follow capability-scoped access. A Spotify integration should see Music. A resume workflow should see Career and relevant learning evidence. It should not require all personal data to be available to every capability.

## Portability

The user's state should remain portable. Ethan OS should support:

- switching AI clients
- switching models
- exporting a domain
- backing up state
- moving to another storage backend
- building standalone applications

The personal OS should outlive any one AI vendor or interface.

## Client and interface independence

Ethan OS is not:

- a Devin project
- a ChatGPT project
- a Claude project
- an IDE feature

Those are interfaces. Ethan OS is the persistent behavior and state architecture underneath them.

Potential interfaces include:

- AI IDE
- ChatGPT Desktop
- Claude Desktop
- CLI
- mobile app
- dedicated capability app
- future interfaces

The same OS should remain usable across them where technically possible.

## Capability applications

Major vertical capabilities may eventually become standalone experiences: a Guided Reading app, a Career app, a Planning app, a DJ app. These should share:

- common personal state
- schemas and contracts
- context and retrieval
- goal relationships
- OS principles

They should not become isolated products with disconnected personal data.

## Personalization without lock-in

Ethan OS should be customizable enough that:

- Ethan OS
- John OS
- any other personal OS

can meaningfully diverge. Downstream users should be able to:

- add capabilities
- change workflows
- remove things
- customize policies
- evolve independently

while still optionally adopting compatible upstream improvements.

## Anti-optimization principle

Ethan OS should not turn a person's entire life into a productivity system. Not every activity must support a measurable goal. There must be room for:

- rest
- relationships
- recreation
- curiosity
- hobbies
- spontaneity
- doing things simply because they are enjoyable

The goal graph provides coherence. It does not require every part of life to justify itself through productivity.

## What Ethan OS should not become

- A giant system prompt.
- A hidden proprietary user profile.
- A productivity guilt engine.
- A cloud service that owns the user's data.
- An uncontrolled autonomous agent.
- A collection of disconnected mini-apps.
- A vendor-locked assistant.
- A database that requires the user to manually maintain everything.
- A system that optimizes every minute of the user's life.

## Visual model

```
                         USER
                          │
                       GOALS
                          │
             CONTEXT + ORCHESTRATION
                          │
      ┌───────────────────┼───────────────────┐
      │                   │                   │
   Knowledge           Planning            Career
   Learning            Schedule            Finance
   Reading             Projects            Health
   Music               Habits              Evidence
      │                   │                   │
      └───────────────────┼───────────────────┘
                          │
                      EXECUTION
                          │
                       EVIDENCE
                          │
                        REVIEW
                          │
                      ADJUST / LEARN
                          │
                    GOALS UPDATED

           USER-OWNED PERSONAL STATE
```

## Near / mid / long-term evolution

**Today**

- Persistent state
- Reusable workflows
- Specialized domains

**Next**

- Context Engine
- Goal Graph
- Cross-domain retrieval and reasoning
- Better evaluation and reviews

**Later**

- Workflow orchestration
- Bounded proactive assistance
- Desktop and client access
- Standalone capability experiences

**Destination**

A portable, user-owned personal AI operating system that becomes more useful as it learns the user's goals, knowledge, decisions, and evolving context.

## Aspirational framing

Several ideas in this document are directions Ethan OS is evolving toward, not capabilities that are fully implemented today. Where the project is actively building these foundations, the language is "evolving toward" or "designed to support." Where an idea is still architectural direction, it is described as the intended destination, not the current state.

For current capability maturity and implementation status, see [ROADMAP.md](ROADMAP.md).
