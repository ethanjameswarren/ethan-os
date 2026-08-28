# Skill: diagnose-schedule

## Purpose

Help the user understand why a schedule feels broken or why a desired activity does not fit.

## Input

- User's complaint or question (e.g., "I never have time to read.")
- Active baseline schedule.
- Recent weekly plans if available.
- Active goals and tasks.
- Existing overrides.

## Steps

1. Identify the user's real concern: missing time, overpacked evenings, not enough sleep, too much context switching, etc.
2. Calculate total fixed time, flexible time, optional time, and unallocated time for the relevant period.
3. Inspect for common causes:
   - fixed commitments dominate the target window;
   - flexible items scheduled in fragmented chunks;
   - competing priorities in the same block;
   - dependency cascades (e.g., late evening pushes bedtime past `latest_bed`);
   - recurring chores or meetings that could batch better;
   - goals/tasks that are larger than the available discretionary windows;
   - recent overrides that were never reverted and now pile up.
4. Propose targeted changes, not blanket overhauls. Examples:
   - move reading to a 30-minute protected morning block;
   - batch errands into one evening;
   - temporarily drop optional blocks to create margin;
   - split a large project task into smaller chunks.
5. If the user asks for a full rebuild, run `skills/planning/generate-weekly-plan.md` with the current preferences.

## Output

- A short diagnosis in plain language.
- One to three targeted recommendations.
- Optional tradeoffs (e.g., "This gives you 30 minutes more reading time but means moving gym to Saturday.").
- Clear next step: accept a recommendation, request a full rebuild, or adjust manually.

## Rules

- Do not respond by simply adding another time block.
- Do not recommend permanent baseline changes unless the user confirms.
- Surface dependency implications.
- Distinguish symptoms ("evenings packed") from causes ("errands scattered across three nights").
