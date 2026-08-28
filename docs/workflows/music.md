# Workflow: Build a DJ Set

## What you do

Describe the kind of set you want, the mood, energy, duration, and any tracks or releases you already know should be included.

Example:

> **You:** "I want a warm-up set for a 3-hour party. Mostly deep house, around 120-124 BPM, no vocals for the first hour."

## What Ethan OS does

1. Captures the set definition and constraints.
2. Searches your collection for tracks matching the criteria.
3. Builds an ordered candidate set respecting energy progression, key flow, and time.
4. Lets you audition, swap, and mark feedback.
5. Finalizes the set and optionally exports it to a private Spotify playlist or prints Avery labels for the records.

## Conceptual stages

- **Define** — capture intent, constraints, and any fixed selections.
- **Find** — identify candidate tracks from your collection.
- **Arrange** — order tracks for flow, energy, and key compatibility.
- **Audition** — play through and capture feedback.
- **Refine** — adjust based on your reactions.
- **Export** — Spotify playlist, label sheet, or simple tracklist.

## Outputs

- A DJ Set object with tracklist and ordering.
- Audition feedback and classification of suggested changes.
- Optional Spotify playlist export log.
- Optional Avery 5160 label sheet for physical records.

## Safeguards

- Your personal judgments (energy, tags, comments) are never overwritten by external metadata.
- Track IDs remain stable across lookups.
- Spotify export is one-way and creates a private playlist by default.
- Lookup disagreements on BPM, key, or track identity are surfaced, not silently resolved.

## Technical details

- Workflows: `workflows/music/build-dj-set.md`, `audition-dj-set.md`, `export-dj-set-to-spotify.md`
- Skills: `skills/music/build-dj-set-candidates.md`, `skills/music/assess-track-for-dj-use.md`, `skills/music/classify-dj-set-feedback.md`
- Data: `ethan-life/data/music/record-collection/dj_track_profiles.csv`
- Scripts: `scripts/spotify/`
- Templates: `templates/`
