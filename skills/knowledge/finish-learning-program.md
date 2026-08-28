# Skill: finish-learning-program

## Purpose

Close a learning program with a user-grounded synthesis and durable takeaways.

## Triggers

- "I finished the LinkedIn Learning course."
- "I'm done with Statistics 301."
- "I passed the certification exam."

## Input

- `knowledge.learning-program`.
- All associated `knowledge.learning-session`.
- `retention-state.yaml`.

## Steps

1. Mark the program `status: finished`.
2. Ask a brief final reflection appropriate to `desired_depth`:
   - Light: "What are the 1-3 most useful ideas?"
   - Normal/Deep: Add "What can you now do that you couldn't before?" and "What should you apply somewhere?" and "What do you still not feel confident about?"
3. Generate a synthesis from the user's actual sessions, insights, and mistakes:
   - Major concepts learned.
   - Strongest retained knowledge.
   - Weak concepts.
   - Important assignments/projects if applicable.
   - Connections to other knowledge.
   - Ideas worth retaining long-term.
4. Promote strong insights to `knowledge.idea` if not already promoted.
5. Create a `knowledge.summary` linked to the program if the user wants a permanent synthesis.

## Output

- Updated `knowledge.learning-program`.
- User-grounded final synthesis.
- Optional `knowledge.summary`.
