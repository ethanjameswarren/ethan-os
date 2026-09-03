# Skill: generate-battle-chronicle

## Purpose

Render a lightweight, regeneratable digital chronicle of tabletop battles.

## Input

- All `hobby.battle-report` records for the project.
- Any linked `hobby.lore-candidate` or `hobby.lore-canon` IDs.

## Output

- HTML file at `ethan-life/reports/hobby/<project>/reports/battles-report.html`.
- Chronological table of battles with opponents, outcomes, points, scenarios, summaries, and lore-candidate status.

## Steps

1. Load all `hobby.battle-report` records.
2. Sort by `played_date` (most recent last).
3. For each battle, display date, opponent faction, result, points, scenario, and a short summary.
4. Highlight battles that generated `lore_candidate_ids` but have not yet been promoted to canon.
5. Note any `canon_update_ids` that have already been promoted.
6. Write the HTML report and return its path.

## Rules

- This report is operational/digital only. Battle results do not enter the annual lore book unless promoted through the lore-candidate review pipeline.
- Do not invent details missing from the battle report.
- Preserve the win/loss record as recorded, without commentary unless requested.
