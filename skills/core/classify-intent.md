# Skill: classify-intent

## Purpose

Classify user input into one of the v0.1 intents.

## Input

- parsed user input
- available intents list

## Output

- intent: capture | process-learning-notes | ask | summarize | review | revise | status
- confidence: high | medium | low
- domain hint (if applicable)
- ambiguity note if intent is unclear

## Intents

- capture: raw thought or note
- process-learning-notes: learning input to be structured
- ask: question against stored knowledge
- summarize: generate/refresh a summary
- review: surface items worth revisiting
- revise: update an existing object
- status: show operational state

## Instructions

- If confidence is low, ask for clarification rather than guess.
- Learning-related inputs default to `process-learning-notes`.
- Questions starting with "what", "how", "why", "do I", "have I" default to `ask`.
