# Skill: manage-warhammer-collection

## Purpose

Manage canonical Warhammer 40,000 inventory, points, army lists, purchases, storage, and inventory reconciliation while preserving strict data-layer boundaries.

## Canonical files

Resolve the hobby project under `ethan-life/domains/hobby/<project>/`, then load:

- `collection/inventory.yaml`: physical ownership and model state only.
- `rules/points.yaml`: append-only, dated points records.
- `army-lists/lists.yaml`: lists referencing collection `unit_id` values.
- `purchases/plan.yaml`: planned and ordered acquisitions.
- `storage/locations.yaml`: case, tray/layer, and optional slot definitions.
- `painting/scheme-references.yaml`: canonical shared material scheme and energy classifications.

Never infer ownership from old prose, army lists, prior estimates, points, or purchase plans. `quantity_owned` is authoritative. Planned and ordered quantities are not owned.

## Supported intents

Show, add, remove, or update models; mark assembly and paint progress; update paint status, wargear/build, storage, and points; manage planned/ordered/received purchases; calculate collection points; build, compare, and generate lists; report missing or unused models; and recommend purchases based on list flexibility.

Use `python ethan-os/scripts/hobby/warhammer_collection.py --project <project-path>` for deterministic operations:

- `validate`
- `points`
- `list-status [--list-id ID]`
- `reconcile --input <yaml>` for a preview; add `--apply` only after confirmation.
- `receive <unit_id> <quantity>` only for a matching ordered purchase.

## Invariants

- Enforce `0 <= quantity_painted <= quantity_assembled <= quantity_owned`.
- Statuses may include `planned`, `ordered`, `owned`, `assembled`, `primed`, `painting`, and `painted`, but quantities remain authoritative.
- Build/wargear belongs on collection records; rules text and points do not.
- Every unit references `paint_scheme_ref: dynasty-standard` and separately records `energy_scheme: cyan`, `red`, or `purple`.
- Cyan is the default for standard dynasty forces, red is for appropriate Destroyer Cult units, and purple is reserved for C'tan/god-associated exceptional entities. If classification is uncertain, ask rather than inventing a scheme.
- Energy colors apply to illuminated effects over the shared black-armor/silver-mechanical material scheme; they are not alternate armor colors.
- Storage references must resolve to a location ID.
- Lists must require no more than owned quantities; explicitly report shortages.
- Preserve stable `unit_id` references.

## Points

Never guess points and never overwrite history. Each points record requires `unit_id`, `value`, `unit_size`, `verified_date`, `rules_edition`, and `source`, plus `source_version` when known. Calculations use the newest verified record matching unit and size. Missing or uncertain values must be flagged for verification.

## Inventory reconciliation

1. Load canonical inventory.
2. Normalize user-provided inventory to stable unit IDs.
3. Preview additions, removals, quantity differences, and uncertain fields.
4. Ask for confirmation when the preview changes canonical state.
5. Apply the confirmed baseline.
6. Recalculate verified collection points.
7. Revalidate every saved list.
8. Report lists broken by ownership or points changes.

## Purchases and flexibility

Rank candidates primarily by the number and meaningful diversity of legal lists they enable, then by useful substitutions and role coverage. Record evidence in `units_enabled`, `lists_enabled`, and `strategic_reason`. Do not recommend a model because it is popular. Never buy anything.

When the user says they bought a planned model, distinguish `ordered` from physically `received`. Receiving moves only the received quantity into inventory, reduces or completes the purchase entry, recalculates totals, and revalidates lists.

## List generation

Generate lists only from confirmed owned quantities and newest verified points. Different lists must have meaningfully different plans, not cosmetic swaps. Explain purpose, substitutions, missing models, points requiring verification, storage locations, and unused owned units. Save lists only with user approval.
