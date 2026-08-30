# Skill: reconcile-career-context

## Purpose

Ensure newly captured career evidence is correctly integrated with existing evidence without introducing contradictions, duplicates, or silent regressions.

## Inputs

- New or updated `career.work_artifact`
- Existing `career.work_artifact` records for the same employer/role
- Existing `career.role_context` for the same employer/role
- Existing `career.capability` records

## Reconciliation checks

For each new or updated artifact, determine whether it:

- **Contradicts** existing evidence (dates, scope, ownership, outcomes)
- **Supersedes** existing evidence (more detailed, more recent, or authoritative update)
- **Expands** existing evidence (adds new but compatible detail)
- **Duplicates** existing evidence (substantially the same content)
- **Complements** existing evidence (different project, responsibility, or capability)

## Rules

- Merge duplicates rather than creating parallel records that cover the same project and timeframe.
- Preserve historically meaningful distinctions — do not merge artifacts that represent genuinely different projects or phases.
- Do not silently replace stronger evidence with weaker summaries.
- When evidence contradicts existing records, flag the conflict and ask for user clarification before updating canonical state.
- When evidence supersedes an existing record, update the existing record and add a `revised_by` / `replaces` link rather than deleting it.
- When evidence expands an existing record, update the record in place and note what was added in provenance.
- Update `career.role_context` only when the new evidence changes recurring patterns, not for every new project detail.
- Update `career.capability` records only when the evidence genuinely strengthens or broadens the capability.

## Output

- A reconciliation decision for each affected existing object
- Updated objects with appropriate `links` (`revised_by`, `replaces`, `related_to`, `sourced_from`)
- A concise report of what was merged, updated, created, or flagged for user review

## Relationship types

- `revises` / `revised_by` — a newer record updates an older one
- `replaces` / `replaced_by` — a record is deprecated by a newer, more authoritative record
- `related_to` — distinct but related records
- `part_of` — artifact belongs to a larger program or role
- `duplicates` — records cover substantially the same content (should usually be merged)

## Confirmation policy

- Auto-execute: merging obvious duplicates, expanding records with compatible detail, or adding complementary artifacts.
- Ask for confirmation: resolving contradictions, deprecating existing records, or when merging would discard meaningful distinctions.
