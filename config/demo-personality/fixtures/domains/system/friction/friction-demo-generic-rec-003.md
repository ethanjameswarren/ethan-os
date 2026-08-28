---
id: friction-demo-generic-rec-003
schema: core.friction-log
schema_version: 1
title: Generic book recommendation
created_at: 2026-08-20
updated_at: 2026-08-22
status: validated
summary: Generic book recommendation
description: The book recommendation was not grounded in the user's library or recent reading.
feedback_type: bad_recommendation
affected_capability: Guided Reading
affected_workflow: workflows/knowledge/book-recommendation.md
affected_skill: skills/knowledge/recommend-next-book.md
user_expectation: Recommendations should be grounded in owned unread books and recent reading.
observed_behavior: Suggested a generic best-seller with no link to user context.
severity: medium
frequency: once
occurrence_count: 1
occurrence_dates:
  - 2026-08-20
context_refs:
  - bundle-20260820-001
relevant_domain: knowledge
root_cause_inferred: reasoning
root_cause_inference_note: Recommendation logic did not use personal library state.
resolution_notes: Updated recommendation skill to prefer owned and wishlist books.
resolved_at: 2026-08-22
fix_reference: fix-20260822-recommendation
validation_status: user_confirmed
test_evaluation_reference: eval-book-recommendation-001
user_confirmed_resolution: true
user_confirmed_at: 2026-08-22
provenance:
  agent_version: ethan-os-0.1.0
  provenance_note: Demo fixture for resolved friction.
---

# Generic book recommendation

Synthetic demo friction entry that has been resolved and validated.
