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

## Jahrekt Dynasty — locked canon

The Necron project uses the following locked canon for the dynasty (`warhammer-40k-necron-dynasty`):

- **Name:** Jahrekt Dynasty — pronounced "JAH-rekt" (approximately "ja-wrecked"). The only canonical dynasty name; all previous working names are deprecated.
- **"Pale Crown" is NOT canon.** It was only an early paint-scheme/concept label. Never use it as a dynasty name, Imperial nickname, ruler title, relic, campaign, location, symbol, or historical term. Do not reintroduce it unless the user explicitly instructs.
- **Also banned:** "Kharaset" and "The Fixed Axis" — deprecated, non-canon; never introduce. Canonical terms: Jahrekt Dynasty, The Piercing Dominion, Dominion through Control, "What resists is… *corrected*."
- **Sigil:** The Piercing Dominion — the approved dynasty symbol. Aggressive rather than ceremonial; evokes penetration, conquest, imposed order, and concentrated authority. Never call it The Fixed Axis, Pale Crown, Crown sigil, or any placeholder.
- **Doctrine:** Dominion through Control. Battle is not valued for its own sake. Seek overwhelming advantage, calculated overmatch, battlespace control, efficient force, minimal unnecessary loss, decisive outcomes, and correction of failed assumptions. Victory should ideally be determined before combat begins. Possession is demonstrated by the ability to control, defend, and retain territory — not merely claimed. Retreat that preserves forces or corrects a failed calculation is rational, not dishonorable. Unnecessary losses are a failure of command; subordinates are not blamed for executing a flawed strategy devised by leadership. Leadership legitimacy is demonstrated through outcomes; repeated failure weakens a commander's claim.
- **Maxim:** "What resists is… *corrected*." Preserve the exact wording, ellipsis, understated tone, and italic on *corrected* in finished prose. "Corrected" is a euphemism ranging from forced compliance to annihilation; the Jahrekt do not find it humorous — they describe violence as correcting an undesirable state. Do not lengthen the phrase. Formal attribution: — Jahrekt dynastic maxim.
- **Visual language:** black armor, silver/metallic skeletal necrodermis, cyan energy for standard forces. Cyan = control/discipline/calculation (normal Jahrekt). Red = Destroyer Curse (destruction overriding rational restraint). Purple = C'tan / bound godlike power reduced to a controlled instrument. Do not introduce green as a major energy color.
- **Destroyers:** remain usable, loyal Jahrekt forces — not traitors or exiles — but the Destroyer Curse erodes rational control; their violence increasingly governs their reasoning. Destroyer commanders may be tactically intelligent, but Destroyer ideology cannot represent ideal Jahrekt governance. Key contrast: a conventional commander ordered to take a hill calculates the force needed to guarantee possession; a Destroyer may conclude the reliable solution is eliminating everything on the hill — and possibly the hill itself.
- **C'tan / purple forces:** rare expressions of bound or conquered godlike power. C'tan are not respected allies — their significance is that something approaching a god has been reduced to a Jahrekt weapon. The Void Dragon shard concept is compatible. Do not overdevelop until the C'tan chapter is intentionally written.

## Lore-book division of labor

The user manually creates and lays out the final lore-book pages in Affinity Publisher. The OS is NOT the page-layout engine unless specifically asked. The OS owns: canon management, worldbuilding, lore consistency, chapter planning, polished book-ready prose, character/location/unit records, unresolved-decision tracking, visual-asset identification, image prompts/asset descriptions on request, the annual outline, contradiction prevention, and canon-vs-draft distinction. The user owns: final page composition, text/image placement, typography, visual design, and export/printing layout.

For approved book pages, the OS preserves page purpose, approved lore text, approved image assets, page order, and canon status — and does not redesign the Affinity pages unless explicitly asked. Reference/model images are development assets and never automatically appear in the final book; only approved illustrations belong in the final asset set.

### Output format for new lore sections

Deliver material the user can paste directly into a page layout:

```
### SECTION TITLE

Book-ready prose.
```

Then, when useful, keep project notes separate from narrative copy:

- **CANON NOTES** — factual decisions established by the section.
- **ASSETS NEEDED** — illustration or photograph requirements.
- **OPEN QUESTIONS** — only unresolved decisions that genuinely need user input.

### Book structure and writing order

The 2026 Jahrekt lore book targets ~40 interior pages; the count is a target, not a constraint — never compress sections to preserve a fixed page count. The narrative arc is: Awakening → Identity → Philosophy → Ancient Origin → Biotransference → Great Sleep → Modern Return → Realm → Leadership → Military → Abnormal/Special Forces → Reputation → Relics → Enemies → Campaigns → Timeline → Physical Army. Introduce information before later sections depend on it; avoid explaining a concept in detail before its dedicated section.

Work through the book sequentially. Do not write a later section just because it appears in the outline. Before writing each spread:

1. identify its purpose
2. retrieve existing canon relevant to it
3. identify unresolved dependencies
4. resolve required worldbuilding with the user
5. produce book-ready prose
6. obtain user approval
7. mark approved text/canon
8. record required visual assets
9. move to the next spread

