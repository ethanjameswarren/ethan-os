# Skill: compress-session

## Purpose

At the end of a meaningful session, distill the discussion into a small set of durable takeaways for retention.

## Target

0-3 review-worthy items per session. Default to 1-2.

## What counts as a durable takeaway

- A concept the user would benefit from remembering months later.
- A mental model or principle.
- A personally meaningful interpretation.
- A useful question or application.
- A cross-domain connection.

## What to skip

- Trivial details.
- One-off observations with no reuse value.
- Already-promoted `knowledge.idea` objects unless the session adds a new angle.

## Rules

1. Prefer promoting strong takeaways to `knowledge.idea` when they are reusable outside the session.
2. For session-level insights worth reviewing but not globally reusable, keep them in `knowledge.reading-session.extracted_insights` and track them in `retention-state.yaml` via a stable `insight_id`.
3. Set `retention_priority` on each insight:
   - `high`: user explicitly marked important, or insight is clearly central
   - `normal`: useful but not critical
   - `low`: minor; do not schedule unless user overrides
4. Do not create summaries that merely restate the book. Capture the user's understanding, reactions, and applications.
5. Preserve the distinction between source-derived facts, user interpretation, and AI synthesis.

## Output

- `compressed_takeaways`: list of `{insight_id, title, note, retention_priority}`
- `promote_to_idea`: subset that should become `knowledge.idea` objects
