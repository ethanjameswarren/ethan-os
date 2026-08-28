---
id: friction-demo-asked-known-001
schema: core.friction-log
schema_version: 1
title: Asked for already-known active book
created_at: 2026-08-27
updated_at: 2026-08-27
status: open
summary: Asked for already-known active book
description: User reported that Guided Reading asked which book is being read even though one active source already exists.
feedback_type: asked_known_information
affected_capability: Guided Reading
affected_workflow: workflows/knowledge/start-reading.md
affected_skill: skills/core/context-assembly.md
user_expectation: Resolve active reading state automatically when exactly one active source exists.
observed_behavior: Asked the user to identify the book.
severity: medium
frequency: once
occurrence_count: 1
occurrence_dates:
  - 2026-08-27
occurrence_context_refs:
  - bundle-20260827-001
context_refs:
  - bundle-20260827-001
  - book-dune
relevant_domain: knowledge
root_cause_inferred: context_assembly
root_cause_inference_note: Active source was not reused during start-reading routing.
provenance:
  agent_version: ethan-os-0.1.0
  provenance_note: Demo fixture for asked-known friction.
---

# Asked for already-known active book

Synthetic demo friction entry.
