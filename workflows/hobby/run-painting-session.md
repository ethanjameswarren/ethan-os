# Workflow: run-painting-session

## Purpose

Coach the user through one painting phase at a time, evaluate photos, and update the painting plan/log and skill profile.

## Trigger

- "I'm ready to prime the Scarabs."
- "What phase should I do next on the Warriors?"
- "I just finished the drybrush step — how does it look?"
- Upload a photograph of a model in progress.

## Inputs

- Collection item / plan title or ID.
- User description and/or uploaded photo.

## Outputs

- One manageable phase instruction or correction plan.
- Updated `hobby.painting-plan`, `hobby.painting-log`, and `hobby.technique-skill` records.
- Optional `hobby.session` record for the session.

## Steps

1. Load the current `hobby.painting-plan`. If none exists, offer `create-painting-plan` first.
2. Determine the current phase (next pending, or the one the user just completed).
3. If the user provided a photo, run `ethan-os/skills/hobby/evaluate-miniature-photo.md` first.
4. Run `ethan-os/skills/hobby/coach-painting-phase.md`.
5. Give one phase's instructions with specific paints, brushes, techniques, inspection points, and what NOT to touch.
6. After the phase, ask for a photo or description so the next step can be evaluation.
7. Update the painting log and plan status.
8. If the phase introduced or reinforced a technique, run `ethan-os/skills/hobby/update-painting-skills.md`.
9. Confirm whether to continue, stop, or fix something first.
