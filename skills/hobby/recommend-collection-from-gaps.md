# Skill: recommend-collection-from-gaps

## Purpose

Analyze battle reports, current collection state, and canon doctrine to recommend acquisitions or list adjustments.

## Input

- All `hobby.battle-report` records.
- All `hobby.collection-item` records.
- Any doctrine canon that influences unit preferences.

## Output

- A ranked list of recommendations with rationale tied to observed events.

## Instructions

1. Read battle reports for failure patterns: anti-armor gap, mobility failure, Warrior casualties, major defeat, abnormal threat.
2. Read effective units and repeated successes.
3. Compare gaps to the existing collection and wishlist.
4. Recommend the smallest purchase that addresses the most common failure or reinforces a clear doctrine need.
5. Tie each recommendation to a specific battle or doctrine entry; do not invent a need.
6. If a recommendation would alter the project direction (e.g., Red/Purple escalation), flag it as a lore decision as well as a purchase.
7. Present options; let Ethan decide whether to add items to the collection wishlist.
