# Workflow: capture-set-audition-feedback

## Purpose

Process a natural-language observation given during an active DJ-set audition and update the
correct canonical record: the track's permanent DJ profile, this set's track relationship, or
transition knowledge between two tracks.

## Trigger

Any message during an active set audition (i.e. `ethan-life/domains/music/sessions/active-set-audition.yaml`
exists), such as:

- `This is more of a builder.`
- `Way too aggressive here.`
- `This works perfectly after track 4.`
- `Move this toward the end.`
- `This is a tool.`
- `Energy 4.`
- `Great transition into X.`
- `Don't use these two together.`
- `next`
- `done`

If there is no active single-release listening session (`current.yaml`) but there is an active set
audition, route here instead of `capture-listening-note`. If both are somehow active, prefer this
workflow while a set audition is in progress and ask Ethan if genuinely ambiguous.

## Inputs

- Ethan's note
- `ethan-life/domains/music/sessions/active-set-audition.yaml`
- `ethan-life/data/music/dj-sets/set_tracks.csv`
- `ethan-life/data/music/record-collection/tracks.csv`
- `ethan-life/data/music/record-collection/dj_track_profiles.csv`

## Outputs

- Updated `tracks.csv` and/or `dj_track_profiles.csv` (permanent track profile updates)
- Updated `set_tracks.csv` row(s) for this set (position, role_in_set, transition_notes,
  evidence_level)
- Updated or cleared `active-set-audition.yaml`
- Updated Notion Track/DJ Sets pages (via `ethan-notion` sync scripts), when applicable

## Steps

1. Load `active-set-audition.yaml`. If it doesn't exist, tell Ethan and offer
   `audition-dj-set` to start one.
2. Run `ethan-os/skills/music/classify-dj-set-feedback.md`.
3. If `action: end_audition`: ask Ethan whether the set should move to `confirmed` (ready to play
   as-is), stay `auditioning` (partial review), or just pause — update `sets.csv.status`
   accordingly, archive `active-set-audition.yaml` to
   `domains/music/sessions/<timestamp>-<set_id>-audition.yaml`, and clear the active file.
4. If `action: next_track`: advance `current_position` in `active-set-audition.yaml` and confirm
   the next track.
5. If `action: update_track_profile`: update `tracks.csv` and/or `dj_track_profiles.csv` exactly as
   `resolve-listening-note` would for the equivalent fields, then mark the corresponding
   `set_tracks.csv` row's `evidence_level` as `observed` (or `mixed`).
6. If `action: update_set_track` or `reorder`: update the matching row(s) in `set_tracks.csv`
   (`role_in_set`, `position`, `evidence_level`) for this `set_id` only.
7. If `action: update_transition`: update `transition_notes` on the relevant `set_tracks.csv`
   row(s), naming both tracks involved, and mark `evidence_level: observed` for that placement.
8. If `action: clarify`: ask Ethan the clarifying question; do not write anything yet.
9. Run the appropriate `ethan-notion` sync for anything that changed (track fields via
   `sync_release.py <release>`; set fields via the DJ Sets sync script once available).
10. Return a concise confirmation of what was recorded and where (track profile vs. this set vs.
    transition), and the next track if relevant.

## Constraints

- Never invent a track or position not present in the active audition tracklist.
- Never silently promote a set-specific observation into the permanent track profile (see
  `instructions/domains/music/instructions.md` feedback-routing rules).
- Missing values remain blank; existing values are preserved unless the note explicitly changes
  them.
