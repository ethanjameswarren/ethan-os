# Workflow: capture-and-route

## Purpose

Capture raw user input and route it to the appropriate domain workflow.

## Steps

1. Parse raw input.
2. Classify intent.
3. If intent is `process-learning-notes`, run `workflows/knowledge/process-learning-notes.md`.
4. If intent is `capture` only, create a Capture object in `ethan-life/domains/knowledge/captures/`.
5. If intent is ambiguous, ask for clarification.

## Output

- Capture object ID
- Routed workflow result (if applicable)
- Concise summary

## Confirmation policy

- Low-risk capture: auto-execute.
- Ambiguous routing: ask for clarification.
