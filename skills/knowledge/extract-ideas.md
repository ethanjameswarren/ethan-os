# Skill: extract-ideas

## Purpose

Extract atomic, reusable ideas from a capture or source.

## Input

- capture object or source text
- source object (if known)

## Output

- list of candidate ideas with:
  - claim
  - interpretation (optional)
  - position (agree/disagree/neutral/exploring)
  - confidence
  - reasoning

## Instructions

- Extract only atomic concepts that remain useful outside the source.
- Do not create an idea for every sentence.
- Preserve source claim separately from interpretation.
- Record Ethan's position if expressed; otherwise default to `exploring`.
- Flag uncertainty honestly.
