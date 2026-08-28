# Skill: active-recall

## Purpose

Before explaining or supplementing a section, prompt the user to retrieve what they remember. Keep it light, not test-like.

## When to use

- At the start of a `continue-reading` workflow, before discussing the new pages.
- If the user already begins by describing what stood out, count that as active recall and skip the prompt.

## Prompts

Use natural variants. Rotate and adapt based on tone and prior sessions.

- "Before we dig into it, without looking back, what are the 1-3 things you remember most?"
- "What stuck with you from this section?"
- "If you had to summarize what you just read in a sentence or two, what would you say?"
- "Was there anything that surprised you or felt important?"
- "Honestly, how much of it do you remember right now?"

## Rules

1. Do not require a specific number of items.
2. Accept "honestly, not much" as a valid response.
3. Do not correct the user immediately; use their recall as the starting point.
4. If the user already offered observations, treat those as the recall output and move to elaboration/clarification.
5. Keep the tone conversational. This is not a quiz.
6. For fiction, recall may include characters, events, atmosphere, or questions — not just facts.

## Output

- `recall_attempt`: user's remembered points (verbatim or summarized)
- `recall_quality`: strong | partial | minimal | skipped
- `follow_up`: one useful elaboration or clarification prompt based on the recall
