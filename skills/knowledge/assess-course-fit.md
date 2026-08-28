# Skill: assess-course-fit

## Purpose

Decide whether a course or program is worth taking based on the user's goals, prior learning, career targets, projects, and schedule.

## Triggers

- "Should I take this LinkedIn Learning course?"
- "Is this course worth taking for me?"
- "Would this certification help me?"
- "assess-course-fit"

## Input

- Natural-language course description or title from the user.
- A `core.context-bundle` for intent `course-decision` across `planning`, `knowledge`, and `career`.

## Steps

1. Parse the course title and topics.
2. Assemble context with `scripts/core/context_assembly.py`:
   - active `planning.goal`
   - active `career.job-target`
   - current `knowledge.learning-program`
   - related `knowledge.idea` and `knowledge.source`
   - active `planning.project`
   - `planning.baseline-schedule` constraints
3. Identify overlaps:
   - Does the user already know this material? (from completed courses, books, or ideas)
   - Is the course redundant with an active program?
4. Identify gaps:
   - Does the course fill a real capability gap for a goal or job target?
   - Does it support an active project?
5. Identify opportunity cost:
   - Does the user have time in the schedule?
   - Does it displace a higher-priority course or project?
6. Produce a recommendation:
   - **Take it** — clear gap, aligned with goal, schedule allows.
   - **Defer it** — useful but lower priority or schedule is full.
   - **Skip it** — already covered, not aligned, or better alternative exists.
7. Provide reasons traceable to the context bundle.

## Output

- Recommendation with reasons.
- Relevant supporting context (goals, projects, job target, current learning).
- Conflicts or opportunity costs if any.

## Rules

- Do not invent career goals or schedule availability.
- Do not recommend a course that is redundant with an active program unless it adds distinct depth.
- Preserve provenance: every claim must trace to a retrieved object.
