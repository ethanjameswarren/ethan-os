# Workflow: capture-listening-note

## Purpose

Process a natural-language observation about the current listening session and update the canonical Track record.

## Trigger

Any message during an active listening session, such as:

- `A1 energy 3, rating 4. Boomy and driving. Weapon.`
- `A2 favorite, groovy and trippy`
- `B1 rating 2`
- `next`
- `done`

## Inputs

- Ethan's note
- `ethan-life/data/music/record-collection/sessions/current.yaml`

## Outputs

- Updated `tracks.csv`
- Updated Notion Track page (via `sync_release.py`)
- Updated or cleared session state

## Steps

1. Load the current session state from `ethan-life/data/music/record-collection/sessions/current.yaml`.
2. If there is no active session, tell Ethan and offer to start one with `Start <release>`.
3. Run `ethan-os/skills/music/resolve-listening-note.md`.
4. If the action is `end_session`, archive `current.yaml` to `sessions/<timestamp>-<release>.yaml`, clear `current.yaml`, and confirm the session is closed.
5. If the action is `next_track`, update `current_track` in `current.yaml` and confirm the next track.
6. If the action is `update_track`, update the matching row in `tracks.csv` and run `ethan-notion/scripts/sync_release.py <release>`.
7. Return a concise confirmation of what was recorded.
