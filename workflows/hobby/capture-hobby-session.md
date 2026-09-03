# Workflow: capture-hobby-session

## Purpose

Record a hobby activity (build, paint, lore, planning, photo, etc.) and update the canonical collection state.

## Trigger

Say something like:

- "I primed the Necron Warriors today."
- "Spent two hours building the Skorpekh Destroyers."
- "Named my Lokhust Heavy Destroyer and decided its kill tally matters."
- "Planning session: I want the dynasty's official name to mean something like irresistible dominion."

## Inputs

- Natural-language session description.
- Existing `hobby.collection-item` records in `ethan-life/domains/hobby/<project>/collection/`.

## Outputs

- New `hobby.session` Markdown file.
- Updated collection-item files.
- Optional `hobby.lore-candidate` files.

## Steps

1. Run `ethan-os/skills/hobby/capture-hobby-session.md`.
2. Ask to confirm any status changes that were inferred.
3. Offer to generate lore candidates if the session produced a narrative idea.
4. Return a concise summary of what was recorded.
