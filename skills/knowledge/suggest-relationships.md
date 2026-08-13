# Skill: suggest-relationships

## Purpose

Suggest typed semantic relationships between objects.

## Input

- newly created or updated objects
- related objects from same domain

## Output

- list of proposed relationships:
  - source ID
  - target ID
  - relation type
  - justification

## Allowed relations

- sourced_from
- supports
- contradicts
- related_to
- derived_from
- applies_to
- tested_by
- revised_by
- part_of

## Instructions

- Only propose relationships with contextual justification.
- Keyword similarity alone is insufficient.
- Prefer `sourced_from` for source/capture/idea links.
- Surface contradictions explicitly.
- Do not over-link.
