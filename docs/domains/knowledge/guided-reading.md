# Guided Reading — Technical Reference

> **For a human overview, see [`docs/capabilities/guided-reading.md`](../../capabilities/guided-reading.md).**
>
> **For the end-to-end workflow from a user's perspective, see [`docs/workflows/guided-reading.md`](../../workflows/guided-reading.md).**
>
> This document is the technical implementation reference. It describes data models, state formats, intents, schemas, and runtime behavior for the AI/runtime.

## Purpose

Read and talk. Ethan OS tracks the book, progress, sessions, ideas, and connections for you.

## Core design

- A **book** is a `knowledge.source` with `source_type: book`.
- A **reading profile** is a `knowledge.reading-profile` object that captures the user's prior familiarity, goals, and spoiler policy for that source.
- **Current progress** is authoritative in `ethan-life/domains/knowledge/reading-state.yaml`.
- A **reading session** is a `knowledge.reading-session` object that records what happened during one interaction.
- Durable, reusable insights may be promoted to `knowledge.idea` objects.
- Final synthesis becomes a `knowledge.summary`.

## Data model

### `knowledge.source` (book metadata)

- `title`, `author`, `source_type: book`
- `edition`, `isbn`, `publication_year`, `total_pages`
- `reading_mode`: nonfiction | fiction | music_history_culture | other
- `status`: unread | reading | paused | finished | abandoned | reference  (reading lifecycle)
- `ownership_status`: owned_physical | owned_digital | borrowed | wishlist | not_owned | unknown
- `format`: hardcover | paperback | ebook | audiobook | pdf | epub | other
- `acquired_at`, `acquisition_source`
- `started_at`, `finished_at`, `rating`
- `tags`, `user_interest_notes`

Note: `current_page` and `spoiler_boundary` are **not** stored here. They live in `reading-state.yaml`.

Ownership/access and reading lifecycle are kept separate. A book can be `owned_physical` and `unread`, or `wishlist` and `unread`, or `not_owned` and discovered.

### `reading-state.yaml`

```yaml
version: 1
active_books:
  - source_id: src-20260827-001
    status: active
    current_page: 32
    last_completed_range:
      start: 16
      end: 32
    spoiler_boundary: 32
    last_reading_at: 2026-08-27
    last_session_id: rs-20260827-002
reading_queue:
  - source_id: src-20260827-005
    queue_position: 1
    status: next_up
    reason: Strong fit after current systems reading.
  - source_id: src-20260827-006
    queue_position: 2
    status: queued
    reason: Owned unread; logistics follow-up.
```

Supports multiple simultaneously active books and a lightweight reading queue.

### `knowledge.reading-profile`

- `source_id`
- `familiarity_level`: unfamiliar | some_exposure | familiar | very_familiar
- `exposure_notes`: prior exposure (films, earlier reads, professional use, etc.)
- `read_context`: first_read | reread | partial_read | reference_read | other
- `discussion_goals`: topics/lenses the user wants to focus on
- `spoiler_policy`: strict_current_page | known_material_ok | full_spoilers_ok
- `prior_questions`: questions or opinions the user already holds
- `discussion_depth`: light | normal | deep
- `source_access`: metadata_only | model_knowledge | full_text_available
- `content_locator`: path/URL/identifier for accessible digital source (no secrets)
- `content_format`: pdf | epub | txt | markdown | other
- `ingestion_status`: not_started | pending | complete | failed
- `page_alignment`: exact | approximate | unknown
- `last_indexed_at`: date content was last inspected
- `source_provenance`: origin, access restrictions, alignment notes

The profile is owned by the source, not by state or individual sessions.

### `knowledge.reading-session`

- `source_id`, `session_date`, `pages.start/end`
- `spoiler_boundary_at`: the highest page completed when this session happened
- `reading_mode`
- `user_observations`: user's exact words
- `discussion_summary`: AI synthesis, clearly labeled
- `questions_asked`, `extracted_insights`, `predictions`, `open_questions`, `applications`, `connections`, `notable_passages`

