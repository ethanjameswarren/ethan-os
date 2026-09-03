# Skill: generate-collection-report

## Purpose

Render a lightweight, regeneratable digital report of the current hobby collection state.

## Input

- All `hobby.collection-item` records for the project.

## Output

- HTML file at `ethan-life/reports/hobby/<project>/reports/collection-report.html`.
- Summary of owned vs planned units, build/paint/magnetization progress, and acquisition gaps.

## Steps

1. Load `hobby.collection-item` records from the project directory.
2. Group by purchase status: owned, wishlist/ordered, sold/gifted.
3. Surface assembly status, painting status, and magnetization status per item.
4. List acquisition gaps: items not owned that appear in plans or unit profiles.
5. Write the HTML report and return its path.

## Rules

- This is a digital operational report, not content for the annual print lore book.
- Do not write raw points or rules text unless explicitly stored in collection items.
- Keep the report concise; do not duplicate the annual lore book.
