# Skill: perform-review

## Purpose

Conduct a retrieval-focused review of a reading-derived retention item.

## Principles

- Test retrieval, not recognition.
- Prefer generation and explanation over multiple-choice answers.
- Evaluate the underlying concept, not exact wording.
- Keep the experience conversational and low-pressure.

## Review prompts

Use the source, prior sessions, and the retention item title to craft a prompt that requires the user to reconstruct the idea.

Examples:

- Nonfiction: "A few days ago you connected feedback loops to labor planning. What was the connection?"
- Nonfiction: "Without checking your notes, explain Meadows' stock/flow distinction."
- Fiction: "What do we know about the Bene Gesserit so far, and why do you find them suspicious?"
- Fiction: "What prediction did you make about the Atreides family at page 35?"

## Evaluation

After the user responds, classify semantically:

- `strong`: core idea recalled accurately; may use their own words.
- `partial`: part recalled, but an important piece missing or shaky.
- `failed`: cannot recall or substantially wrong.

Do not score on exact phrasing. Ask a brief follow-up only if needed to disambiguate `partial` vs `failed`.

## Response to outcomes

- `strong`: acknowledge, briefly reinforce if useful, then schedule next review with longer interval.
- `partial`: acknowledge what was retained, ask/teach the missing component, schedule moderate interval.
- `failed`: no guilt. Help reconstruct the idea from the source or prior discussion, then schedule sooner review.

## Spoiler protection

For fiction, ensure the review prompt and any follow-up material do not reference content beyond the user's configured spoiler boundary.

## Output

- `recall_result`: strong | partial | failed | skipped
- `notes`: brief note on what the user recalled or missed
- Updated retention item scheduled via `skills/knowledge/schedule-review.md`
