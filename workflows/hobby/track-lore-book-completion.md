# Workflow: track-lore-book-completion

## Purpose

Track lore-book completion and dependencies without inventing, resolving, or promoting creative canon. The workflow preserves the user's control over all canon decisions while ensuring unresolved work, contradictions, and newly unblocked work remain visible.

## Trigger

- "Show the 2026 lore book completion tracker."
- "Update lore-book completion after this canon decision."
- "What lore decision should we develop next?"
- "What is blocked in the dynasty lore book?"

## Inputs

- The target annual lore-book completion tracker.
- `hobby.lore-canon` records and their explicit statuses.
- Approved results from `review-and-promote-lore` or `worldbuilding-session`.
- The target `hobby.lore-book-edition`, section records, narratives, media, and collection records.

## Outputs

- Updated human-readable annual completion tracker.
- A summary of the current phase, completed decisions, developing decisions, remaining TBDs, blocked items, overall completion, contradictions, newly available work, and the next recommended unresolved decision.
- No new canon unless the user has explicitly approved it through the lore review process.

## Canon state mapping

The tracker uses exactly three creative-lore states:

- `TBD` — not yet decided.
- `DEVELOPING` — being explored or drafted, but not canonical.
- `CANON` — explicitly approved.

Map source lore statuses as follows:

- `locked` -> `CANON` (equivalently "LOCKED CANON")
- `developing` or `provisional` -> `DEVELOPING` (equivalently "WORKING CANON")
- `TBD` -> `TBD` (equivalently "UNRESOLVED")
- `deprecated` and `contradicted` never count toward completion; retain them only as warnings or historical references.

A draft, rendered section, candidate, generated concept, or repeated assertion is not evidence of approval. Never promote `DEVELOPING` material to `CANON` merely because it appears in a draft.

## Phase dependencies

1. **Dynasty Foundation** — in progress until all eight foundation decisions are `CANON`.
2. **Characters & Court** — blocked until Phase 1 is complete.
3. **Military Organization** — blocked until Phases 1–2 are complete.
4. **History & Narrative** — blocked until Phases 1–3 are complete.
5. **Book Assembly** — blocked for final completion until Phases 1–4 are complete. Draft assembly may proceed only from established canon and must preserve unresolved labels.

A blocked item may reference existing source material, but it cannot be marked complete until its prerequisite phases are complete and its own acceptance criteria are met.

## Steps

1. Load the annual tracker and all records it references.
2. Recalculate each tracked item's state from explicit source status and approval evidence; do not infer missing facts.
3. When the user supplies newly approved canon:
   1. Update the appropriate canonical lore record.
   2. Identify lore, sections, narratives, and tracker items that depend on it.
   3. Compare the approved statement with existing canon and flag contradictions for user resolution.
   4. Update the completion tracker.
   5. Identify items newly available to develop because their dependencies are satisfied.
   6. Do not invent missing information to complete a phase.
4. Mark a phase complete only when every required item in that phase is complete and canonical where a creative decision is involved.
5. For Book Assembly, separately track all 23 sections and every required, recommended, or optional visual asset. A section is complete only when its source canon is sufficient, its prose is approved, and its section record is `complete`.
6. Calculate overall completion from explicitly complete tracker deliverables. Show the numerator and denominator with the percentage so partial or blocked work is not misleading.
7. Recommend the next unresolved decision from the earliest incomplete, unblocked phase. Recommend one decision, not an invented answer.
8. Return the human-readable summary and list any contradictions or records needing review.

## 2026 tracked scope

### Phase 1 — Dynasty Foundation

Official dynasty name; current ruler; tomb world; ancient origin; Great Sleep; modern awakening; arrival omen; heraldry.

### Phase 2 — Characters & Court

Ruling Overlord; royal court; Crypteks; military commanders; Destroyer personalities; character relationships.

### Phase 3 — Military Organization

Cyan force organization; Red / Destroyer organization; Purple / C'tan classification; named formations; named units; command hierarchy; integration of the physical model collection into canonical formations.

### Phase 4 — History & Narrative

Territories; important locations; Imperial encounters; Ork encounters; Chaos encounters; Aeldari encounters; Tyranid relationship; named rivals; major campaigns; major battles; master timeline; 2–4 narrative vignettes.

### Phase 5 — Book Assembly

All 23 master-outline sections and all edition visual assets. Convert established canon into polished book-ready prose; do not use assembly to resolve canon gaps.
