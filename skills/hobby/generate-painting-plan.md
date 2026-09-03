# Skill: generate-painting-plan

## Purpose

Create a unit-specific `hobby.painting-plan` based on the user's owned supplies, current skill level, the dynasty's canonical color scheme, and the model's visual category (Cyan / Red / Purple).

## Input

- `hobby.collection-item` record.
- `hobby.lore-canon` visual-language entry.
- All `hobby.paint-supply` records.
- All `hobby.technique-skill` records.

## Output

- One new `hobby.painting-plan` Markdown file.
- Confirmation of paints and techniques recommended.

## Instructions

1. Determine the model's visual category from `tags` / collection item notes / linked lore:
   - Cyan = normal dynasty forces, nobility, Crypteks, Warriors, Immortals, Deathmarks, normal Canoptek constructs.
   - Red = Destroyer Cult units.
   - Purple = C'tan shards / bound godlike assets.
   - Flayed Ones = separate pathology; not automatically Red.
2. Build a recipe that always includes:
   - Black armor base.
   - Silver mechanical structure.
   - Brighter/paler silver or chrome on high-status areas.
   - The appropriate energy color (Cyan, Red, or Purple).
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
