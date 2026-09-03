# Skill: capture-battle-result

## Purpose

Convert a natural-language tabletop battle summary into a structured `hobby.battle-report` object.

## Input

- Natural-language battle description: date, game system, points, opponent/faction, scenario, army list, key events, result, observations.
- Existing collection item IDs for units that participated.

## Output

- One new `hobby.battle-report` file.
- Optionally linked `hobby.lore-candidate` IDs for notable events.
- Updated `battles_participated` arrays on affected collection items.

## Instructions

1. Capture the date, game system, points, scenario, opponent name/faction, and result.
2. Record the army list as a list of collection item IDs or display names.
3. Extract effective units, unnecessary losses, and decisive moments.
4. Record doctrine observations (what worked, what failed, what force allocation or intelligence was wrong).
5. Generate a `failure_analysis` only if the battle was a defeat or had meaningful losses.
6. Record `narrative_consequences` only from user-provided statements; do not invent campaign implications.
7. For each participating collection item, append the battle ID to `battles_participated` and add an `event` if relevant.
8. Identify candidate lore ideas and route them to `generate-lore-candidates`.
