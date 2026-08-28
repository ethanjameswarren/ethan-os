# Workflow: build-reading-queue

## Purpose

Create, update, or reorder a coherent reading queue from the user's library and goals.

## Triggers

- "Build me my next 5-book queue."
- "Put Dune next."
- "Make Thinking in Systems my next book."
- "Move Good Strategy after Dune."
- "Remove this from the queue."
- "What's my reading queue?"

## Steps

1. Load `ethan-life/domains/knowledge/reading-state.yaml`.
2. Load all `knowledge.source` objects with `source_type: book` from `ethan-life/domains/knowledge/sources/`.
3. Load relevant `knowledge.reading-profile` objects.
4. Parse user intent:
   - build/rebuild queue → use `skills/knowledge/build-reading-queue.md` to generate a coherent sequence.
   - move/reorder → adjust `reading_queue` order or status without full rebuild.
   - remove → set the entry `status: removed` or delete it.
   - show → read and summarize the current queue.
5. Run `skills/knowledge/build-reading-queue.md` when building/rebuilding.
6. Ensure `reading-state.yaml` remains the canonical state. Do not duplicate queue state in Notion or other places.
7. Validate and write.

## Output

- updated `reading-state.yaml`
- concise queue summary with reasons

## Confirmation policy

Auto-execute. Queue changes are low-risk. Ask for confirmation only if a request would remove an active book from the queue or overwrite a user-defined order.
