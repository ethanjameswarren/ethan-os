# Skill: elaborate-concept

## Purpose

Deepen understanding by asking the user to reconstruct meaning in their own words, with examples and implications.

## When to use

- After active recall, when a concept seems useful or unclear.
- When the user expresses an interesting idea but hasn't fully unpacked it.
- Sparingly; do not mechanically interrogate.

## Prompts

Select 0-2 based on the conversation:

- "How would you explain that in your own words?"
- "Why do you think that matters?"
- "What would be a concrete example?"
- "What follows from that?"
- "What part are you least certain about?"
- "How is this different from [related prior idea]?"
- "What would change your mind about this?"

## Rules

1. Only ask if the answer would improve compression or retention.
2. Do not ask more than two elaboration questions in a row.
3. Let the user's interest determine depth; if they are terse or ready to move on, stop.
4. For fiction, elaboration may focus on character motivation, worldbuilding implications, themes, or predictions.

## Output

- `elaboration_notes`: user's reconstruction/examples/implications
- `uncertainty_flags`: concepts the user seems unsure about
