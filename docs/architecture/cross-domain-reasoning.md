# Cross-Domain Reasoning

## Purpose

Cross-Domain Reasoning interprets the `core.context-bundle` that Context Assembly produces. It does not retrieve or select context. Its job is to notice useful patterns across the retrieved objects.

```
USER REQUEST
→ INTENT
→ UNIVERSAL RETRIEVAL
→ CONTEXT ASSEMBLY
→ CROSS-DOMAIN REASONING
→ DOMAIN WORKFLOW
→ OUTPUT / ACTION
```

## Responsibilities

- Identify connections.
- Detect overlaps and duplication.
- Find gaps and missing links.
- Surface conflicts and tradeoffs.
- Trace why something matters.
- Distinguish activity from outcome.
- Provide provenance for every finding.

## What it does NOT do

- Retrieve new objects.
- Load unrelated domains.
- Create or modify state.
- Schedule tasks automatically.
- Make automatic career or financial decisions.

## Finding model

A finding has:

| field | meaning |
|-------|---------|
| `type` | `connection`, `transfer_opportunity`, `overlap`, `gap`, `evidence_gap`, `conflict`, `tradeoff`, `priority_mismatch`, `stale_assumption` |
| `statement` | human-readable observation |
| `object_ids` | objects that ground the finding |
| `domains` | domains involved |
| `evidence` | the traceable evidence |
| `confidence` | `high`, `medium`, `low` |
| `why_it_matters` | why the user should care |
| `implication` | optional interpretation |
| `suggested_action` | optional next step, non-automatic |

## Grounding rules

- High confidence comes from explicit typed links.
- Medium confidence comes from shared tags or concepts.
- Low confidence comes from heuristics.
- Every claim refers to `object_ids` in the bundle.

## Provenance

The evidence field records why the finding was generated. A `transfer_opportunity` might cite `shared_concepts`. A `connection` might cite the typed `relation` name. A `gap` might cite the absence of expected linked objects.

## Workflow integration

Cross-Domain Reasoning is used by:

- `skills/knowledge/assess-course-fit.md`
- `skills/planning/sunday-weekly-planning.md`
- `workflows/career/build-tailored-resume.md`
- `workflows/core/ask.md`

Each workflow decides what to do with the findings.
