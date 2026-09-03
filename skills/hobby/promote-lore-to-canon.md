# Skill: promote-lore-to-canon

## Purpose

Convert an approved `hobby.lore-candidate` into canonical `hobby.lore-canon` or merge it into an existing canon entry while preserving provenance.

## Input

- Approved candidate object.
- Existing lore-canon entries that relate to the same topic.

## Output

- A new or updated `hobby.lore-canon` Markdown file.
- Updated candidate status (`merged`) with `canon_id_if_merged`.

## Instructions

1. Determine whether to create a new lore-canon entry or append to an existing one.
2. Set `lore_type` based on the candidate category and existing canon structure.
3. Preserve the candidate's source IDs in `derived_from_candidate_ids`, `source_battle_ids`, and/or `source_session_ids`.
4. Set `status` to `developing` unless the user explicitly marks it `locked`.
5. Write or update the canon file. If updating, append a revision note rather than overwriting.
6. Mark the candidate as `merged` and record the new canon ID.
7. Confirm the promotion and any implications for related collection items.
