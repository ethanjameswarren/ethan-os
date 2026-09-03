# Workflow: generate-hobby-lore-book

## Purpose

Render a print-oriented annual lore book for a hobby project from curated canon, sections, media, and narratives.

## Trigger

- "Render the current Necron lore book."
- "Generate the current dynasty book."
- "Create the 2026 print edition."
- "I want to see what's ready for the book so far."

## Inputs

- `hobby.lore-book-edition` metadata for the target edition (defaults to current-year draft if omitted).
- `hobby.lore-book-section` outline and section records.
- Selected `hobby.lore-canon`, `hobby.media`, and `hobby.narrative` records.

## Outputs

- Print-oriented HTML rendered to `ethan-life/reports/hobby/<project>/lore-book/<year>/lore-book.html`.
- Optional PDF in the same directory.
- Summary of included, omitted, and TBD sections plus visual/media gaps.

## Steps

1. Decide whether the user wants:
   - a **draft/current render** of the latest state, or
   - a **frozen annual edition** (e.g., Edition 2026).
2. For an annual edition, create or update the `hobby.lore-book-edition` object with status `finalized` and set `generated_date`.
3. Run `ethan-os/skills/hobby/generate-hobby-lore-book.md`.
4. Run the rendering script (`scripts/hobby/generate_lore_book.py`) with `--edition 2026` (or current year) and `--life-dir <ethan-life>`.
5. Write the output to the edition build directory; do not modify canonical source files.
6. Report included sections, omitted empty/TBD sections, and the visual-opportunity checklist.
7. Offer to start a worldbuilding or media-capture session for any blocking gap.

## Edition distinction

- **Draft/current render**: overwrites `.../lore-book/<year>/lore-book.html` in place; `edition_status` stays `draft`.
- **Finalized annual edition**: copies the source snapshot into the edition directory, sets `edition_status` to `finalized`, and preserves it. Later lore changes do not alter a finalized edition.
