# Intent Router

## Purpose

Classify user input into an intent and select the corresponding workflow.

## v0.1 intents

| intent | trigger examples | workflow |
|--------|------------------|----------|
| capture | "I had a thought...", "Save this..." | `workflows/core/capture-and-route.md` |
| process learning notes | "Finished chapter 4...", "Here are my notes on..." | `workflows/knowledge/process-learning-notes.md` |
| ask / retrieve | "What do I know about...?", "What have I learned about...?" | `workflows/core/ask.md` |
| summarize | "Summarize Atomic Habits" | `workflows/knowledge/process-learning-notes.md` (or `workflows/core/ask.md`) |
| review | "What should I review?" | `workflows/core/review.md` |
| revise | "I changed my mind about..." | `workflows/core/revise.md` |
| status | "Status", "What is pending?" | `workflows/core/status.md` |
| start listening session | "Start SK11X025", "Listen to KW34", "Lookup Holden Federico - Dust" | `workflows/music/lookup-release-and-listen.md` |
| capture listening note | "A1 energy 3, rating 4", "B2 favorite", "next", "done" | `workflows/music/capture-listening-note.md` |

## Routing rules

- If intent is ambiguous, ask for clarification.
- For substantive Life OS requests, follow the cross-repository execution order:
  `ethan-os` → `ethan-life` → `ethan-notion` → live Notion.
  Do not route directly to Notion unless the user explicitly asks for a pure Notion infrastructure or presentation change (e.g., add a database property, fix a relation, update a database ID, change a mapping).
- If input matches multiple domains but only Knowledge is enabled, route to Knowledge.
- Future domains (food, health, etc.) require enablement in `ethan-life/.ethan-os.yaml`.