## Source access and enrichment

When starting a book, the system determines what material is available:

| access level | behavior |
|--------------|----------|
| `metadata_only` | Rely on user observations; ask open questions; do not fabricate content. |
| `model_knowledge` | Use reliable general knowledge; treat page numbers as edition-dependent; be conservative. |
| `full_text_available` | Retrieve actual sections for the reported range; ground questions in real content. |

Rules:

- Never claim to have inspected the user's exact page range unless the corresponding source text was actually retrieved.
- If full text is available, retrieve only the reported range and never later material for fiction with `strict_current_page`.
- Record `page_alignment` as `exact`, `approximate`, or `unknown` based on edition confidence.
- Do not persist full copyrighted book text in `ethan-life`. Persist only locators, references, short excerpts, and derived notes.
- If no digital source is available, reading still works.

## Reading modes

| mode | suitable for | reflection path |
|------|--------------|---------------|
| nonfiction | explanatory, business, science, philosophy, systems | what stood out, what surprised, agree/disagree, connections, implications, action |
| fiction | novels, stories | reaction, characters, worldbuilding, themes, predictions, unresolved questions |
| music_history_culture | scene histories, music biographies, cultural studies | people, clubs, scenes, context, styles, technology, personal connections |
| other | everything else | adaptive open questions |

Modes are classified automatically and can be overridden by the user.

## Spoiler protection (fiction)

- `spoiler_boundary` = the highest page the user has explicitly completed.
- It advances only on explicit progress reports.
- The OS does not reveal later plot, characters, terminology, or thematic conclusions from beyond the boundary, including from model knowledge.
- If source text is retrieved, the retrieval itself must respect the boundary: only current-page-earlier material is fetched, plus harmless local context needed to interpret the current passage. Later chapters/pages are not retrieved and then suppressed.

## Intents

| intent | examples | workflow |
|--------|----------|----------|
| start reading | "I'm starting Dune" | `workflows/knowledge/start-reading.md` |
| continue reading | "Did 16-32" | `workflows/knowledge/continue-reading.md` |
| discuss reading | "The Bene Gesserit seem sketchy" | `workflows/knowledge/discuss-reading.md` |
| finish reading | "I finished Thinking in Systems" | `workflows/knowledge/finish-reading.md` |
| reading status | "Where am I in Dune?" | `workflows/knowledge/reading-status.md` |
| review reading | "What ideas are due for review?" | `workflows/knowledge/review-reading.md` |
| update reading profile | "I want to focus more on the ecology" | `workflows/knowledge/update-reading-profile.md` |
| manage book library | "I bought The Box." | `workflows/knowledge/manage-book-library.md` |
| bootstrap library | "Here are the books I own..." | `workflows/knowledge/manage-book-library.md` |
| book recommendation | "What should I read next?" | `workflows/knowledge/book-recommendation.md` |
| build reading queue | "Build me my next 5-book queue." | `workflows/knowledge/build-reading-queue.md` |
| reading stats | "Show my reading stats." | `workflows/knowledge/reading-status.md` |
| cross-reading retrieval | "What have I learned about incentives?" | `workflows/knowledge/reading-status.md` |

## Pre-reading assessment

When a `knowledge.reading-profile` does not yet exist for a source, run a short pre-reading assessment:

- Ask at most 1-3 prompts; often just one.
- Infer `familiarity_level`, `read_context`, `discussion_goals`, `spoiler_policy`, and `discussion_depth` from the response.
- Skip the assessment if the user already provided enough context in their start message.
- Never infer `full_spoilers_ok` from familiarity alone.
- Persist the result as a `knowledge.reading-profile` linked to the source.

## Conversation design

