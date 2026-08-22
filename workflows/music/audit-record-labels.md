# Workflow: audit-record-labels

## Purpose

Report the physical labeling state of the collection (or a scoped subset), grouped usefully by
what action is needed, at both the release and track level — never a single "incomplete" flag.

## Trigger

- `Audit my record labels.`
- `What records still need labels?`
- `What labels are ready to print?`
- `What do I need to listen to before I can finish labeling them?`
- `What labels are blocked only by factual metadata?`

## Inputs

- `ethan-life/data/music/record-collection/albums.csv`
- `ethan-life/data/music/record-collection/tracks.csv`
- `ethan-life/data/music/record-collection/ai_track_assessments.csv`
- `ethan-life/data/music/record-collection/physical_label_status.csv`

## Outputs

- A grouped audit report (no writes — this is read-only)

## Steps

### 1. Determine scope

Default: the whole collection. Ethan may scope by release, artist, style, or a data-readiness/
physical-status filter (e.g. "which techno releases need listening data").

### 2. Evaluate readiness

Run `ethan-os/skills/music/evaluate-label-readiness.md` for every album and track in scope.

### 3. Group results

Produce these groups at both the album level and the track level:

- **Ready to print**: `data_readiness: printable` or `complete`, `print_status: not_printed`.
- **Needs lookup**: has a `gap_reasons` entry with `category: objective_metadata` or
  `external_context`.
- **Needs listening**: has a `gap_reasons` entry with `category: ethan_listening`. If
  `ai_assessment_available` is true for a track in this group, say so explicitly (e.g. "Ethan data
  missing; AI assessment available, medium confidence") — informational only, never presented as
  equivalent to Ethan's own data.
- **Printed but not applied**: `print_status: printed`, `application_status: not_applied`.
- **Needs sticker work** (tracks only): `sticker_color_applied` or `bpm_written` is false, even if
  the Avery label itself is fully printed/applied.
- **Fully complete**: `data_readiness: complete`, printed, applied, and (tracks) stickered/BPM
  written.

A single entity may appear in more than one group (e.g. "needs lookup" and "needs listening" at
once) — report it in every group that applies rather than picking one.

### 4. Report collection-level metrics

When auditing the whole collection (or a large scope), include counts: releases total, tracks
total, album labels complete, album labels ready to print, tracks fully labeled, tracks ready to
print, tracks needing listening, tracks needing lookup, tracks needing sticker/BPM work, and a
rough percent-complete figure (fully complete / total).

### 5. Offer next steps

- If Ethan asks for "ready to print", hand off to `print-record-labels`.
- If Ethan asks what to listen to, list the specific tracks/releases and offer to hand off to
  `lookup-release-and-listen` (starting with the first one, per Ethan's request).
- If Ethan asks what's blocked only by factual metadata, list those and offer to hand off to the
  lookup skill/workflow.
- After a listening session or a lookup/enrichment run updates the underlying data, re-run this
  audit (or the relevant slice of it) rather than trusting a previously reported status — readiness
  is always computed fresh, never cached.

## Confirmation policy

- Auto-execute: the entire audit (read-only, no canonical or physical-status writes).
