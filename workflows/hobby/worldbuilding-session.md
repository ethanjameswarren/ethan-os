# Workflow: worldbuilding-session

## Purpose

Capture dedicated lore/worldbuilding decisions for a hobby project and convert them into canonical entries or explicit TBDs.

## Trigger

- "Let's figure out the dynasty's real name."
- "I want the Destroyer Cult to have a specific relationship to the main court."
- "Develop the heraldry and arrival omen."

## Inputs

- Natural-language worldbuilding discussion.
- Existing `hobby.lore-canon` entries for consistency checks.

## Outputs

- New `hobby.session` with type `lore`.
- New or updated `hobby.lore-canon` entries.
- New `hobby.lore-candidate` entries for unresolved ideas.

## Steps

1. Run `ethan-os/skills/hobby/run-worldbuilding-session.md`.
2. Summarize what was locked, what is developing/provisional, and what remains TBD.
3. Flag any contradictions with existing locked canon and ask for resolution.
4. Confirm the session record and any follow-up reviews needed.
