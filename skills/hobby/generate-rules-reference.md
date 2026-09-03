# Skill: generate-rules-reference

## Purpose

Render a lightweight, regeneratable reference for current tabletop rules, points, stats, and abilities.

## Input

- Stored rules or list data for the project (e.g., codex edition, points values, datasheets).
- If no structured rules data exists, the report explains what is missing.

## Output

- HTML file at `ethan-life/reports/hobby/<project>/reports/rules-report.html`.
- Snapshot of the current rules state with effective date and provenance.

## Steps

1. Load any available rules/points data for the project.
2. If none is stored, generate an empty report that lists what should be captured.
3. Display edition, points totals, key stat references, and ability notes.
4. Label effective date and source.
5. Write the HTML report and return its path.

## Rules

- Rules are volatile and dynamic. This report is not included in the annual print lore book.
- Do not present rules as permanent lore.
- When in doubt, ask the user for the current edition/points rather than guessing.
