# Workflow: print-record-labels

## Purpose

Build and render an Avery 5160 print batch from label-ready entities, supporting partial sheets.
Generating the file is not printing — nothing is marked printed here; that happens in
`mark-record-labels` after Ethan confirms.

## Trigger

- `Give me everything that's ready to print.`
- `Make a sheet starting at label 11.`
- `Print labels for RYCL016.`
- `Reprint the label for SK11X015-A1.`

## Inputs

- Ethan's scope/instruction (all ready entities, a specific release/track, a starting position,
  or an explicit reprint request)
- `ethan-life/data/music/record-collection/albums.csv`
- `ethan-life/data/music/record-collection/tracks.csv`
- `ethan-life/data/music/record-collection/physical_label_status.csv`
- `ethan-life/data/music/record-collection/print_batches.csv` (for `batch_id` numbering)

## Outputs

- New batch directory `ethan-life/data/music/record-collection/print-batches/<batch_id>/` with
  `sheet.tex` (and `sheet.pdf` if compilable)
- New row in `print_batches.csv` (`confirmed_printed` left blank)

## Steps

### 1. Determine the entity set

- Default: run `evaluate-label-readiness` (via `audit-record-labels`'s grouping) and select
  everything in the "Ready to print" group.
- If Ethan scopes to a specific release/track, use that instead (still checked for readiness —
  warn if it isn't actually `printable`/`complete` and ask whether to proceed anyway).
- Only include entities with `print_status: not_printed`, unless Ethan explicitly asks for a
  reprint of something already printed.

### 2. Determine the starting position

Default `sheet_start_position: 1`. If Ethan specifies a starting label number (e.g. "starting at
label 11" for a partially-used sheet), use that.

### 3. Assign a batch ID

`batch-YYYYMMDD-NNN` — next sequence number for the day in `print_batches.csv`.

### 4. Render the sheet

Run `ethan-os/skills/music/render-avery-5160-sheet.md` with the entity set, starting position, and
`batch_id`.

### 5. Record the batch

Append a row to `print_batches.csv`: `batch_id`, `generated_at`, `sheet_start_position`,
`entity_ids` (semicolon-separated, in print order), `tex_path`, `pdf_path` (blank if not
compiled), `confirmed_printed` blank, `confirmed_printed_at` blank.

### 6. Report to Ethan

State: how many labels, how many sheets, the starting position, the file path(s), and that nothing
has been marked printed yet — printing is confirmed separately via `mark-record-labels` (e.g.
"Those are printed.").

## Confirmation policy

- Auto-execute: selecting ready entities, rendering the sheet, recording the batch.
- Ask for confirmation: printing an entity that isn't fully `printable`/`complete` (missing
  desired data will show as blank on the label), and explicit reprints of already-printed labels.
