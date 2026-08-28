# Workflow: Capture a Learning Note

## What you do

Describe something you read, watched, heard, or thought about in your own words.

Example:

> **You:** "I listened to a podcast about decision fatigue. The main idea is that small repeated decisions drain willpower for bigger ones."

## What Ethan OS does

1. Stores the raw capture.
2. Asks what stood out or how it connects to what you already know.
3. Extracts reusable ideas, separating source claims from your interpretation.
4. Links the capture and ideas to related sources, ideas, or projects.
5. Offers to schedule a lightweight review if the idea seems worth keeping.

## Conceptual stages

- **Capture** — your original note.
- **Clarify** — the OS asks follow-up questions.
- **Extract** — durable ideas are created from the capture.
- **Connect** — links are added to existing ideas.
- **Review** — important ideas resurface later as conversational prompts.

## Outputs

- A Capture object.
- One or more Idea objects.
- Typed relationships between sources, captures, and ideas.
- An optional Review item.

## Safeguards

- The OS never fabricates source content.
- It distinguishes source claims, your interpretation, and AI-generated explanation.
- It does not store full copyrighted text.

## Technical details

- Workflow: `workflows/knowledge/capture-learning-note.md`
- Skills: `skills/knowledge/extract-ideas.md`, `skills/knowledge/connect-ideas.md`, `skills/knowledge/schedule-review.md`
- Schemas: `schemas/domains/knowledge/capture.schema.yaml`, `idea.schema.yaml`
