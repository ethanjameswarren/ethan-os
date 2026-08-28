# Workflow: guided-learning

## Purpose

Support structured learning across formats — university courses, online courses, certifications, professional training — using the same Knowledge and retention systems as Guided Reading.

## Triggers

| intent | examples | skill |
|--------|----------|-------|
| start learning | "I'm starting Statistics 301" | `skills/knowledge/start-learning-program.md` |
| continue learning | "Finished lecture 5" | `skills/knowledge/capture-learning-session.md` |
| review learning | "Quiz me on this week" | `skills/knowledge/review-learning-program.md` |
| finish learning | "I finished the course" | `skills/knowledge/finish-learning-program.md` |
| assess course fit | "Should I take this LinkedIn Learning course?" | `skills/knowledge/assess-course-fit.md` |

## Steps

1. Classify the intent: `start-learning`, `continue-learning`, `review-learning`, `finish-learning`.
2. Load the active `knowledge.learning-program` from `ethan-life/domains/knowledge/learning-programs/`.
3. Load the relevant `knowledge.source` if `source_id` is set.
4. Dispatch to the appropriate skill.
5. The skill may create or update `knowledge.learning-program`, `knowledge.learning-session`, `knowledge.idea`, `knowledge.summary`, or retention state.
6. Return a concise, conversational response.

## Outputs

- `knowledge.learning-program` objects
- `knowledge.learning-session` objects
- `knowledge.idea` objects from promoted insights
- `knowledge.summary` from completion
- Updated `retention-state.yaml`

## Confirmation policy

- Starting a program: auto-execute.
- Capturing a session: auto-execute; retention is selective, not automatic.
- Finishing a program: present the final synthesis and ask for confirmation before creating a summary.
- Review: auto-execute; only update retention state, not the program itself.

## Safeguards

- Do not store full copyrighted material; persist only locators, short excerpts, and derived notes.
- Do not auto-advance every active project.
- Do not schedule every insight for retention.
- Preserve source grounding and provenance.
