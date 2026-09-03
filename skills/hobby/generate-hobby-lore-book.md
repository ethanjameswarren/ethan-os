# Skill: generate-hobby-lore-book

## Purpose

Render a print-oriented annual lore book from curated `hobby.lore-canon`, `hobby.lore-book-section`, `hobby.media`, and `hobby.narrative` records without modifying source files. Raw battle reports, collection status, points, and session logs are excluded unless explicitly promoted into canon.

## Input

- `hobby.lore-book-section` outline and section records.
- `hobby.lore-book-edition` metadata for the target edition.
- Selected `hobby.lore-canon`, `hobby.media`, and `hobby.narrative` sources.

## Output

- A rendered HTML file (and optionally PDF) written to a versioned build directory such as `ethan-life/reports/hobby/<project>/lore-book/<year>/lore-book.html`.
- A summary of included, TBD, and excluded sections plus visual/media gaps.

## Instructions

1. Load the target edition metadata. If none is specified, render a `draft` of the current year.
2. Load the master outline and any additional `hobby.lore-book-section` records.
3. Include only sections with status `complete`, `reviewing`, or `drafting`. Omit sections that are `TBD`, `excluded`, or empty unless explicitly marked for inclusion with a placeholder note.
4. For each included section, pull content from linked `hobby.lore-canon`, `hobby.media`, and `hobby.narrative` entries. Do not pull raw `hobby.battle-report` or `hobby.collection-item` data unless a canon entry explicitly references it.
5. Mark `TBD` sections as "intentionally unresolved" rather than leaving blank pages.
6. Preserve provenance: cite canon/media IDs for quotes, captions, and narrative excerpts.
7. Build a visual-opportunity list from required/recommended media that is missing or placeholder.
8. Produce a print-oriented HTML page: fixed page dimensions, page-break hints, safe zones, chapter openers, and headers/footers.
9. Do not invent missing lore. Output the rendered file and report included, omitted, and blocked sections.

## Output structure

```text
reports/hobby/<project>/lore-book/<year>/
    source/
        lore-book-edition.md
    lore-book.html
    lore-book.pdf (if generated)
```

## Relationship types

- `generated_from` — the rendered edition is derived from the edition object, outline, and canon/media records.
