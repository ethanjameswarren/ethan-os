# Skill: recommend-practice-model

## Purpose

Suggest the next model to paint based on the intended practice order, current skill level, and which techniques need practice.

## Input

- Collection items and their statuses.
- `hobby.painting-plan` and `hobby.painting-log` records.
- `hobby.technique-skill` records.

## Output

- A ranked recommendation of the next 1–3 models to paint and why.

## Instructions

1. Prefer unpainted models earlier in the practice order.
2. Favor models that allow the user to practice techniques currently at `new` or `practicing` status.
3. Defer characters, centerpiece models, and complex models until foundational techniques (`spray priming`, `base coating`, `cleanup`, `shade/wash control`) are at least `comfortable`.
4. For each recommendation, explain which technique(s) it practices and what risk it avoids.
5. If the user wants to paint a model earlier than recommended, flag which skills to be careful with and suggest a quick practice step first.
6. Do not recommend buying a new model just to practice; use owned or planned collection items.
