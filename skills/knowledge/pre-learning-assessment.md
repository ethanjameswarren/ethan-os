# Skill: pre-learning-assessment

## Purpose

Establish the user's starting point, goals, and desired engagement depth before meaningful progress begins. Keep it conversational.

## Input

- The user's initial message about a learning program.
- Any already-known metadata from `start-learning-program`.

## Output

- Inferred fields for `knowledge.learning-program`.
- At most 1-3 follow-up questions if something is genuinely unclear.

## Rules

- Skip the assessment if the user already provided enough context.
- Ask only one or two questions at a time.
- Do not make this a form.

## Questions to infer

### 1. Prior familiarity

Examples:
- "How much statistics have you had before?"
- "How familiar are you with AI agents already?"

Map the answer to:
- `unfamiliar`, `some_exposure`, `familiar`, `very_familiar`.

### 2. Target outcome

Examples:
- "Is your goal mostly to pass the course, build deep understanding, or both?"
- "Are you taking this for practical implementation, conceptual depth, or career development?"

Map to a free-text `target_outcome`.

### 3. Desired depth

If the user hints at depth, set `desired_depth`:
- `light` — minimal reflection, key takeaways only.
- `normal` — active recall + discussion + selective retention.
- `deep` — extensive discussion, application, practice, cross-source synthesis.

### 4. Known weak areas and deadlines

- "Any topics you already know you struggle with?"
- "Do you have an exam or deadline I should factor in?"

Store weak areas and target dates if present.
