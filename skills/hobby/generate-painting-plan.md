# Skill: generate-painting-plan

## Purpose

Create a unit-specific `hobby.painting-plan` based on the user's owned supplies, current skill level, the canonical `dynasty-standard` material scheme, and the model's separate energy classification (`cyan`, `red`, or `purple`).

## Input

- `hobby.collection-item` record.
- Canonical `painting/scheme-references.yaml` definition.
- `hobby.lore-canon` visual-language entry.
- All `hobby.paint-supply` records.
- All `hobby.technique-skill` records.

## Output

- One new `hobby.painting-plan` Markdown file.
- Confirmation of paints and techniques recommended.

## Instructions

1. Load the collection record's `paint_scheme_ref` and `energy_scheme`. Require `paint_scheme_ref: dynasty-standard`; if `energy_scheme` is absent or uncertain, request confirmation rather than inferring a new scheme. Classification rules are:
   - Cyan = normal dynasty forces, nobility, Crypteks, Warriors, Immortals, Deathmarks, and normal Canoptek constructs.
   - Red = appropriate Destroyer Cult units.
   - Purple = C'tan shards and bound godlike assets; keep this classification rare.
   - Flayed Ones = separate pathology; not automatically Red.
2. Build a recipe from the shared material scheme before energy effects:
   - Black armor and armor plates.
   - Silver exposed skeletal/mechanical structure.
   - Black chest/ribcage where appropriate.
   - Predominantly black-and-silver weapons following the same armor/mechanical distinction.
   - The classified energy color only on eyes, weapon energy, power sources, symbols, conduits, and other illuminated elements.
   - Brighter/paler silver or chrome may be used on high-status areas without changing the underlying scheme.
3. Prefer owned paints and tools. Only recommend a purchase if a required color or technique is genuinely impossible with current supplies (e.g., the model needs Red energy and no red paint is owned; needs a drybrush and no drybrush is owned).
4. Sequence phases in a practical order. Include inspection checkpoints after major phases.
5. For each phase, specify:
   - exact paint/brush/tool IDs to use,
   - the technique(s) practiced,
   - what to inspect for,
   - common errors to watch for,
   - what NOT to touch yet.
6. Introduce techniques only at the user's current `comfortable` level or one step above. Do not include advanced techniques (e.g., glazing, complex wet-blending) unless earlier prerequisite techniques are already `comfortable` or `proficient`.
7. Estimate total time in minutes; break it into sessions if the plan is long.
8. Save the plan and link it to the collection item.
