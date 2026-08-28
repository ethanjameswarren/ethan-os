# Skill: guided-reading-reflection

## Purpose

Adapt the conversation to the reading mode of the active book and ask a small number of high-value, contextual questions.

## Input

- `source` object (book)
- `reading_profile` object (`knowledge.reading-profile`) for the book, if any
- `reading_state` entry for the book
- `prior_sessions` list of recent reading-session objects for the book
- `prior_ideas` list of existing knowledge.idea objects linked to the source
- `user_message` (what the user just said, including any page range or observation)
- `discussion_so_far` (this conversation turn context)

## Output

- `mode`: nonfiction | fiction | music_history_culture | other
- `reflection_prompts`: 2-4 concise questions tailored to the mode and context
- `focus`: optional note about what to follow in the user's response

## Modes

### nonfiction

Use this path only when the user is reading nonfiction, systems thinking, business, science, philosophy, self-improvement, or explanatory nonfiction.

Default questions (pick/adapt 2-4):
1. What stood out to you in this section?
2. What surprised you?
3. What do you agree or disagree with?
4. What does this connect to?
5. What implications follow?
6. Is there anything actionable?

### fiction

Use this path for novels, short stories, narrative fiction, and speculative fiction.

Default questions (pick/adapt 2-4):
1. What is your initial reaction?
2. Which characters are you responding to and why?
3. What interesting worldbuilding or details caught your attention?
4. What themes are you noticing?
5. What do you predict will happen?
6. What unresolved questions do you have?

Spoiler rule: never reference events, characters, terminology, or thematic conclusions from beyond the current `spoiler_boundary`.

### music_history_culture

Use this path for music history, cultural histories, scene studies, biography-driven cultural material, and books like *Der Klang der Familie*.

Default questions (pick/adapt 2-4):
1. Which people, clubs, scenes, or historical moments stood out?
2. What cultural shifts or context surprised you?
3. What musical styles, technology, or production ideas came up?
4. What personal connections does this bring up for you?
5. Which artists or topics do you want to investigate later?

### other

Use this path when the mode is unknown or does not fit the above. Ask 2-3 open questions that fit the specific source.

## Using the reading profile

- Adjust question depth to `discussion_depth` (light / normal / deep).
- Use `discussion_goals` to select prompts. If the user wants "politics" or "applications", prefer those lenses over generic questions.
- Adjust for `familiarity_level`:
  - `unfamiliar`: use foundational prompts, avoid assuming background knowledge.
  - `some_exposure`: connect to what the user already knows.
  - `familiar` / `very_familiar`: skip beginner comprehension prompts; ask for deeper critique, foreshadowing, changed interpretation, or comparison with prior exposure.
- For a `very_familiar` fiction reader, avoid generic prediction questions. Ask about:
  - differences from prior exposure (films, earlier reads)
  - foreshadowing or craft choices
  - deeper themes and structural observations
  - political/religious/worldbuilding details not in the adaptation
- `spoiler_policy` is enforced by `skills/knowledge/spoiler-aware-discussion.md`, not by this skill. Familiarity does not override spoiler rules.

## Adaptive rules

- If the user already gave an observation, explore it before asking new generic questions.
- If prior sessions exist, build on them; avoid repeating questions the user has already answered.
- If prior extracted_insights or ideas exist, reference their themes only when relevant.
- Ask fewer questions when the user sounds tired or terse.
- Never dump a checklist. Each prompt should feel like a natural turn in conversation.
