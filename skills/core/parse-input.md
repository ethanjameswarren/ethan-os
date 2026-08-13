# Skill: parse-input

## Purpose

Normalize messy natural-language input into a structured form without losing meaning.

## Input

- raw user text
- optional context (current task, recent captures)

## Output

- cleaned text
- inferred intent hint
- entities mentioned (sources, topics, prior objects if referenced)
- ambiguity flags

## Instructions

- Preserve the user's meaning. Do not add interpretation.
- Correct obvious spelling/grammar only when meaning is clear.
- Flag ambiguity for the intent router.
- Do not assign IDs or create objects.
