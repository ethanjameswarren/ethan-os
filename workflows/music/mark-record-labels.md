# Workflow: mark-record-labels

## Purpose

Record the physical-world facts that only Ethan can confirm: a batch was actually printed, a
label was applied to a sleeve, a color sticker was applied, or a BPM was handwritten. This is the
only place `physical_label_status.csv`/`print_batches.csv` get marked complete.

## Trigger

- `Those are printed.`
- `Mark RYCL016's label as applied.`
- `SK11X015-A1 has its sticker now.`
- `I wrote the BPM on A1.`

## Inputs

- Ethan's confirmation, referencing a batch (`batch_id`, or "that"/"those" from context) or
  specific entities
- `ethan-life/data/music/record-collection/print_batches.csv`
- `ethan-life/data/music/record-collection/physical_label_status.csv`

## Outputs

- Updated `physical_label_status.csv` rows (created if they don't exist yet)
- Updated `print_batches.csv` row (`confirmed_printed`, `confirmed_printed_at`) when confirming a
  batch print

## Steps

### 1. Resolve the target

- A batch reference (most recent batch from context, or an explicit `batch_id`) → applies to every
  `entity_id` in that batch.
- A specific release/track reference → applies to just that entity.

### 2. Apply the confirmed action

- **Printed**: set `label_printed: true`, `print_batch_id`, `last_printed_at` on each affected
  `physical_label_status.csv` row (creating the row if it's the entity's first physical touch);
  set `confirmed_printed: true` and `confirmed_printed_at` on the `print_batches.csv` row.
- **Applied**: set `label_applied: true`, `last_applied_at`.
- **Sticker applied**: set `sticker_color_applied: true` (track-only).
- **BPM written**: set `bpm_written: true` (track-only).

Multiple confirmations may apply at once (e.g. "those are printed and applied").

### 3. Update audit timestamp

Set `last_audited_at` to now on every row touched.

### 4. Confirm back to Ethan

State exactly what was marked and for how many entities.

## Constraints

- Never set `label_printed`/`confirmed_printed` except from this workflow, and never as a side
  effect of `print-record-labels` generating a file.
- Never infer that a label was applied because it was printed, or that a sticker/BPM was done
  because a label was printed — these are independent facts.

## Confirmation policy

- Auto-execute: recording any of these confirmations once Ethan states them plainly. These are
  Ethan reporting his own completed physical actions, not the AI inferring anything, so no
  additional confirmation step is needed.
