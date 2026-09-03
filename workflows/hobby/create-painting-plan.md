# Workflow: create-painting-plan

## Purpose

Generate a unit-specific painting plan that respects the army color scheme, owned supplies, and the user's current skill level.

## Trigger

- "Make a painting plan for the Necron Warriors."
- "How should I paint the Skorpekh Destroyers?"
- "What order do I paint the Overlord?"

## Inputs

- Collection item title or ID.

## Outputs

- New `hobby.painting-plan` Markdown file.
- Summary of paints/tools to use and any gaps requiring a purchase.

## Steps

1. Run `ethan-os/skills/hobby/generate-painting-plan.md`.
2. Confirm the visual category (Cyan / Red / Purple) and any exceptions (e.g., Flayed Ones).
3. Present the recipe and phase order. Ask for confirmation or adjustments.
4. If a required paint/tool is missing, explain why it materially improves the result or enables a required color/technique before recommending purchase.
5. Save the plan and link it to the collection item.
