# Hobby Domain Instructions

## Scope

Reusable behavior for long-form hobbies that combine physical collection, creative output, worldbuilding, and event-driven narrative. Typical examples: miniature wargaming, model building, TTRPG campaigns, worldbuilding projects, and similar collecting-plus-story activities.

This domain intentionally separates:

- **Collection state** — what is owned, ordered, assembled, painted, magnetized, used.
- **Activity sessions** — build, paint, lore/worldbuilding, shopping, photography, review.
- **Battle / play reports** — tabletop (or equivalent) events that become canonical narrative inputs.
- **Lore candidates** — generated story ideas awaiting review.
- **Lore canon** — approved worldbuilding facts with explicit status and provenance.
- **Annual lore book** — a curated, print-oriented artifact built from canon, media, and approved narratives. Separate from dynamic reports.
- **Digital reports** — lightweight regeneratable operational outputs for collection, battles, rules/points, and progress.
- **Media assets** — photographs of real miniatures, generated concept art, heraldry, maps, diagrams, comic panels.
- **Narratives / vignettes** — curated illustrated scenes, flashbacks, comic spreads, and story excerpts.

All personal data (collection, lore, sessions, reports) lives in `ethan-life/domains/hobby`. All reusable skills, workflows, and schemas live in `ethan-os`.

## Core principles

- **Canon is earned.** Generated ideas, placeholders, AI concept names, and inferred lore must not silently become canon. They must pass through an explicit review step.
- **TBD is a valid status.** Unknown elements remain explicitly marked as TBD rather than invented.
- **Provenance is required.** Every canonical fact must trace back to a user decision, a game event, a build/paint session, or another recorded source.
- **Physical truth drives narrative.** A tabletop outcome, a paint scheme decision, or a model acquisition is a real event that may generate lore, but it must be recorded first.
- **No retconning without review.** If a newer fact contradicts older canon, flag it as `contradicted` or `deprecated` and explain why.

## Object flow

```
Collection items  →  Sessions (build/paint/lore/game)
                          ↓
                   Battle reports / session notes
                          ↓
                   Lore candidates (proposed)
                          ↓
                   Review & approve / reject / modify
                          ↓
                   Lore canon (locked / developing / TBD)
                          ↓
                   Lore-book sections + curated media/narratives
                          ↓
                   Annual lore-book edition (draft → finalized)
                          ↓
                   Rendered print HTML/PDF

Dynamic data also flows to separate digital reports:

Collection state → Collection Report
Battle reports   → Battle Chronicle
Rules/points     → Rules Reference
Sessions/progress → Hobby Progress Report
```

## Painting coach and skill development

For miniature/model hobbies, the system actively helps the user improve rather than just storing paint recipes.

**Assembly assessment.** Before a kit is glued, identify push-fit vs glue-required points, mould-line cleanup needs, fragile parts, alternate builds/weapon options, and whether magnetization or subassemblies are worthwhile. Warn explicitly before permanent glue is applied to anything that may be worth magnetizing.

**Unit-specific painting plans.** A plan is generated from:
- paints and tools the user already owns,
- the project's canonical color scheme,
- the user's current skill profile,
- which techniques have already been practiced.

Do not recommend buying additional supplies unless they are genuinely required for a color or technique the plan cannot achieve otherwise.

**Step-by-step coaching.** Painting sessions are interactive. Present one manageable phase at a time. After each major phase (especially after a photo is provided), evaluate what looks correct, what needs correction, whether to continue or fix first, and exactly how to make the correction. Distinguish:
- **must fix** — will be hard to correct later or breaks the army-wide scheme;
- **worthwhile improvement** — noticeable at tabletop distance but not blocking;
- **optional advanced refinement** — can wait.

Avoid perfectionism. Default target is tabletop-ready, not display-quality.

**Skill progression.** Each `hobby.technique-skill` carries a status:
- `new`
- `practicing`
- `comfortable`
- `proficient`

Advance only when supported by repeated evidence. Do not introduce advanced techniques simply because they exist.

**Practice order.** Use cheaper/repetitive models to learn foundational techniques before applying them to characters and centerpiece models. The practice order for the Necron project is:
Scarab Swarms → Warriors → Skorpekh Destroyers → Lokhust Heavy Destroyer → Doomstalker → Overlord → Immortals → Technomancer → Deathmarks → advanced models → C'tan Shard of the Void Dragon.

**Painting log.** A `hobby.painting-log` records the recipe, techniques, mistakes, corrections, time, photos, and lessons for each completed model. Capture only what is useful for future painting; avoid burdensome data entry.


## Status vocabulary

**Lore canon status**

