# Workflow: update-technique-skill

## Purpose

Explicitly mark a painting or modeling technique as practiced, comfortable, or proficient.

## Trigger

- "I think I'm comfortable with drybrushing now."
- "Mark edge highlighting as practicing after the Warriors."
- "Magnetization went well on the Destroyers."

## Inputs

- Technique name and the model(s) practiced on.
- Optional user self-assessment.

## Outputs

- Updated `hobby.technique-skill` file.
- Summary of progression.

## Steps

1. Run `ethan-os/skills/hobby/update-painting-skills.md`.
2. Confirm the new status is supported by the models listed.
3. Update the technique-skill record, `practiced_on_model_ids`, and `first_practiced_date` if needed.
4. Flag any plans that now become easier or any advanced techniques that are now appropriate to introduce.
5. Confirm the new status.
