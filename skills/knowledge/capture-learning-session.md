# Skill: capture-learning-session

## Purpose

Capture a learning session, update program progress, surface weak concepts, and schedule selective retention.

## Triggers

- "Finished lecture 5."
- "Finished module 3."
- "Watched the section on MCP."
- "Did the lab."
- "Finished the course exercise."
- "Got this wrong."
- "I'm stuck on exercise 4."

## Input

- The user's message.
- Active `knowledge.learning-program`.
- Optional `knowledge.source` for grounding.

## Steps

1. Resolve the program. If none is active, prompt the user to start one first.
2. Determine `session_type` from the message or ask.
3. Update the program's `current_module_id` and `completed_module_ids` if a module was finished.
4. Run active recall first unless the user already described what they remember.
5. Ask a few adaptive questions based on `course_type` and `desired_depth`:
   - University: What did the professor emphasize? What was unclear? What connects to previous lectures?
   - Online: What was the main concept? Could you explain it without the video? What would you actually use this for?
   - Certification: Can you distinguish this from similar concepts? Could you apply it to a scenario? What did you get wrong?
6. For mistakes or "stuck on exercise":
   - Identify the underlying concept.
   - Ask what they tried.
   - Help them reason through it without giving the answer when understanding is the goal.
   - Record the misconception in `mistakes` with `concept`, `correction`, and `recurring`.
7. Capture durable takeaways in `extracted_insights` only if they are reusable, meaningful, or connect to other knowledge. Do not capture everything.
8. Record `connections` to other `knowledge.idea`, `knowledge.source`, `planning.project`, or `planning.task` when the user mentions a link.
9. If the user explicitly wants to retain an insight, schedule it in the retention system. Do not auto-retain everything.
10. Create a `knowledge.learning-session` in `ethan-life/domains/knowledge/learning-sessions/`.

## Output

- Created `knowledge.learning-session` ID.
- Updated `knowledge.learning-program`.
- Concise summary and any next step or follow-up question.
