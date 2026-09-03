# Workflow: capture-battle-result

## Purpose

Turn a tabletop game into a canonical battle report and surface candidate lore.

## Trigger

- "I played a 500pt game against Orks and tabled them in turn 3."
- "My Warriors got wiped by a Predator and I lost."
- "Draw against Aeldari; the Wraiths saved me."

## Inputs

- Natural-language battle summary.
- Collection item IDs of units used.

## Outputs

- New `hobby.battle-report` file.
- Updated collection item `battles_participated` arrays.
- Optional `hobby.lore-candidate` files for notable events.

## Steps

1. Run `ethan-os/skills/hobby/capture-battle-result.md`.
2. Ask whether any unit deserves a nickname, honor, or correction narrative.
3. Offer to generate lore candidates now.
4. If the result suggests a collection gap, offer `recommend-collection-from-gaps`.
5. Return a short battle summary and any candidate IDs.
