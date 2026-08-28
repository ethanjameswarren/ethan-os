---
id: ls-stats-lecture-3
schema: knowledge.learning-session
schema_version: 1
title: Hypothesis testing lecture
created_at: 2026-01-15
program_id: lp-statistics-301
session_type: lecture
session_date: 2026-01-15
module_id: mod-week-3
topic: p-values and t-tests
user_observations:
  - text: p-values still feel slippery
  - text: The professor emphasized rejecting the null hypothesis
active_recall:
  - p-value is the probability of seeing the data if the null hypothesis were true
  - t-test compares means across groups
questions_asked:
  - Without looking back, what does a small p-value mean?
extracted_insights:
  - insight_id: i-p-value-intuition
    title: p-value as evidence against null
    note: Smaller p-value means stronger evidence against the null hypothesis
    retention_priority: high
mistakes:
  - description: Confused p-value with probability the alternative is true
    concept: p-values
    correction: p-value is not P(alternative true); it is P(data or more extreme | null true)
    recurring: false
open_questions:
  - When should I use a z-test instead of a t-test?
connections:
  - target_id: lp-statistics-301
    target_type: learning_program
    description: Part of the university course
provenance:
  source: user
  captured_at: 2026-01-15
---
