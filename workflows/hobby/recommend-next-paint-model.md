# Workflow: recommend-next-paint-model

## Purpose

Suggest the next model to paint based on practice order, current skills, and techniques that need practice.

## Trigger

- "What should I paint next?"
- "Which model is best to practice drybrushing on?"
- "I want to start the Overlord but is it too soon?"

## Inputs

- Optional preferred model or skill focus.

## Outputs

- 1–3 model recommendations with rationale.

## Steps

1. Run `ethan-os/skills/hobby/recommend-practice-model.md`.
2. Prefer unpainted models earlier in the practice order.
3. Match the recommendation to techniques currently at `new` or `practicing`.
4. Defer characters and centerpiece models until foundational skills are `comfortable`.
5. If the user insists on a model earlier than recommended, explain what to be careful about and which quick practice step to do first.
6. Confirm the recommendation.
