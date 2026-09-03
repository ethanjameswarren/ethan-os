# Skill: audit-lore-contradictions

## Purpose

Scan `hobby.lore-canon`, `hobby.lore-candidate`, and `hobby.collection-item` records for contradictions, deprecated placeholders, or lore drift.

## Input

- All `hobby.lore-canon` and `hobby.lore-candidate` files.
- Optional list of known placeholder names that must remain non-canon (e.g., concept-art names).

## Output

- A structured audit report: contradictions, deprecated entries, TBD items, orphaned candidates, collection items with lore gaps.

## Instructions

1. List all canon entries and their statuses.
2. Identify `locked` entries and ensure later entries do not contradict them unless marked `contradicted` or `deprecated`.
3. Flag any `deprecated` or `contradicted` entry that lacks a `deprecated_reason`.
4. List `TBD` fields as expected gaps, not errors.
5. List `proposed` candidates older than a reasonable horizon (e.g., 30 days) as stale review items.
6. List known placeholder names found in canon content and mark them for deprecation.
7. Recommend the next reconciliation action.