- `locked` — user-approved, stable truth. Change only through an explicit revision.
- `developing` — approved but incomplete or provisional details remain.
- `provisional` — treated as true for now, pending future confirmation.
- `TBD` — explicitly unknown; do not invent content.
- `deprecated` — older version replaced by a newer entry.
- `contradicted` — in conflict with newer canon; requires reconciliation.

**Lore candidate status**

- `proposed` — auto-generated from a battle/session/collection event.
- `under_review` — Ethan is considering it.
- `approved` — merged into a lore-canon entry.
- `rejected` — explicitly discarded.
- `superseded` — replaced by a better candidate.

## Magnetization check

Before a kit with meaningful alternate builds or weapon options is assembled, run the `check-magnetization` skill. Output:

- `not_applicable` — no meaningful options.
- `recommended` — magnetization is worth the effort for this kit.
- `optional` — options exist but one loadout is clearly preferred.
- `undecided` — Ethan has not made a decision; block assembly status update.

Record the decision in the collection item's `magnetization_status` and `magnetization_note`.

## Collection progression states

A collection item may move through:

- `purchase_status`: owned / ordered / wishlist / not_owned / sold / gifted
- `assembly_status`: unassembled / assembled / partially_assembled / damaged / unknown
- `painting_status`: unprimed / primed / painting / completed / archived / not_applicable
- `magnetization_status`: not_applicable / planned_review / decided_no / decided_yes / partially_magnetized / fully_magnetized

Track `events` for notable moments: acquired, assembled, primed, painted, first_game, damaged, repaired, etc.

## Lore candidate review rules

- A trivial single event does not automatically become major lore. Promote based on pattern, narrative weight, and Ethan's judgment.
- Candidates must reference the originating battle/session/collection item IDs.
- Approved candidates are merged into one or more `hobby.lore-canon` entries; the candidate is then `merged` and its `canon_id_if_merged` is set.
- Rejected candidates are kept with a `rejection_reason` so the system does not re-propose them.

## Annual lore book generation

The annual lore book is the flagship, curated, print-oriented artifact. It is NOT an operational dashboard.

1. Source material: `hobby.lore-canon`, `hobby.lore-book-section`, `hobby.media`, and `hobby.narrative`. Optionally reference `hobby.collection-item` IDs when a unit profile is deliberately written.
2. Do NOT automatically include raw `hobby.battle-report` records, collection purchase status, points, build queues, session logs, or volatile rules.
3. A battle result enters the lore book only if it becomes a `hobby.lore-candidate`, is reviewed, and is approved/promoted into canon.
4. Each edition is represented by a `hobby.lore-book-edition` object: edition year, title, subtitle, status (`draft`/`finalized`/`archived`), generated date, source snapshot, print status, included sections/media/narratives, omitted empty sections, and visual gaps.
5. Render a print-oriented HTML artifact with fixed page dimensions, margins, bleed awareness, page breaks, chapter openers, headers/footers, and page numbering.
6. Frozen annual editions are preserved under `ethan-life/reports/hobby/<project>/lore-book/<year>/`. Later lore changes do not alter a finalized edition.
7. Identify missing visual opportunities and list them in the rendered output so the book can be progressively illustrated.

## Digital reports

Dynamic hobby data lives in lightweight, regeneratable digital reports only:

- **Collection report** — owned/planned units, assembly/paint/magnetization state, acquisition gaps.
- **Battle chronicle** — chronological battle history, outcomes, opponents, lore-candidate status.
- **Rules reference** — current edition, points, stats, abilities; volatile and edition-specific.
- **Hobby progress report** — session history, painting progress, milestones.

These reports should be clean digital HTML/Markdown outputs, not pages in the print lore book. They live in `ethan-life/reports/hobby/<project>/reports/`.

## Media and narrative assets

Media is first-class for the print book.

- `hobby.media` records track photographs, generated artwork, heraldry, diagrams, maps, comic panels, and page decorations.
- Generated artwork must be labeled as generated and include the tool/model used.
- Photographs of real miniatures must be distinguishable from concept/generated art.
- Each asset records provenance, creator/source, rights, print suitability (resolution, crop, orientation), and which lore/collection items it illustrates.
- `hobby.narrative` records hold curated illustrated scenes, comic spreads, flashbacks, vignettes, and quotes. They are not auto-generated battle reports.

## Relationships

Use inline typed links (`part_of`, `related_to`, `derived_from`, `revised_by`, `source_for`, `rendered_from`, `illustrated_by`) to connect collection items, sessions, battles, candidates, canon entries, lore-book sections, media assets, narratives, and rendered reports.
