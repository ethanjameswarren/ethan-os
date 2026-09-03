# Skill: update-painting-skills

## Purpose

Update `hobby.technique-skill` statuses after a model or phase is completed, reflecting real practice.

## Input

- Completed `hobby.painting-log` or `hobby.session`.
- User self-assessment, if provided.
- Existing `hobby.technique-skill` records.

## Output

- Updated technique-skill files.
- Summary of progression.

## Instructions

1. For each technique practiced in the session, review the result and the user's self-assessment.
2. Advance the status only when evidence supports it:
   - `new` → `practicing` after a first successful attempt or two.
   - `practicing` → `comfortable` after consistent, repeatable results on normal models.
   - `comfortable` → `proficient` after clean results under varying conditions, including corrections and edge cases.
3. Do not skip statuses. A single good result does not make someone proficient.
4. Record `practiced_on_model_ids` with the relevant collection item or painting-log IDs.
5. Update `first_practiced_date` if it was previously blank.
6. Add notes about what went well and what still needs work.
7. If a technique was attempted but failed or produced poor results, keep it `practicing` and note the specific issue to address next time.
