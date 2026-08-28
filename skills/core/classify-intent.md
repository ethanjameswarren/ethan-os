# Skill: classify-intent

## Purpose

Classify user input into one of the v0.1 intents.

## Input

- parsed user input
- available intents list

## Output

- intent: capture | process-learning-notes | ask | summarize | review | revise | status | schedule-change | plan-week | plan-day | diagnose-schedule
- confidence: high | medium | low
- domain hint (if applicable)
- ambiguity note if intent is unclear

## Intents

- capture: raw thought or note
- process-learning-notes: learning input to be structured
- start-learning: begin a new course or program
- continue-learning: progress a session in an active learning program
- review-learning: quiz or review a learning program
- finish-learning: finish a course or program
- assess-course-fit: decide whether a course or program is worth taking
- ask: question against stored knowledge
- summarize: generate/refresh a summary
- review: surface items worth revisiting
- revise: update an existing object
- status: show operational state
- schedule-change: add, move, or modify a schedule item
- plan-week: generate a concrete weekly plan
- plan-day: generate a single-day plan
- sunday-review: build next week's plan during Sunday weekly review
- diagnose-schedule: identify why a schedule feels broken or where time could fit

## Instructions

- If confidence is low, ask for clarification rather than guess.
- Learning-related inputs default to `process-learning-notes`, unless the user is clearly starting, continuing, reviewing, or finishing a course or program.
- Questions starting with "what", "how", "why", "do I", "have I" default to `ask`.
