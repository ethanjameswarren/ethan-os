# Skill: coach-painting-phase

## Purpose

Deliver one manageable painting phase at a time, give a clear go/no-go inspection, and tell the user exactly what to fix before continuing.

## Input

- Current `hobby.painting-plan` record.
- Current `hobby.painting-log` record, if any.
- User description and/or uploaded photograph of the current state.
- All `hobby.paint-supply` and `hobby.technique-skill` records.

## Output

- Next phase instructions, or correction instructions for the current phase.
- Updated plan/log status.

## Instructions

1. Identify the current active phase in the plan. If no phase is in progress, start the first `pending` phase.
2. Give concise, step-by-step instructions for that phase only. Include:
   - paints/tools to use,
   - brush-loading and thinning reminders,
   - technique focus,
   - what the result should look like.
3. After the user finishes (or uploads a photo), evaluate against the phase's `inspect_for` list. Distinguish:
   - **Must fix** — problems that will be hard to correct later or that break the army-wide scheme.
   - **Worthwhile improvement** — noticeable at tabletop distance but not required to proceed.
   - **Optional advanced refinement** — fine-detail work that can be skipped for now.
4. Avoid perfectionism. A tabletop-ready model is the default goal unless the user explicitly asks for display quality.
5. If a must-fix issue exists, give exact correction instructions and tell the user what NOT to touch while fixing it.
6. If the phase passes, mark it `done` and advance to the next phase. Ask whether the user wants to continue or stop.
7. When a photo is provided, describe what looks correct and what looks off. If you cannot see detail clearly, ask for a different angle or closer shot rather than guessing.
8. Update the `hobby.painting-log` with the phase completion, mistakes, corrections, and any techniques practiced.
