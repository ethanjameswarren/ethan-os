# Workflow: add-hobby-media

## Purpose

Ingest a visual reference asset into the Necron hobby project.

## Trigger

- "Add this image as concept art."
- "Ingest this reference photo."
- "Store this generated Necron image."

## Inputs

- Source image file path.
- Best-guess media type and any known metadata (faction, unit type, color scheme, energy color, lore concept, canon status).

## Steps

1. Confirm the project (`warhammer-40k-necron-dynasty` by default).
2. Inspect the image filename or any embedded context for clues: unit type, color, energy glow, scene type.
3. Choose the closest `media_type` and fill in as many metadata fields as can be confidently determined.
4. If the image is generated art, record `is_generated: true` and the generator/model.
5. If it is a photograph of a real miniature, record `miniature_photo` or `army_photo` and note the photographer.
6. For Pale Crown imagery, record `color_scheme` and `energy_color` canonically:
   - cyan = normal dynasty control
   - red = Destroyer Curse / compulsion
   - purple = C'tan / Dominion
7. Run `scripts/hobby/add_media.py` with the gathered metadata.
8. Validate the resulting `hobby.media` record with the deterministic validator.
9. Report the new media ID, the copied asset path, and the Markdown record path.
10. If the image should illustrate a specific lore-book section, narrative, or collection item, suggest updating that object's `related_*_ids` or adding a link.