- Ask 2-4 questions initially, adaptive to mode, context, and the reading profile.
- Use the profile to avoid beginner questions for very familiar readers.
- Follow interesting answers rather than completing a rigid checklist.
- Preserve the user's wording/meaning.
- Do not make the user approve every extracted note.
- Reading should not feel like homework.

## Retention loop

Guided Reading optimizes for durable understanding, not note volume. The normal flow is:

```
READ → ACTIVE RECALL → DISCUSS → CONNECT → COMPRESS → REVIEW LATER
```

### Active recall

When the user reports completing a segment, ask for retrieval first:

- "Without looking back, what are the 1-3 things you remember most?"
- Accept "honestly, not much" as valid.
- If the user already described what stood out, count that as recall and skip the prompt.

### Elaboration

Use 0-2 follow-ups that require the user to reconstruct meaning:

- "How would you explain that in your own words?"
- "Why do you think that matters?"
- "What would be a concrete example?"

### Compression

At the end of a session, identify 0-3 durable takeaways. A takeaway is worth keeping if it is:

- a concept, mental model, principle, or useful question,
- reusable months later,
- personally meaningful or actionable.

Keep richer detail inside the reading session; retention items are intentionally small.

### `retention-state.yaml`

Canonical spaced-review state:

```yaml
version: 1
retention_items:
  - item_id: ret-20260827-001
    source_type: session_insight  # or idea
    source_id: rs-20260827-001    # session id or idea id
    insight_id: tis-stock-flow-labor
    source_book_id: src-20260827-001
    title: System state vs. underlying flows
    first_learned_at: 2026-08-27
    last_reviewed_at: 2026-08-27
    next_review_due_at: 2026-08-28
    interval_index: 2
    successful_recalls: 2
    failed_recalls: 0
    current_confidence: high
    retention_priority: high
    last_recall_result: strong
    status: active
```

- `source_type: idea` references a `knowledge.idea` object directly.
- `source_type: session_insight` references a stable `insight_id` inside a `knowledge.reading-session`.

### Spaced-review schedule

Intervals (days): `[1, 3, 7, 14, 30, 60, 120]`

Outcome adjustments:

- `strong`: advance to the next interval.
- `partial`: stay at or step back one interval.
- `failed`: reset to the first interval and reconstruct the idea.
- `skipped`: keep the item active; do not advance.

Priority and status:

- `retention_priority`: low | normal | high. Low-priority items are not scheduled unless the user overrides.
- `status`: active | paused | archived. User opt-out sets `archived`.

### Review experience

Reviews test retrieval, not recognition:

- Bad: multiple-choice "What is a feedback loop?"
- Good: "A few days ago you connected feedback loops to labor planning. What was the connection?"

After the user's response, classify semantically: `strong`, `partial`, `failed`, or `skipped`. Do not score exact wording.

### Fiction reviews

Do not turn fiction into trivia. Review:

- character relationships, motivations, themes,
- major events already encountered,
- predictions the user made,
- changes in interpretation.

Respect `spoiler_policy` and `spoiler_boundary` in every review.

### Cross-book synthesis

When the user has encountered related concepts in multiple books, reviews and discussions may ask them to compare or connect ideas:

- "How does Meadows' idea of leverage points relate to Rumelt's idea of a guiding policy?"

Only connect ideas the user has actually encountered.

## v1 closeout operational pieces

### Library bootstrap / bulk import

`skills/knowledge/bootstrap-library.md` parses multiple books from a single user message and creates/updates `knowledge.source` objects. It infers `ownership_status` and `status` from context, avoids duplicates via `skills/knowledge/resolve-book-edition.md`, and reports only genuinely ambiguous items.

Examples:
- "Here are the books I own: Thinking in Systems, Dune, The Box."
- "These are books I've already read: Atomic Habits, The Psychology of Money."
- "Add these to my wishlist: Skunk Works, Fooled by Randomness."

### Duplicate / edition resolution

`skills/knowledge/resolve-book-edition.md` distinguishes a logical work from a manifestation/edition.

