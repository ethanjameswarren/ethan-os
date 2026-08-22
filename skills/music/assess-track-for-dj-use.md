# Skill: assess-track-for-dj-use

## Purpose

Produce (or refresh) one track's persistent AI DJ assessment, reusing already-stored data before
any external lookup, and persist it to
`ethan-life/data/music/record-collection/ai_track_assessments.csv`. This is the sole writer of
that file — no other skill or workflow writes to it.

## Assessment schema (current version: 1)

One row per assessed track, keyed by `track_id`:

| field | meaning |
|---|---|
| `track_id` | Matches `Track ID` in `tracks.csv`. |
| `ai_style` | Style/substyle read, e.g. "Minimal Techno, Hypnotic". |
| `ai_energy` | Estimated energy, 1-5. |
| `ai_role_suggested` | Comma-separated likely role(s) from opener/builder/driver/peak/tool/reset/closer. |
| `ai_descriptors` | Comma-separated descriptive tags (groove/mood character). |
| `ai_mixing_notes` | Mixing considerations (breakdowns, long intro/outro, transition risk, etc.). |
| `ai_summary` | 1-2 sentence concise assessment. |
| `ai_confidence` | `high` \| `medium` \| `low`. |
| `ai_evidence_sources` | One of `local_metadata_only`, `local_metadata+ethan_listening`, `local_metadata+external_lookup`, `full` (local metadata + Ethan listening data + external lookup). |
| `assessment_version` | `1` (this skill's current method version — bump if the method changes materially). |
| `source_fingerprint` | See "Fingerprint" below. |
| `assessed_at` | ISO timestamp. |

## Input

- `track_id` (required)
- `mode`: `assess_if_missing` (default) | `force_reassess`
- Already-loaded `tracks.csv` row for this track, its `albums.csv` row, any `dj_track_profiles.csv`
  row, and any `lookup-log.csv` rows for the release (source URLs already gathered by a prior
  `lookup-release` call)
- The existing `ai_track_assessments.csv` row for this track, if any

## Fingerprint

Compute `source_fingerprint` as a short hash (e.g. first 12 hex chars of a SHA-1) of the
pipe-joined, trimmed values of: `BPM`, `Key`, `Base`, `Tags`, `Comment`, `Energy`, `Rating`,
`Special` (from `tracks.csv`) and `dj_role_confirmed`, `mix_notes`, `listened_at` (from
`dj_track_profiles.csv`). Recompute it fresh each time this skill runs.

## Staleness check (run before doing any work)

An existing assessment is stale if either is true:

- its `source_fingerprint` differs from the freshly computed one, or
- its `assessment_version` is less than the current version (`1`).

## Instructions

1. If `mode: assess_if_missing` and a non-stale assessment already exists for `track_id`, do
   nothing and return the existing row (this is the normal "reuse before research" path — callers
   should not invoke this skill for tracks that already have a fresh assessment).
2. Otherwise, gather inputs, preferring already-stored data over any new external call:
   - Objective metadata from `tracks.csv` (`Artist`, `Track`, `Length`, `BPM`, `Key`) and
     `albums.csv` (`Label`, `Year`, `Album`, `Artists`, `Comment`).
   - Ethan's existing data, if any: `tracks.csv` (`Energy`, `Rating`, `Special`, `Base`, `Tags`,
     `Comment`) and `dj_track_profiles.csv` (`dj_role_confirmed`, `mix_notes`, `listened_at`).
   - Any source URLs already recorded in `lookup-log.csv` for this release — reuse their content
     if still relevant rather than re-fetching.
3. Determine whether the locally available information is sufficient for a meaningful assessment
   (i.e. more than just BPM and a release title). If not, and only then, run a bounded external
   lookup (reuse `skills/music/lookup-release.md`'s source priority — Discogs, Hard Wax, label/
   Bandcamp, other stores) focused on style/genre context, not re-verifying facts already
   confirmed in the canonical store.
4. Set `ai_evidence_sources` based on what was actually used:
   - `local_metadata_only`: only `tracks.csv`/`albums.csv` objective fields.
   - `local_metadata+ethan_listening`: also used Ethan's subjective fields.
   - `local_metadata+external_lookup`: also used a fresh external lookup, no Ethan listening data.
   - `full`: used all three.
5. Produce `ai_style`, `ai_energy`, `ai_role_suggested`, `ai_descriptors`, `ai_mixing_notes`, and
   `ai_summary` from the gathered evidence. Weight Ethan's existing subjective fields heavily when
   present (they describe the actual track, not just its metadata) but keep them **advisory
   input** to the AI's own read — do not just copy Ethan's `Energy`/`Tags` verbatim into the AI
   fields; that would blur the independence this file exists to preserve.
6. Set `ai_confidence`:
   - `high`: strong local listening data and/or multiple consistent external sources.
   - `medium`: reasonable metadata/style signal but no listening data, or a single external source.
   - `low`: sparse metadata, no listening data, no external corroboration.
7. Write/replace the row for `track_id` in `ai_track_assessments.csv` with `assessment_version: 1`,
   the freshly computed `source_fingerprint`, and `assessed_at` set to now.
8. Mirror `ai_role_suggested` into `dj_track_profiles.csv.dj_role_suggested` for this `track_id`
   (create the row if it doesn't exist yet; only touch `dj_role_suggested` and `updated_at` — never
   touch `dj_role_confirmed`, `mix_notes`, or `listened_at`).
9. Return the new/updated assessment row and whether it was newly created, refreshed, or left
   unchanged.

## Constraints

- Never write to `tracks.csv` or overwrite any Ethan-owned field.
- Never overwrite `dj_role_confirmed`, `mix_notes`, or `listened_at` in `dj_track_profiles.csv`.
- Never fabricate specifics presented as fact; `ai_summary`/`ai_mixing_notes` should read as
  interpretation, not as a claim of having heard the track.
- `mode: force_reassess` always regenerates, ignoring the staleness check (used for explicit
  "reassess this track" requests).
