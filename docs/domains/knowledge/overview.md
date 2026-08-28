# Knowledge & Learning Domain

The first fully implemented domain in Ethan OS.

## Purpose

Capture, understand, connect, summarize, review, and revise what Ethan learns from books, articles, podcasts, videos, courses, conversations, and experience.

## v0.1 objects

- Source
- Capture
- Idea
- Summary
- Review
- Reading Session (`knowledge.reading-session`)

## Guided Reading

The `Guided Reading` workflow lets Ethan read and talk while the OS manages notes, progress, and cross-source connections. See `docs/domains/knowledge/guided-reading.md`.

## Guided Reading extensions

- **Pre-reading assessment**: per-source `knowledge.reading-profile` for familiarity, goals, and spoiler policy.
- **Source enrichment / access**: `source_access`, `page_alignment`, and `content_locator` so discussions can be grounded when text is available.
- **Retention**: active recall, elaboration, compression, and spaced-review scheduling via `retention-state.yaml`.
- **Book library + recommendations**: full reading universe tracking through `knowledge.source` library fields, plus explainable recommendations.

## Design principles

- Preserve raw captures.
- Distinguish source claims from Ethan's interpretation and position.
- Extract atomic ideas.
- Create meaningful typed relationships.
- Produce personal summaries, not generic SparkNotes.
- Preserve evolution via optional `## Evolution` sections.
