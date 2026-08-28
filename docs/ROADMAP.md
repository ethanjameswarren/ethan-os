# Ethan OS Roadmap

A concise human-facing view of where Ethan OS is today and where it is headed.

Last reviewed: 2026-08-28

## Maturity model

| status | meaning |
|--------|---------|
| **Stable** | Ready for normal use. Core behavior is implemented, validated, and has been used successfully. |
| **Beta** | Usable end-to-end, but real-world usage may still reveal UX or architecture changes. |
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
| Finance | Beta | Accounts, transactions, budgets, monthly review | Better reporting and integration boundaries |
| Health | Beta | Habits, metrics, medical notes, weekly review | More flexible habit/review cadences |
| Career | Beta | Career evidence, job targets, tailored resumes, interview prep | More robust evidence-to-asset matching |
| Music / DJ Workflows | Beta | Collection management, DJ set building, record labels, Spotify sync | Polish and real-set usage feedback |
| Spotify Integration | Beta | OAuth setup, playlist export/sync, track matching, collection-style sync | Scope review and privacy/scope documentation |
| Notion Projection / Sync | Planned | Database mappings and sync architecture defined; live end-to-end sync not yet validated | Validate live sync behavior and decide projection scope |
| Downstream Bootstrap & Updates | Beta | Bootstrap script, safe update assessment, conflict classification, validation, rollback, Apache-2.0 licensing/attribution support | Real-world fork/clone testing and refinement |
| Human-Facing Documentation | In Development | P0 docs created: README, docs index, concepts, Guided Reading capability and workflow summaries, getting-started guides | Extend to remaining capabilities |
| Schedule Planning | Planned | Weekly review exists; calendar-based scheduling not yet implemented | Design calendar-aware scheduling without making external services authoritative |

## Now

Work actively being stabilized or built.

### Guided Reading real-world testing

- Verify prompts feel low-friction during actual reading.
- Tune retention scheduling and review delivery.
- Validate recommendation usefulness from real library and ratings.
- Confirm source-access and spoiler policies behave as expected.

### Human-facing documentation layer

- Complete P0 docs for the remaining capabilities.
- Add human workflow summaries for at least one workflow per domain.
- Keep technical docs accurate without forcing visitors into them.

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
- a capability becomes usable end-to-end,
- a beta capability graduates to stable,
- a planned or exploring item is abandoned or deferred,
- a significant new capability is approved,
- the current focus changes materially.

This is a product/capability roadmap, not a technical backlog. For detailed implementation work, see domain docs, workflow files, and the repository history.
