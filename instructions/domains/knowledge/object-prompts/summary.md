# Summary Object Prompt

## Purpose

Generate or refresh the canonical summary for a source or topic.

## Required fields

- `id`: stable ID
- `schema`: `knowledge.summary`
- `schema_version`: `1`
- `title`
- `source_id` or `topic`
- `created_at`
- `provenance`

## Body sections

1. `## 30 Seconds` — only the most important takeaway.
2. `## 5 Minutes` — major concepts, Ethan's interpretation, disagreements, applications.
3. `## Detailed Personal Summary` — source arguments, interpretation, examples, disagreements, open questions, connections, applications, changes in Ethan's thinking.

## Instructions

- The summary must be Ethan's personal synthesis, not a generic book summary.
- Preserve source/user separation.
- Surface uncertainty and disagreement honestly.
- Update the canonical file rather than creating a new one; Git tracks history.
