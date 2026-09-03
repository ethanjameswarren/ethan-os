# Workflow: review-and-promote-lore

## Purpose

Review pending lore candidates and promote approved ones into canon.

## Trigger

- "Review my lore candidates."
- "Promote the Lokhust destroyer kill tally to canon."
- "Reject the idea that the dynasty hates humans."

## Inputs

- `hobby.lore-candidate` records with status `proposed` or `under_review`.

## Outputs

- Updated candidate statuses.
- New or updated `hobby.lore-canon` entries for approved candidates.

## Steps

1. Run `ethan-os/skills/hobby/review-lore-candidates.md` to present each candidate.
2. Collect Ethan's decision for each: approve, modify, reject, defer, supersede.
3. For approved or modified candidates, run `ethan-os/skills/hobby/promote-lore-to-canon.md`.
4. For rejected candidates, record a rejection reason.
5. Confirm what was promoted and what remains pending.
