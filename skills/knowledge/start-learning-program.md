# Skill: start-learning-program

## Purpose

Begin a new learning program and create its canonical `knowledge.learning-program` object.

## Triggers

- "I'm starting Statistics 301."
- "I'm taking a LinkedIn Learning course on AI agents."
- "Add my Coursera course."
- "I'm studying for AWS Solutions Architect."

## Input

- User's natural language description.
- Any known program metadata (provider, start date, target, course type).

## Steps

1. Resolve the program title. If a `knowledge.learning-program` with the same title and provider already exists, treat this as a new learning cycle.
2. Infer or ask for `course_type`:
   - `university_course`, `online_course`, `certification`, `workplace_training`, `self_study`, `other`.
3. Run `skills/knowledge/pre-learning-assessment.md` if no prior profile-like data was given.
4. Create the `knowledge.learning-program` in `ethan-life/domains/knowledge/learning-programs/` with:
   - `schema: knowledge.learning-program`, `schema_version: 1`
   - `status: learning`
   - `started_at: today`
   - `course_type`, `provider`, `instructor` if known
   - `subject` if inferable
   - `learning_goals`, `prior_familiarity`, `target_outcome`, `desired_depth`
   - `known_weak_areas` if stated
   - `target_completion_date` if stated
   - `modules` if the user supplied a syllabus or module list; otherwise leave empty
   - `current_module_id` null, `completed_module_ids` empty
5. If the user provided a syllabus, outline, or exam objectives, populate `modules` and `assessments` lightly.
6. If a `knowledge.source` for the course material already exists or the user provides a URL, link it via `source_id`.
7. Return a concise confirmation and the first step they might take.

## Output

- Created or updated `knowledge.learning-program` ID.
- Any missing information asked as a short follow-up.
