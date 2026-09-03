# Skill: review-lore-candidates

## Purpose

Help Ethan review pending `hobby.lore-candidate` objects and decide whether to approve, reject, modify, defer, or merge them.

## Input

- All `hobby.lore-candidate` records with `status: proposed` or `status: under_review`.
- Related `hobby.lore-canon` entries to check consistency.

## Output

- Updated candidate statuses and review notes.
- Optional routing to `promote-lore-to-canon` for approved candidates.

## Instructions

1. Present each candidate with its source event, candidate type, and current wording.
2. Check for contradictions with `locked` or `developing` canon. Flag any conflict.
3. Ask for a decision on each: approve, reject, modify, defer, supersede.
4. For modifications, rewrite the candidate content and set status to `under_review`.
5. For approved candidates, collect the target `lore_type` and proposed canon entry or new entry.
6. For rejected candidates, record a `rejection_reason` and leave the candidate intact.
7. Do not auto-promote; route to `promote-lore-to-canon`.
