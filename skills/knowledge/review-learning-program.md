# Skill: review-learning-program

## Purpose

Surface due retention items and weak concepts for a learning program, and build targeted review for assessments.

## Triggers

- "Quiz me on this week's material."
- "What have I learned so far?"
- "What am I weak on?"
- "I have a midterm next week."
- "My AWS exam is in two weeks."

## Input

- Active `knowledge.learning-program`.
- `knowledge.learning-session` history.
- `retention-state.yaml`.

## Steps

1. Load the program and its sessions.
2. If an assessment is approaching:
   - Filter `assessments` with a `due_date` within the relevant window.
   - Collect weak concepts from `mistakes`.
   - Collect `extracted_insights` from sessions relevant to the assessment scope.
   - Build a targeted, user-grounded review rather than a generic study guide.
3. If no assessment is approaching:
   - Surface 1-3 due retention items.
   - Ask retrieval questions conversationally.
   - Classify recall as `strong`, `partial`, `failed`, or `skipped`.
   - Update the retention schedule.
4. For weak concepts, ask application or scenario questions:
   - "If you saw X, what would you do first?"
   - "How is this different from Y?"
5. Do not produce multiple-choice quizzes. Use conversational retrieval.

## Output

- Targeted review questions.
- Updated retention schedule if items were reviewed.
- A short note on weak concepts and confidence.
