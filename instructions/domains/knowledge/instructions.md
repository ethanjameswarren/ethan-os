# Knowledge Domain Instructions

## Scope

Capture, understand, connect, summarize, review, and revise learning material.

## Source handling

- Create a Source object for books, articles, papers, podcasts, videos, courses, conversations, and experiences.
- Link captures and ideas to their sources.
- Do not duplicate source metadata across objects.

## Capture handling

- Preserve raw captures in `ethan-life/domains/knowledge/captures/`.
- Captures are immutable records of what Ethan said.

## Idea extraction

- Extract atomic ideas that remain useful independently of the source.
- Record:
  - claim (source's claim)
  - interpretation (Ethan's reading)
  - position (agree / disagree / neutral / exploring)
  - confidence (low / medium / high)
- Do not convert source claims into Ethan's beliefs.

## Relationships

- Use inline typed links.
- Only create relationships with contextual justification.

## Summaries

- One canonical summary per source.
- Include 30 Seconds, 5 Minutes, and Detailed Personal Summary sections.
- Detailed section must include source claims, Ethan's interpretation, agreement/disagreement, uncertainty, connections, and applications.

## Lifecycle

Optional lifecycle states: `captured`, `understood`, `connected`, `testing`, `practicing`, `internalized`.
- Apply primarily to Ideas.
- Objects may move backward when understanding changes.
