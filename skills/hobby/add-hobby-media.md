# Skill: add-hobby-media

## Purpose

Ingest an image or visual asset into a hobby project while preserving the original file, storing it in the correct assets location, and creating a reusable `hobby.media` metadata record.

## Input

- Source image file path.
- Project slug (defaults to `warhammer-40k-necron-dynasty`).
- Media type: `concept_art`, `generated_art`, `miniature_photo`, `army_photo`, `portrait`, `heraldry`, `symbol`, `diagram`, `map`, `comic_panel`, `page_decoration`, `reference_image`, `other`.
- Optional metadata: title, subject, caption, creator, generated_by, tags, faction, unit_type, color_scheme, energy_color, associated_lore_concept, canon_status, related IDs, print suitability, orientation.

## Output

- Original image copied into `ethan-life/domains/hobby/<project>/media/assets/<media-type>/`.
- `hobby.media` Markdown record in `ethan-life/domains/hobby/<project>/media/`.
- A stable `media-YYYYMMDD-HHMMSS-<slug>` ID that can be referenced by lore-book sections, narratives, collection records, painting guides, and digital reports.

## Rules

- Never modify the original image. Copy only.
- Always record provenance: source file path, creator or generator tool, rights note.
- For generated artwork, set `is_generated: true` and record `generated_by`.
- For photographs of real miniatures, set `media_type` to `miniature_photo` or `army_photo` and note that it is a real object.
- For Pale Crown/Necron images, record `color_scheme` and `energy_color` using the canonical language:
  - black-silver-cyan for normal dynasty forces
  - black-silver-red for Destroyer Curse forces
  - black-silver-purple for C'tan/Dominion forces
- Use `canon_status` to distinguish:
  - `canonical` — approved visual canon
  - `candidate` — under review for canon
  - `reference` — general visual reference (default for new uploads)
  - `unverified` — unclear origin/associations
- If the image cannot confidently be tied to a specific unit, character, event, or narrative, keep `subject`, `unit_type`, and `associated_lore_concept` general and tag it broadly.

## How to add another image later

Run:

```bash
python scripts/hobby/add_media.py --image <path> --media-type <type> --title "..." --subject "..." --tags tag1,tag2
```

Or use the `add-hobby-media` workflow.