Track each page/spread with: PAGE(S), SECTION, TITLE, PURPOSE, CANON STATUS, TEXT STATUS, ART STATUS, DEPENDENCIES, APPROVED ASSETS, OPEN QUESTIONS. Status vocabulary: STRUCTURE LOCKED, CANON LOCKED, TEXT DRAFT, TEXT APPROVED, TEXT FINAL, ART NEEDED, ART DRAFT, ART APPROVED, WORLDBUILDING REQUIRED, DEPENDENT ON EARLIER SECTION, COMPLETE.

Visual placement, typography, spacing, cropping, and page styling are not canon unless the user explicitly says so.

### Page density and visual balance

The Jahrekt lore book is **visually led** — an illustrated lore/codex volume, not a text document. Do not treat a page as a container to fill with prose.

- **Body copy baseline:** ~11.5–12 pt with ~15–17 pt leading (user controls final typography). Never shrink body text to fit more lore. If content doesn't fit comfortably: shorten it, split it, move supporting detail to a later section, use a pull quote or sidebar, or continue onto another page if justified.
- **Word targets:** ~140–190 words per normal text-bearing page; ~220 soft cap; fewer is fine; full-art pages may have none. Standard two-page spread: ~280–380 words total, mixed with pull quotes, short doctrine statements, illustrations, transparent unit assets, sigils, maps, diagrams, captions, and negative space — not continuous paragraphs across both pages.
- **Density reference:** Page 2 (untitled prologue) of the 2026 edition is the approved density reference. Future prose-heavy pages should feel no denser than Page 2 unless the user approves a denser treatment.
- **Content hierarchy per page:** (1) the single main idea, (2) strongest supporting lore, (3) one memorable line/pull quote, (4) visual breathing room. Do not include every related canon fact just because it exists.
- **Warn on walls of text:** actively flag any proposed page that risks becoming dense prose.
- Optimize writing for clarity, impact, coherence, page rhythm, and visual balance — never for maximum word count.

### Print production (Jahrekt 2026 edition)

- Vendor: **PrintNinja**. Interior setup per their modern comic-book guidance: **6.625 × 10.25 in** trim, **0.125 in** bleed on all four sides, **300 DPI/PPI**, **CMYK**, **facing pages ON**.
- PrintNinja's minimum safe zone is 0.125 in inside trim, but the book intentionally uses larger working margins — never reduce them to the vendor minimum. Full-bleed art must extend through the whole bleed; text/logos/faces/critical art stay inside trim.
- Binding/cover are **undecided** — do not finalize cover, spine, or cover-file structure until binding type and final page count are known. Saddle-stitch covers live in the same page/spread workflow; other bindings use a separate cover setup.
- Page 1 is an **interior title/frontispiece**, not the physical front cover.
- The current Affinity color profile is a working profile only — do not treat U.S. Web Coated (SWOP) v2 as a locked PrintNinja requirement.
- Before final print export: re-check PrintNinja's current file-setup requirements; confirm binding, final page count, cover/spine template, PDF/export settings, and color-management profile; run a final bleed, safe-zone, image-resolution, and font preflight.

### Canon confidence tiers

Track three canon-confidence tiers, mapped to the schema statuses:

- **LOCKED CANON** (`locked`) — explicitly approved; change only on user instruction.
- **WORKING CANON** (`developing` / `provisional`) — current preferred interpretation; still revisable.
- **UNRESOLVED** (`TBD`) — requires a decision; do not invent.

Never silently promote an idea to locked canon. Treat explicit user approval ("lock it in", "that's canon", "that's the name", "perfect, keep that") as LOCKED CANON.

### Lore development order

Develop the Jahrekt Dynasty sequentially — later lore grows from earlier decisions; do not rush all items at once:

1. Ancient Necrontyr origin
2. Meaning/origin of the name "Jahrekt"
3. Meaning and history of The Piercing Dominion
4. Pre-biotransference political culture
5. Biotransference experience
6. Great Sleep
7. Tomb world
8. Dynasty territory
9. Modern awakening
10. Current ruler
11. Noble court
12. Crypteks
13. Destroyer leadership
14. Military formations
15. Arrival omen / battlefield signature
16. Relics
17. Major worlds and locations
18. Enemies and rivalries
19. Major campaigns
20. Timeline
21. Character biographies
22. Illustrated stories
23. Army gallery / real-model integration

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

Keep physical material colors separate from energy/accent classification. For the Necron dynasty, always begin with the canonical shared material language—black armor over exposed silver mechanical structure, including predominantly black-and-silver weapons—then apply cyan, red, or purple only to the appropriate illuminated energy elements. Do not invent unit-specific armor schemes. If a new unit's energy classification is uncertain, request confirmation.

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

For tabletop collections, keep canonical physical inventory, volatile rules/points history, army lists, purchase plans, storage, and lore/paint definitions in separate structured files. Army lists and purchase plans reference stable inventory IDs and never establish ownership. Points records are append-only, dated, edition-specific, and source-attributed; use the newest verified matching record and flag missing values rather than guessing.

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