- Default to one source per logical work (title + author).
- Use ISBN as the strongest identifier when available.
- Merge different formats (paperback + Kindle) into one source unless the user wants separate tracking.
- Create a new source only for materially different editions (revised content, translation affecting page alignment, etc.).
- Preserve edition notes and page alignment when relevant.

### Reading queue

A lightweight `reading_queue` lives in `reading-state.yaml`:

```yaml
reading_queue:
  - source_id: src-...
    queue_position: 1
    status: next_up   # or queued | recommended | removed
    reason: ...
```

`skills/knowledge/build-reading-queue.md` and `workflows/knowledge/build-reading-queue.md` manage creation, reordering, and removal. `skills/knowledge/five-book-queue.md` generates a coherent five-book sequence considering variety, ownership, difficulty, length, and current interests.

### Due-review surfacing

`skills/knowledge/surface-due-reviews.md` selects 1-3 active retention items with `next_review_due_at <= today`, sorted by priority and confidence. It is used by `review-reading.md` and may briefly surface a single item during reading interactions, but it does not interrupt every session. No scheduler or notification infrastructure is required.

### Cross-reading retrieval

`skills/knowledge/cross-reading-retrieval.md` answers questions across the entire reading history using sources, sessions, ideas, summaries, reviews, retention state, and typed relationships. It preserves provenance and respects fiction spoiler boundaries.

Examples:
- "What have I learned about incentives?"
- "What did I think about Dune's politics?"
- "What themes keep coming up across books?"

### Lightweight reading stats

`skills/knowledge/reading-stats.md` produces useful summaries without gamification:

- currently reading, finished this month/year, abandoned/paused
- owned unread and wishlist counts
- fiction/nonfiction mix
- common themes/domains
- strongest retained ideas and weak concepts due for review
- average rating when meaningful

No streaks, badges, or volume targets.

### Recommendation simplicity

Recommendations in v1 use transparent reasoning over library, history, ratings, reviews, goals, retained ideas, abandoned books, and stated interests. There is no ML recommender. Any scoring is simple, explainable, and easy to modify.

## Book library, backlog, and recommendations

Books remain `knowledge.source` objects with `source_type: book`. The library tracks the full reading universe:

- **reading lifecycle** (`status`): unread, reading, paused, finished, abandoned, reference
- **ownership/access** (`ownership_status`): owned_physical, owned_digital, borrowed, wishlist, not_owned, unknown

This separation lets a book be owned but unread, wishlisted but not owned, finished but borrowed, etc.

### Adding books naturally

The OS infers ownership and reading status from natural language:

- "I bought The Box." → `owned_physical`, `unread`
- "I have Dune on Kindle." → `owned_digital`, `unread`
- "Add Fooled by Randomness to my wishlist." → `wishlist`, `unread`
- "I finished The Psychology of Money years ago." → keep ownership, `finished`
- "I borrowed this from someone." → `borrowed`, `unread`

Only ask for clarification when both ownership and reading status remain ambiguous.

### Recommendations

`skills/knowledge/recommend-next-book.md` supports:

- "What should I read next?" — prefer owned unread and strong wishlist fits, but allow new discoveries
- "What should I buy next?" — prefer wishlist and not-owned books; exclude already-owned unless edition matters
- "What do I already own that I should read?" — restrict to owned unread/paused
- "Give me something completely different." — bias away from recent themes/authors/modes
- "What should I read after Dune?" — use the named book's themes, user reactions, and retained ideas

Each recommendation must explain *why* it fits, using user-grounded evidence (ratings, session insights, retained ideas, themes). Do not pretend preference is known when evidence is weak.

### Reading profile

A lightweight profile is derived from canonical data:

- recurring themes/domains from ideas and sessions
- fiction/nonfiction balance
- technical depth and narrative preference
- liked/disliked authors and abandoned books
- cross-domain connections

It is not a rigid personality profile and is revisable from behavior.

### Diversity and gap detection

