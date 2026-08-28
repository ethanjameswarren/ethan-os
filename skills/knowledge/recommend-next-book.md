# Skill: recommend-next-book

## Purpose

Recommend the next book to read or buy based on the user's library, reading history, retention data, derived profile, and stated mood/context.

## Input

- All `knowledge.source` objects with `source_type: book` from `ethan-life/domains/knowledge/sources/`
- `ethan-life/domains/knowledge/reading-state.yaml`
- `ethan-life/domains/knowledge/retention-state.yaml`
- `knowledge.reading-session`, `knowledge.idea`, and `knowledge.summary` objects as needed
- User's query and any stated constraints (e.g., "from what I own", "something different", "after Dune")
- Optional external discovery results

## Output

- A ranked list of 1-5 recommendations, each with:
  - `source_id` if it exists in the library, or a candidate external book description
  - `title`, `author`
  - `reason`: user-grounded explanation of why it fits
  - `expected_ownership_action`: read_now | buy | borrow | add_to_wishlist | none
  - `confidence`: high | medium | low

## Recommendation logic

1. Determine the user's intent from the query:
   - "What should I read next?" → prefer owned unread and strong wishlist fits, but allow new discoveries.
   - "What should I buy next?" → prefer wishlist and not-owned books; exclude already-owned unless edition/replacement matters.
   - "What do I already own that I should read?" → restrict to `owned_physical`, `owned_digital`, or `borrowed` with `status: unread` or `paused`.
   - "Give me something completely different." → bias away from recent authors, themes, and reading modes.
   - "What should I read after X?" → use X's themes, user reactions, and retained ideas as the primary signal.

2. Build a lightweight reading profile from canonical data:
   - preferred domains/themes from session insights, ideas, summaries
   - fiction/nonfiction balance from recent sources
   - technical/narrative depth from `discussion_depth` and `reading_mode`
   - authors/styles repeatedly responded to or rated highly
   - abandoned books and low ratings as negative signals
   - recurring cross-domain connections (e.g., systems, uncertainty, incentives)

3. Score candidates:
   - Relevance to derived profile and recent themes.
   - Match to stated mood/context.
   - Ownership: mild preference for owned unread to reduce unnecessary buying, but do not let ownership dominate fit.
   - Recency of purchase/wishlist: newer owned unread or wishlist items may score higher.
   - Diversity: if recent reading has been narrow, optionally suggest a different mode/theme.
   - Difficulty/length match when known.
   - Avoid recently recommended books the user rejected or ignored unless context changes.

4. Do not restrict candidates to the known library. External discovery is allowed, but a discovered book should not be marked owned or wishlist without user action.

5. Explain each recommendation using user-grounded evidence:
   - Reference specific retained ideas, ratings, themes, or patterns.
   - Do not pretend a preference is known when evidence is weak.
   - Example good reason: "You've repeatedly responded to systems, incentives, and uncertainty. *The Black Swan* would extend that into rare-event risk and the limits of prediction."

## External discovery

- If external search is available, use it to find candidate books that match the derived profile.
- Clearly distinguish discovered metadata from user-owned data.
- Match discovered books against existing sources by title/author/ISBN to avoid duplicate Source objects.
- Do not create a new `knowledge.source` for a discovered book until the user marks it as wishlist, owned, or starts reading it.

## Feedback handling

- "I already read that." → update source `status` to `finished` if not already; remove from recommendations.
- "I own that." → update `ownership_status` accordingly.
- "That sounds boring." / "Not interested in that author." → record negative signal; avoid similar for a while.
- "Add that to my wishlist." / "Buy-list it." → create/update source with `ownership_status: wishlist`.
- "I want something lighter/heavier/fiction/nonfiction." → apply as query context for this and future recommendations.

## Diversity / gap detection

Optional: surface gaps in the user's recent reading:
- mostly technical books → suggest fiction or narrative history
- mostly systems/strategy → suggest history, biography, or culture
- many wishlist items but several owned unread → surface owned backlog
- repeated authors/topics → suggest breadth

Only push diversity if the user's query is open-ended or they explicitly ask for a change.
