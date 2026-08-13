# Skill: resolve-ideas

## Purpose

Match extracted ideas to existing ideas to prevent duplicates.

## Input

- candidate ideas
- existing ideas in `ethan-life/domains/knowledge/ideas/`

## Output

- for each candidate:
  - action: create | update | link-existing
  - matched_id (if link-existing or update)
  - reason

## Instructions

- Link if the claim is substantively the same.
- Create new if the claim differs in meaning, scope, or implication.
- Update if the new capture adds nuance to an existing idea.
- Avoid duplicate objects.
