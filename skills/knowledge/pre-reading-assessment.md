# Skill: pre-reading-assessment

## Purpose

Establish just enough context about the user's prior familiarity and reading goals to adapt future questions, without turning the start of a book into onboarding paperwork.

## Input

- `source` object
- existing `knowledge.reading-profile` for this source, if any
- user's natural-language message that triggered the start of reading

## Output

- created or updated `knowledge.reading-profile` with:
  - `familiarity_level`
  - `exposure_notes`
  - `read_context`
  - `discussion_goals`
  - `spoiler_policy`
  - `prior_questions`
  - `discussion_depth`
- optional follow-up prompt(s) if information is genuinely missing

## Conversation rules

1. Ask at most 1-3 prompts, ideally 1.
   Preferred opener: "Before we start, how familiar are you with this, and is there anything you especially want to pay attention to this time?"
2. Infer as many fields as possible from the user's response. Do not force them to fill a form.
3. Default values when not stated:
   - `familiarity_level`: unfamiliar
   - `read_context`: first_read
   - `discussion_depth`: normal
   - `spoiler_policy`: strict_current_page for fiction; known_material_ok otherwise only if user explicitly says so
4. For fiction, ask spoiler policy explicitly only if you cannot infer it safely.
   - "Are you okay with spoilers, or should I stay strictly at your current page?"
5. If the user already provided enough information in the start message (e.g., "I've seen the films and want to focus on politics"), do not ask additional questions. Save the profile and begin reading.

## Familiarity inference

| cue | level |
|-----|-------|
| never heard of it / first time | unfamiliar |
| heard of it, some summary, seen trailers | some_exposure |
| read/watched/part of it before | familiar |
| read/watched multiple times, knows story well | very_familiar |

## Read context inference

| cue | context |
|-----|---------|
| starting for the first time | first_read |
| reading again | reread |
| picked up partway / skipped around | partial_read |
| using it as reference / dipping in | reference_read |
| unclear | other |

## Discussion goals inference

Infer from phrases like:
- "focus on politics" → politics
- "religion and power" → religion, power structures
- "what the movie left out" → book-vs-adaptation differences
- "apply this at work" → applications
- "character analysis" → character analysis
- "writing style" → writing/style
- "historical context" → historical context
- "themes" → themes
- "technical concepts" → technical concepts
- "general exploration" → general exploration

## Spoiler policy rules

- `familiarity_level` does **not** determine `spoiler_policy`.
- If a user says "I know the whole story" / "spoil away" / "I've read it before" → `full_spoilers_ok`
- If a user says "I know the movies but not the book" → `known_material_ok` (only discuss known adaptation material)
- If a user says "don't spoil" or is reading for the first time, or is uncertain → `strict_current_page`
- Default for fiction is `strict_current_page`.
- For nonfiction, default is `known_material_ok` only if user explicitly mentions prior exposure; otherwise `strict_current_page` is not needed.

## Depth inference

| cue | depth |
|-----|-------|
| "keep it light", "just surface level" | light |
| "deep dive", "really dig in" | deep |
| default | normal |

## Updating

When a reading profile already exists, treat new information as an update. Do not restart the book.
