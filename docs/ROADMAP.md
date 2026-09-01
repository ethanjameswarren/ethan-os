# Ethan OS Roadmap

A concise human-facing view of where Ethan OS is today and where it is headed.

For the long-term design philosophy and destination, see [VISION.md](../VISION.md).

Last reviewed: 2026-08-31

## Maturity model

| status | meaning |
|--------|---------|
| **Stable** | Ready for normal use and validated through repeated successful usage. |
| **Beta** | Ready for normal use end-to-end, but still being validated through real-world usage and may receive UX or architecture refinements. |
| **In Development** | Actively being implemented; not yet considered ready for normal use. |
| **Planned** | Approved direction, but implementation has not started or is minimal. |
| **Exploring** | Idea worth investigating, but architecture and scope are not committed. |
| **Deferred** | Intentionally not being worked on now. |

## Current state

Ethan OS is a public behavior layer for personal AI systems. The core runtime, validation, and several domains are implemented and tested. Work is focused on making the system reliable and understandable in real-world use.

## Capability status

| Capability | Status | What works now | Next step |
|------------|--------|----------------|-----------|
| Core Runtime | Stable | Intent routing, workflow selection, skill loading, schema validation, deterministic tests, demo flow | Hardening and richer error handling |
| Knowledge | Beta | Sources, captures, ideas, summaries, reviews, typed relationships, retrieval across objects | Improve synthesis and cross-domain retrieval |
| Guided Reading | Beta | Full reading lifecycle, library/backlog, active recall, retention scheduling, source grounding, spoiler protection, recommendations | Real-world friction testing and prompt refinement |
| Planning / Projects | Beta | Goals, projects, tasks, weekly review | Tighter integration with scheduling |
| Finance | Beta | Accounts, transactions, budgets, income sources, expense profiles, debts, financial goals, allocation policies, financial snapshots, debt payoff strategies (avalanche/snowball/promo-aware/custom), 401k per-paycheck targeting, cash-flow allocation, orchestrated financial reviews with epistemological labeling, and a stdlib Python calculator with deterministic tests | Real-world usage validation, trend analysis, and multi-period comparison |
| Health | Beta | Habits, metrics, medical notes, weekly review, equipment inventories, and location-aware workout construction | Validate real workouts, substitutions, and unavailable-equipment recovery |
| Career | Beta | Career evidence, role reconstruction, capability maps, job targets, goal-aligned resumes, LinkedIn/Indeed profiles, cover letters, and interview prep | Validate a target-specific presentation package and review claim selection |
| Music / DJ Workflows | Beta | Collection management, DJ set building, record labels, Spotify sync | Polish and real-set usage feedback |
| Spotify Integration | Beta | OAuth setup, playlist export/sync, track matching, collection-style sync | Scope review and privacy/scope documentation |
| Notion Projection / Sync | Planned | Database mappings and sync architecture defined; live end-to-end sync not yet validated | Validate live sync behavior and decide projection scope |
| Downstream Bootstrap & Updates | Beta | Bootstrap script, safe update assessment, conflict classification, validation, rollback, Apache-2.0 licensing/attribution support | Real-world fork/clone testing and refinement |
| Human-Facing Documentation | Beta | README, docs index, core concepts, all major capability docs, representative workflow summaries per domain, and getting-started guides created | Additional polish and contributor documentation may still evolve |
| Schedule Planning | Beta / Ready | End-to-end baseline, weekly planning, daily replanning, overrides, conflict detection, and schedule diagnosis implemented. Currently being validated through real-world use. | Real-world usage and calendar integration refinement |
| Google Calendar Integration | In Development | OAuth, event reads and normalization, deterministic ICS export, and explicit weekly-plan write-back are implemented; no credentialed real-world run is recorded. | Validate read and write-back with a test calendar, including partial-failure recovery |
| Desktop AI Client Access | Planned | Conceptually supported by the file-based architecture; no official non-IDE desktop-client bridge implemented or validated yet. | Design and validate an MCP/server bridge that keeps ethan-life private and client adapters vendor-agnostic. |
| Guided Learning | Beta / Ready | Supports university courses, online/self-paced learning, certifications, and workplace training with active recall, structured sessions, selective retention, progress tracking, assessment prep, and Sunday planning integration. Deterministic tests pass; real-world usage is now being used to refine prompts, material ingestion, and retention behavior. | LinkedIn Learning live test, prompt and retention refinement, and later syllabus/material ingestion automation |

## Cross-cutting / horizontal services

These are the shared services that make the vertical capabilities feel like one coherent system.

