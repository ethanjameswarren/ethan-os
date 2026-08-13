# Capture Object Prompt

## Purpose

Generate a Capture object from raw user input.

## Required fields

- `id`: stable ID
- `schema`: `knowledge.capture`
- `schema_version`: `1`
- `title` or first few words
- `created_at`
- `provenance`

## Body

Preserve the original raw input as closely as possible. Minor cleanup (spelling, punctuation) is allowed if it does not change meaning.

## Instructions

- Captures are low-friction. Do not require structured input.
- Do not extract ideas here. Extraction happens in a later step.
- Save to `ethan-life/domains/knowledge/captures/`.
