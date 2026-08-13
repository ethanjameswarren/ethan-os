# Skill: resolve-references

## Purpose

Resolve mentions of existing objects to stable IDs.

## Input

- parsed user input or generated object
- set of existing objects in `ethan-life`

## Output

- list of matched IDs with confidence
- list of unresolved mentions
- recommendation: link existing, create new, or ask

## Instructions

- Match by title, aliases, or semantic similarity.
- Prefer linking existing objects over creating duplicates.
- If uncertain, flag for confirmation.
- Never invent IDs.