The system can intentionally diversify recommendations:

- mostly technical books → suggest fiction or narrative history
- lots of systems/strategy → suggest history, biography, or culture
- many wishlist items but owned unread backlog → surface owned backlog
- repeated authors/topics → suggest breadth

Diversity is not forced if the user clearly wants depth in one area.

### Recommendation provenance and feedback

- Discovered books are not marked owned or wishlist without user action.
- Recommendations are explained with user-grounded reasons.
- User feedback is captured: "I already read that", "I own that", "that sounds boring", "add to wishlist", "I want fiction next", etc.

## End-to-end v1 lifecycle

```
DISCOVER
→ ADD / ACQUIRE (bootstrap-library, manage-book-library)
→ QUEUE (build-reading-queue)
→ PRE-ASSESS (pre-reading-assessment)
→ START (start-reading)
→ READ
→ ACTIVE RECALL (active-recall)
→ DISCUSS (guided-reading-reflection, spoiler-aware-discussion)
→ CONNECT (cross-book-synthesis, cross-reading-retrieval)
→ CAPTURE (reading-session)
→ RETAIN (compress-session, schedule-review)
→ REVIEW (review-reading, surface-due-reviews)
→ FINISH (finish-reading)
→ SYNTHESIZE (generate-summary)
→ RECOMMEND NEXT (recommend-next-book, book-recommendation)
```

Each step works from canonical `ethan-life` data and does not require Notion or external infrastructure.

## Manual v1 usability test

Use two books: *Dune* (fiction, very familiar user, strict spoiler policy) and *Thinking in Systems* (nonfiction, limited familiarity).

1. "I'm starting Dune."
2. "Very familiar. I know the movies and most of the story. I want to focus on politics, religion, power structures, and what the movies leave out."
3. "Finished pages 1-20."
4. Offer spontaneous observations. Expected: no redundant recall prompt; questions adapt to high familiarity; spoiler policy respected; session saved; retention items identified.
5. "I'm starting Thinking in Systems."
6. "Finished 1-15." Expected: active recall first if observations weren't offered; nonfiction discussion; connections extracted; retention scheduled.
7. "What am I reading?"
8. "What do I need to review?"
9. "What ideas from books have I connected to work?"
10. "Build me my next 5-book queue."

The experience should feel conversational and low-friction.

## Knowledge extraction

Session objects can hold insights, connections, predictions, applications, and questions. Promote an insight to `knowledge.idea` only when it is:

- reusable outside the immediate passage,
- meaningfully distinct,
- likely useful for later retrieval.

## Provenance

- Every object records `provenance.agent_version` and `provenance.provenance_note`.
- `user_observations` preserves the user's words.
- `discussion_summary` is explicitly AI synthesis.
- Ideas promoted from sessions carry a link back to the session and source.

## Notion sync

Notion `knowledge_db` projects reading fields (current page, status, mode, dates, source access, alignment, ingestion status, ownership, format, tags) from `reading-state.yaml`, `knowledge.source`, and `knowledge.reading-profile`. Useful views include Reading Now, Owned / Unread, Wishlist, Finished, Paused, and Abandoned. Due reviews may be projected from `retention-state.yaml` by a future scheduler or UI. Notion is not authoritative. Canonical state remains in `ethan-life`.

## Storage locations

- Behavior / schemas / workflows / skills: `ethan-os/`
- Canonical books, profiles, sessions, reading state, retention state: `ethan-life/domains/knowledge/`
- Demo fixtures / tests: `ethan-os/config/demo-personality/fixtures/domains/knowledge/`

## Extending reading modes

Add a new enum value to:

- `schemas/domains/knowledge/source.schema.yaml` `reading_mode`
- `schemas/domains/knowledge/reading-session.schema.yaml` `reading_mode`
- `skills/knowledge/guided-reading-reflection.md`
- `ethan-notion/manifests/databases.yaml` `Reading mode` select options
