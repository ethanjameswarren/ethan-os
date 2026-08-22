# Skill: render-avery-5160-sheet

## Purpose

Turn an ordered list of album/track entities into a print-ready `.tex` file using
`ethan-os/templates/avery-5160.sty`, handling blank fields, text fitting, ordering, and partial
sheets, then attempt a PDF compile if the environment supports it.

## Input

- `entities`: ordered list of `{entity_type, entity_id}` to print, already filtered to
  `printable`/`complete` and not-yet-printed by the calling workflow (see
  `evaluate-label-readiness`)
- `sheet_start_position`: 1-30 (default 1)
- `albums`, `tracks`: canonical rows needed to render content
- `batch_id`: `batch-YYYYMMDD-NNN`, assigned by the calling workflow

## Output

- `tex_path`: `ethan-life/data/music/record-collection/print-batches/<batch_id>/sheet.tex`
- `pdf_path`: same directory, `sheet.pdf`, if compilation succeeded; otherwise `null` with a note
  that Ethan needs a LaTeX toolchain to compile the `.tex` locally
- `label_count`: number of labels placed
- `sheets_used`: number of physical sheets the batch spans

## Instructions

### 1. Preserve canonical ordering

Order: album label, then that album's tracks in `Track ID`/side order (A1, A2, B1, B2, ...), for
each release in the batch, in the order the calling workflow provided them. If multiple releases
share a sheet, keep each release's labels contiguous — never interleave tracks from different
releases.

### 2. Build each label's content string

**Album** (`\LabelTitle{}` / `\LabelMeta{}` / `\LabelBody{}` per
`templates/avery-5160-README.md`):

- Title line: `"<Year> - <Album>"`. If `Year` is blank, omit the `"<Year> - "` prefix entirely —
  print just `<Album>` (never a stray dash or blank year).
- Meta line: `"<Release> | <Label>"`. If `Label` is blank, print just `<Release>`.
- Metrics line: `"BPM: <Avg BPM> | Energy: <Avg Energy> | Rating: <Avg Rating>"`, from
  `evaluate-label-readiness`'s computed averages. Omit any of the three segments whose average is
  blank (no tracks had a value); omit the entire line only if all three are blank.
- Comment line: the album's `Comment` (Hard Wax-style), shortened per step 4 if needed. Omit
  entirely if blank — do not print an empty line in its place.

**Track**:

- Title line: `"<Energy> - <Track>"`. If `Energy` is blank, print just `<Track>` (no leading dash).
- Meta line: `<Artist>`.
- Tag line: up to 2 tags from `Tags`, `/`-joined (e.g. `"Boomy / Atmospheric"`). If more than 2
  tags exist, take the first 2 in their existing order — never reorder to "pick the best" ones,
  since that would be interpretation, not formatting. Omit the line if `Tags` is blank.
- Comment line: the track's `Comment`, shortened per step 4 if needed. Omit if blank.

### 3. Never omit identifying information

Regardless of space constraints, always include: the track/album title, and the
release/catalog number (on the album label) or artist (on the track label). These are never
shortened past recognizability and never dropped.

### 4. Fit `Comment` text to the label

The label body has roughly 4-5 lines of small type available after the title/meta/tag lines.
Apply, in order:

1. Print the full `Comment` if it fits.
2. If not, wrap it naturally (LaTeX will do this within the fixed-width `minipage`) — this alone
   is often sufficient.
3. If it still would overflow the available vertical space (estimate: more than ~120 characters
   for a track label with a tag line present, ~150 without; more than ~140 for an album label),
   shorten prose by trimming trailing clauses at a sentence or clause boundary (period, semicolon,
   or comma) rather than mid-word, and append `…`.
4. Only as an absolute last resort, hard-truncate at a word boundary and append `…`.

This shortening is print-rendering only — never write the shortened text back into `tracks.csv` or
`albums.csv`; the canonical `Comment` cell is untouched.

### 5. Escape LaTeX special characters

Escape `& % $ # _ { } ~ ^ \` in every field value before inserting it into the `.tex` content
(e.g. `&` → `\&`), since track/artist/comment text may contain them.

### 6. Render the file

Write `\LabelStartAt{<sheet_start_position>}` followed by one `\PrintLabel{...}` per entity in
order, wrapped in the standard `\documentclass{article}\usepackage{avery-5160}...\begin{document}
...\end{document}` structure shown in `templates/avery-5160-sheet.tex`. Save to
`ethan-life/data/music/record-collection/print-batches/<batch_id>/sheet.tex`.

### 7. Attempt compilation

If a LaTeX toolchain is available in the environment, compile to
`print-batches/<batch_id>/sheet.pdf`. If not, report the `.tex` path and tell Ethan he'll need to
compile it locally (e.g. `pdflatex sheet.tex` with `ethan-os/templates/avery-5160.sty` on the
include path) — do not treat compilation failure/unavailability as a workflow failure.

## Constraints

- Never fabricate a field value to fill visual space.
- Never reorder labels across releases to "optimize" the sheet layout.
- Never mark anything printed as a side effect of rendering — that is a separate, explicit step in
  `print-record-labels`/`mark-record-labels`.
