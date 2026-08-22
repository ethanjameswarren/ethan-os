# Music domain invariants

## Ownership

- `ethan-os` owns the lookup, listening-session, and capture behavior.
- `ethan-life` owns the canonical collection data, session state, and provenance log.
- `ethan-notion` only maps canonical records into the live Notion databases.

## External sources

- External lookup is enrichment only. It never becomes the source of truth.
- Cross-check multiple sources when practical.
- Prefer exact catalog/release-number matches.
- If multiple plausible matches exist, present candidates and ask Ethan to choose.
- Never fabricate missing track names, artists, positions, durations, years, or labels.

## Fields that may be populated from external sources

Albums:
- Release
- Label
- Year
- Album
- Artists

Tracks:
- Release
- Side
- Artist
- Track
- Length

## BPM policy

- BPM may be pre-filled from external sources only when a sufficiently credible source explicitly provides it.
- Never infer BPM from genre, style, or other tracks.
- Do not overwrite an existing Ethan-entered BPM.
- If external sources disagree materially, leave BPM blank.
- Record that BPM came from an external source in the lookup provenance log.

## Fields that belong to Ethan only

Unless Ethan explicitly asks the AI to interpret his listening notes, external sources and the AI must not pre-fill:

- Energy
- Rating
- Special
- Base
- Tags
- Comment

The AI may structure Ethan's natural-language listening observations into these fields.

## Canonical write order

1. Resolve the release and build/update the canonical CSV rows in `ethan-life`.
2. Append the lookup provenance row to `lookup-log.csv`.
3. Write the listening-session state in `ethan-life`.
4. Run targeted Notion synchronization from `ethan-notion`.
5. If Notion sync fails, preserve the canonical CSV update and report the failure. Do not roll back canonical state.

## Session behavior

- After a release is confirmed, keep it in session context until Ethan says `done`, `next release`, or starts a new lookup.
- Track references like `A1` or `B2` resolve against the current session tracklist.
- Missing information is valid and remains blank.
- Do not force completion of every field before moving on.