| Capability | Status | What works now | Next step |
|------------|--------|----------------|-----------|
| Context Engine | Beta / Ready | `core.context-request` and `core.context-bundle` schemas, `skills/core/context-assembly.md`, `scripts/core/context_assembly.py`, and `docs/architecture/context-assembly.md` implemented. Used by Sunday Planning, tailored resume, course-fit assessment, and `workflows/core/ask.md`. | Harden permission enforcement and refine retrieval precision through real usage. |
| Cross-Domain Reasoning | Beta / Ready | `scripts/core/cross_domain_reasoning.py`, `skills/core/cross-domain-reasoning.md`, and `docs/architecture/cross-domain-reasoning.md` in place. Finds transfer opportunities, overlaps, gaps, conflicts, priority mismatches, and goal-support traces. Used by course-fit, Sunday Planning, resume, and `ask` workflows. | Refine based on real usage and expand beyond one-hop reasoning. |
| Universal Personal Retrieval | Beta / Ready | `scripts/core/universal_retrieval.py` discovers objects across domains, ranks them with a transparent score, and supports `entity_refs`, `avoid_domains`, and `time_horizon`. Used by the Context Engine. | Add optional semantic/keyword expansion and search by arbitrary user questions. |
| Temporal State | Exploring | `updated_at` on core objects; schedule overrides already support `valid_for` ranges. | Decide minimal temporal metadata pattern before retrofitting every object. |
| Decision Intelligence | Beta / Ready | `knowledge.decision` schema, `skills/knowledge/capture-decision.md`, `workflows/core/review-decision.md`, demo fixtures, and deterministic tests in place. Cross-domain reasoning recognizes decisions. | Live capture and real-world review cycles. |
| Review Orchestrator | Beta / Ready | `scripts/core/review_orchestrator.py`, `workflows/core/review-orchestrator.md`, `workflows/planning/review-goal.md`, and `workflows/core/review-decision.md` in place. Skips empty domains, surfaces decisions, goals, learning, and retention reviews, and delegates to domain workflows. | Harden cadence logic and add more domain-specific review delegations. |
| Priority Alignment | Beta / Ready | Strategic-objective policy, project evaluation, weekly planning, next-action ranking, goal review, and drift/gap findings connect an authoritative long-term goal to execution. A private planning goal may project the authoritative domain goal under explicit synchronization rules. | Validate monthly trajectory review and drift/gap recovery through real use. |
| Workflow Evaluation | In Development | `evaluations/context-engine/expectations.md` and `evaluations/cross-domain-reasoning/expectations.md` now define behavioral expectations. Tests validate retrieval, reasoning, and privacy boundaries. | Extend to other high-stakes workflows such as resume and schedule planning. |
| Beta Usage / Friction Tracking | Beta / Ready | `core.friction-log` schema, `skills/core/capture-friction.md`, `workflows/core/capture-friction.md`, `workflows/core/review-friction-log.md`, `scripts/core/friction_log.py`, and deterministic tests are in place. Capture, private persistence, review/triage, and evaluation-candidate conversion work end-to-end. | Real-world usage refinement; do not expand into a full issue tracker. |
| Workflow Orchestration | Exploring | Workflows call skills; workflow-to-workflow composition is not yet formal. | Design orchestration primitive for multi-workflow events. |
| Proactive Assistance | Exploring | No background behavior; all prompts are user-initiated. | Define urgency/relevance thresholds and a manual proactive-surface skill. |
| Privacy & Permissions | Planned | Privacy is enforced by architecture and `.gitignore`; client-scoped permissions are not implemented. | Design permission contract for desktop clients and integrations. |
| Personal Data Import / Portability | Planned | Bootstrap script exists; domain-specific importers are not. | Add 1-2 high-leverage importers (resume/library/Spotify). |
| Capability Packs / Profiles | Exploring | Domains are individually toggleable; no packaging layer exists. | Document how domains compose into profiles. |

## Now

Work actively being stabilized or built.

### Guided Reading real-world testing

- Verify prompts feel low-friction during actual reading.
- Tune retention scheduling and review delivery.
- Validate recommendation usefulness from real library and ratings.
- Confirm source-access and spoiler policies behave as expected.

### Schedule Planning real-world testing

- Verify baseline, weekly plan, and override scopes behave naturally in conversation.
- Confirm dependency reasoning feels right for commute, sleep, and morning-routine changes.
- Test schedule diagnosis prompts without over-scheduling or silently deleting activities.
- Refine minimal-change behavior based on actual usage.

### Core runtime hardening

- Better handling of ambiguous intent.
- Clearer confirmation thresholds for material changes.
- Validation error messages that help recovery.

## Next

Likely near-term work once current capabilities are stable.

- **Extend human-facing capability docs** for Knowledge, Planning, Finance, Health, Career, and Music.
- **Improve cross-domain retrieval** so ideas from a book can naturally appear in planning, career, or health contexts.
- **Schedule Planning** — connect goals, tasks, and reviews with calendar-aware scheduling while keeping `ethan-life` authoritative.
- **Refine review and recommendation behavior** based on real usage, including abandoned books and negative feedback.
- **Better music workflow polish** for live DJ set preparation and post-set reflection.

## Later / Direction

These are desired outcomes, not committed features or dates.

- **More life domains** operating through the same reusable architecture, without parallel silos.
- **Richer cross-domain reasoning** — a learning from a book informing a project plan, a habit, or a career story.
- **Optional user-facing application or interface** that talks to `ethan-life` without replacing the file-based model.
- **Deeper connected-service integrations** where useful, always as projections from canonical `ethan-life` state.
- **Portable personal knowledge** that can move across AI models, interfaces, and storage backends.
- **More proactive planning and review** while preserving explicit user control and avoiding notification overload.

## Exploring

Ideas that have come up but are not yet committed.

- A dedicated mobile or desktop app for Ethan OS.
- Voice-first capture and low-friction input channels.
- Vector/semantic search backend as an optional layer.
- Gmail or messaging integrations for action/capture extraction.
- Fitness device integrations for Health domain.
- CSV bank statement import and merchant-level transaction categorization for Finance (e.g. Chase, Navy Federal).
- Financial data provider integrations for Finance domain.
- External automation hooks such as Zapier or Make.
- A public documentation site beyond the repository Markdown files.

## Deferred

- Replacing the file-based model with a traditional database as the canonical store.
- Gamification, streaks, or achievement systems.
- Broad multi-user or shared-instance support beyond the personal single-user model.
- ML-based recommendation systems; current recommendation logic remains transparent and rule-based.

## Maintenance notes

Update this roadmap when:

- a capability enters active development,
- a beta capability becomes usable end-to-end,
- a beta capability graduates to stable,
- a planned or exploring item is abandoned or deferred,
- a significant new capability is approved,
- the current focus changes materially.

This is a product/capability roadmap, not a technical backlog. For detailed implementation work, see domain docs, workflow files, and the repository history.
