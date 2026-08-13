# Skill: suggest-review

## Purpose

Surface items worth revisiting.

## Input

- all knowledge objects
- review frequency policy

## Output

- list of review candidates with reason:
  - low_confidence
  - stale (old with weak understanding)
  - disconnected (few relationships)
  - contradictory
  - manually flagged

## Instructions

- Prefer quality over quantity.
- Surface genuine uncertainty and contradictions first.
- Do not flood with low-value items.
- Return concise actionable list.
