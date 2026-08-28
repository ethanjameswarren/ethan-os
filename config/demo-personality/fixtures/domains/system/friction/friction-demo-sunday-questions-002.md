---
id: friction-demo-sunday-questions-002
schema: core.friction-log
schema_version: 1
title: Sunday planning asks too many questions
created_at: 2026-08-26
updated_at: 2026-08-27
status: open
summary: Sunday planning asks too many questions
description: The Sunday planning workflow prompted repeatedly for information that was already in the context bundle.
feedback_type: excessive_questions
affected_capability: Planning / Weekly Review
affected_workflow: workflows/planning/weekly-review.md
affected_skill: skills/planning/sunday-weekly-planning.md
user_expectation: Use existing schedule, goals, and projects without repeated prompts.
observed_behavior: Asked five clarifying questions before building the plan.
severity: medium
frequency: repeated
occurrence_count: 2
occurrence_dates:
  - 2026-08-26
  - 2026-08-27
occurrence_context_refs:
  - bundle-20260826-001
  - bundle-20260827-002
context_refs:
  - bundle-20260826-001
relevant_domain: planning
root_cause_inferred: context_assembly
root_cause_inference_note: Context bundle was assembled but not consumed by the skill.
provenance:
  agent_version: ethan-os-0.1.0
  provenance_note: Demo fixture for repeated-question friction.
---

# Sunday planning asks too many questions

Synthetic demo friction entry with multiple occurrences.
