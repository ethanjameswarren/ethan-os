---
id: friction-demo-wrong-context-005
schema: core.friction-log
schema_version: 1
title: Pulled finance context for no reason
created_at: 2026-08-27
updated_at: 2026-08-27
status: open
summary: Pulled finance context for no reason
description: While the user was asking about a book, Ethan OS surfaced finance records as context.
feedback_type: irrelevant_context
affected_capability: Context Engine
affected_workflow: workflows/core/ask.md
affected_skill: skills/core/context-assembly.md
user_expectation: Context assembly should only retrieve objects relevant to the current question.
observed_behavior: Included unrelated finance transactions in the context bundle.
severity: high
frequency: once
occurrence_count: 1
occurrence_dates:
  - 2026-08-27
context_refs:
  - bundle-20260827-004
  - tx-grocery-20260825
relevant_domain: core
root_cause_inferred: retrieval
root_cause_inference_note: Retrieval broadened too far without relevance filtering.
provenance:
  agent_version: ethan-os-0.1.0
  provenance_note: Demo fixture for high-severity context error.
---

# Pulled finance context for no reason

Synthetic demo high-severity friction entry.
