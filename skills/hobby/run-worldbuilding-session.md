# Skill: run-worldbuilding-session

## Purpose

Capture a dedicated worldbuilding/lore conversation as structured `hobby.session`, `hobby.lore-canon`, and `hobby.lore-candidate` objects.

## Input

- Natural-language discussion about the project's setting, characters, doctrine, visuals, or factions.
- Existing `hobby.lore-canon` entries to avoid silent contradictions.

## Output

- One `hobby.session` file describing the worldbuilding session.
- New or updated `hobby.lore-canon` entries.
- Any unresolved ideas saved as `hobby.lore-candidate` with status `proposed`.

## Instructions

1. Create a session record with `session_type: lore`.
2. For each firm decision, create or update a `hobby.lore-canon` entry:
   - Mark as `locked` only when Ethan explicitly says it is final.
   - Otherwise mark as `developing` or `provisional`.
3. For unresolved or tentative ideas, create `hobby.lore-candidate` records with `status: proposed`.
4. Explicitly mark unknown elements as `TBD` in the relevant canon entry rather than inventing content.
5. Check against existing locked canon; surface any contradiction for resolution.
6. Summarize what was decided, what was left TBD, and what now needs review.
