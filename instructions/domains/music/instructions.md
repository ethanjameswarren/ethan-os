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
- Comment (release-level descriptive blurb, typically Hard Wax-style; distinct from the Ethan-only `Comment` on Tracks — see "Physical record labeling" below. This was missing from this list even though it's already how the field is used in practice; corrected here rather than introducing a new field.)

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

## Track identity

- Every track has a stable `Track ID` in `tracks.csv`, derived as `<Release>-<Side>` (with a `-2`, `-3`, ... suffix only if a release genuinely has more than one track sharing a `Side` label). Never re-derive or reassign an existing `Track ID`.
- `Key` (musical/Camelot key) is objective track metadata and follows the same external-sourcing policy as BPM (see above): only from a credible explicit source, never inferred, never overwriting an Ethan-entered value, blank on disagreement.

## DJ set-building

### Ownership

- `ethan-os` owns set-building, auditioning, and feedback-classification behavior (`workflows/music/build-dj-set.md`, `audition-dj-set.md`, `capture-set-audition-feedback.md`, `manage-dj-set.md`).
- `ethan-life` owns canonical DJ interpretation (`data/music/record-collection/dj_track_profiles.csv`) and set state (`data/music/dj-sets/sets.csv`, `set_tracks.csv`).
- `ethan-notion` exposes DJ-relevant properties on the existing `Tracks` database and a new read-oriented `DJ Sets` database; it does not own ordering or set-construction logic.

### Honesty policy (core invariant for this capability)

- Metadata (BPM, Key, genre/style tags, label/release context) can generate a plausible **candidate** set. It is never proof of how a track actually sounds or mixes.
- Only Ethan's confirmed listening observations (Energy, Rating, Tags, Special, Comment in `tracks.csv`; `dj_role_confirmed`/`mix_notes`/`listened_at` in `dj_track_profiles.csv`) count as **observed** evidence.
- Every track placed in a candidate set must be recorded in `set_tracks.csv` with an `evidence_level` of `observed`, `inferred`, or `mixed`, and a short `added_reason`.
- When presenting a set to Ethan, explicitly and separately call out tracks/transitions whose placement is `inferred` rather than `observed`. Do not phrase inferred characteristics ("this will sound driving", "this will mix well into X") as settled fact — phrase them as reasoning from metadata ("BPM and tags suggest this could work as a driver, but you haven't listened to it").
- AI-suggested DJ roles are written only to `dj_role_suggested`. A role only moves to `dj_role_confirmed` (the permanent, authoritative track profile) when Ethan explicitly confirms it. `role_in_set` on a `set_tracks.csv` row may differ from `dj_role_confirmed` and does not require the same confirmation bar, since it is scoped to one set and can be revised freely during auditioning.

### Evidence priority for candidate generation

See "AI track assessment" below for the current evidence priority order — it supersedes a plain
BPM/Key/style/AI-inference list with the persistent AI assessment layer inserted. The rule that
matters most stays constant: do not over-optimize for harmonic (key) compatibility; it is one
signal among several, not a hard constraint.

### Set lifecycle

`candidate` → `auditioning` → `confirmed` → `played` → `archived` (tracked in `sets.csv.status`). A freshly built set is always `candidate`; it only becomes `auditioning` when Ethan starts listening through it, and `confirmed`/`played`/`archived` only on Ethan's explicit instruction. Track-level state within a set (`set_tracks.csv.status`: `proposed`/`confirmed`/`removed`) is independent of the set's overall status.

### AI track assessment (persistent, reusable)

`ethan-life/data/music/record-collection/ai_track_assessments.csv` holds a persistent,
reusable AI-generated DJ assessment per track (style, estimated energy, likely role(s),
descriptors, mixing considerations, a concise summary, confidence, evidence sources, an
assessment-method version, a source fingerprint, and a timestamp). See
`skills/music/assess-track-for-dj-use.md` for the schema and generation rules.

Purpose: so `build-dj-set` reuses prior AI reasoning about a track instead of re-researching or
re-interpreting it from scratch on every request. External research/interpretation is enrichment
that runs when useful evidence is missing, not the default path for every build.

**Independence from Ethan's data (hard rule):**

- The AI assessment is never written by, and never overwrites, Ethan's fields (`Energy`, `Rating`,
  `Special`, `Base`, `Tags`, `Comment` in `tracks.csv`; `dj_role_confirmed`, `mix_notes`,
  `listened_at` in `dj_track_profiles.csv`).
- Listening-capture and set-audition workflows (`capture-listening-note`, `resolve-listening-note`,
  `capture-set-audition-feedback`, `classify-dj-set-feedback`) never write to
  `ai_track_assessments.csv`. The AI assessment only changes via explicit (re)assessment
  (`enrich-dj-track-assessments` / `assess-track-for-dj-use`).
- `AI energy = 4` and `Ethan Energy = 3` are both valid, coexisting facts about the same track.
  Disagreement is preserved and visible, not resolved by deletion.
- `ai_role_suggested` is non-authoritative. It only becomes `dj_role_confirmed` when Ethan
  explicitly confirms it, exactly like any other AI-suggested role.

**Reuse before research** — normal set construction (`build-dj-set`) does, in order:

1. Load eligible tracks (`tracks.csv`).
2. Load Ethan's data (`tracks.csv` subjective fields, `dj_track_profiles.csv`).
3. Load persisted AI assessments (`ai_track_assessments.csv`).
4. Filter/rank candidates using the evidence priority below.
5. Identify meaningful knowledge gaps only (tracks that are strong candidates by objective
   filters but have no usable assessment).
6. Perform targeted enrichment for those gaps only, bounded per request (see
   `workflows/music/build-dj-set.md`) — never a full-collection re-query as part of a normal build.
7. Construct the candidate set.

**Evidence priority for candidate generation** (supersedes the plain list previously here):

1. Ethan's confirmed listening observations (`Energy`, `Rating`, `Special`, `Tags`, `Comment`,
   `dj_role_confirmed`, `mix_notes`, `listened_at`).
2. A persisted, non-stale AI track assessment (`ai_track_assessments.csv`) — reusable structured
   evidence, cheaper and preferred over fresh ad hoc inference, but still not Ethan's own judgment.
3. `BPM`.
4. `Key` (supporting evidence only, never a hard constraint).
5. External stylistic descriptors / label context (`Base`, `albums.csv`, `lookup-log.csv`).
6. Fresh, uncached AI inference — only when no usable assessment exists and the gap is meaningful
   enough to justify targeted enrichment (see above); this should be rare in steady state.

Do not over-optimize for harmonic (key) compatibility; it remains one signal among several.

**When AI and Ethan disagree** on the same attribute (e.g. AI energy 4 / role driver vs. Ethan
energy 3 / role builder confirmed), favor Ethan's confirmed value for the actual placement
decision, but keep the AI's read as visible secondary evidence in `added_reason` rather than
discarding it. Do not apply a blanket rule that AI values are void whenever any Ethan value
exists elsewhere on the track — evaluate per attribute.

**Assessment freshness (staleness):**

- An assessment is stale if its `source_fingerprint` no longer matches the current inputs (BPM/Key
  correction, new `Tags`/`Comment`/`Special`, new `dj_track_profiles.csv` data), or if its
  `assessment_version` is older than the current method version.
- A `low` `ai_confidence` assessment is not automatically stale, but is a priority candidate for
  re-enrichment.
- Staleness is evaluated lazily, per track, when that track is touched (candidate generation,
  explicit reassessment, batch enrichment) — never as an automatic full-collection regeneration
  triggered by an unrelated single edit (e.g. Ethan logging one listening note does not
  invalidate the rest of the collection).

**Evidence-level definitions, restated with the AI assessment layer** (semantics unchanged from
the original DJ set-building design, clarified for this addition):

- `observed`: the decisive evidence for this placement/role came from Ethan's own confirmed data.
- `inferred`: the decisive evidence came only from objective metadata and/or the AI assessment,
  with no supporting Ethan data for that attribute.
- `mixed`: Ethan supplied some confirmed data relevant to the track, but the specific
  placement/role decision also relied on the AI assessment or other inference to fill a gap.

### Feedback routing during auditioning

During an active set audition, classify each of Ethan's observations (see `skills/music/classify-dj-set-feedback.md`) into exactly one of:

- **Permanent track profile** (`dj_track_profiles.csv`, or the existing Ethan-only fields in `tracks.csv`) — general statements about the track itself, independent of this set (e.g. "This is a tool", "Energy 4").
- **Set-track relationship** (`set_tracks.csv` row for this set) — statements scoped to this set's arrangement (e.g. "Move this toward the end", "This is more of a builder here").
- **Transition knowledge** (`set_tracks.csv.transition_notes`, referencing the adjacent track) — statements about how two specific tracks mix together (e.g. "This works perfectly after track 4", "Don't use these two together").

When ambiguous, prefer the narrower scope (set-track or transition) over silently promoting an observation to the permanent track profile.

## Physical record labeling

Ethan's physical system: a clear label area on the sleeve, a color sticker per track (with a
handwritten BPM), one printed Avery 5160 album label, and one printed Avery 5160 label per track.
**The database remains canonical; physical labels are a fast-reference derivative, generated from
it, never a second source of truth.**

### Ownership

- `ethan-os` owns label-readiness logic, print generation, the physical/print audit workflow, and
  missing-data classification (`workflows/music/audit-record-labels.md`, `print-record-labels.md`,
  `mark-record-labels.md`; `skills/music/evaluate-label-readiness.md`,
  `render-avery-5160-sheet.md`, `suggest-sticker-color.md`; `templates/avery-5160.sty`).
- `ethan-life` owns canonical album/track data (unchanged), plus the physical status/history files:
  `data/music/record-collection/physical_label_status.csv`, `print_batches.csv`,
  `sticker-color-taxonomy.md`, and generated output under `print-batches/`.
- `ethan-notion` may expose the persisted physical booleans (printed/applied/sticker/BPM) as
  presentation-only checkboxes; it does not compute or store readiness.

### Field mapping (no new canonical metadata fields)

**Album label** (`<<Year>> - <<Album>>` / `<<Release>> | <<Label>>` /
`BPM: <<Avg BPM>> | Energy: <<Avg Energy>> | Rating: <<Avg Rating>>` / `<<Comment (Hard Wax)>>`):
`Year`/`Album`/`Release`/`Label`/`Comment` come directly from `albums.csv` (see the corrected
external-sourceable fields list above for `Comment`). `Avg BPM`/`Avg Energy`/`Avg Rating` are
computed on demand from `tracks.csv` rows for that `Release` — never stored, never persisted as a
canonical field, so they can't drift from the underlying track data. Compute only over tracks with
a non-blank value for that field; a blank does not count as `0`. Round: BPM to the nearest whole
number, Energy and Rating to one decimal place. If a release has zero tracks with a value for a
given metric, omit that piece from the printed line rather than printing `0` or `N/A`.

**Track label** (`<<Energy>> - <<Track>>` / `<<Artist>>` / `<<Tag>>` / blank / `<<Comment>>`):
`Energy`/`Track`/`Artist`/`Tags`/`Comment` all come directly from the existing `tracks.csv`
columns — `Tag` reuses the canonical `Tags` field (no second tags concept). Print-time formatting
only (never mutates the canonical cell): show at most 2 tags, `/`-joined (e.g. `Boomy /
Atmospheric`); shorten `Comment` only if needed to fit (see the render skill's fitting rules).
`BPM`/`Key` are intentionally **not** on the printed track label — `BPM` is handwritten on the
physical sticker — but a missing `BPM` still surfaces in the audit under the sticker/lookup gap
bucket, since Ethan still needs it to write the sticker.

### Readiness — four distinct axes, always computed live (never cached as a stored boolean)

1. **Data readiness**: `blocked` (missing a required identity field — `Album`+`Release` for an
   album; `Track`+`Artist` for a track) | `printable` (required fields present; audit reports
   `gap_reasons` for missing desired fields) | `complete` (required and desired fields present).
   Desired-but-non-blocking fields: Album — `Year`, `Label`, Avg BPM, Avg Energy, Avg Rating,
   `Comment`; Track — `Energy`, `Tags`, `Comment`. A release/track missing only desired fields is
   still printable; it is never blocked for a subjective field Ethan simply hasn't gotten to yet.
2. **Print status** (`physical_label_status.csv.label_printed`): set only on Ethan's explicit
   confirmation that a sheet was actually printed — never merely because a `.tex`/PDF was
   generated (`print-record-labels` step: generate → confirm → mark).
3. **Application status** (`label_applied`): has the printed label been placed on the sleeve.
4. **Sticker status** (`sticker_color_applied`, `bpm_written`): track-only; blank/N/A for albums.

### Missing-data classification (say *why*, not just "incomplete")

- **Missing objective metadata** (BPM, artist, year, label, catalog/`Release`) → action: `lookup`
  (hand off to `lookup-release-and-listen` / the lookup skill).
- **Missing Ethan listening data** (Energy, Rating, Tags, Comment) → action: `listen` (hand off to
  the listening workflow).
- **Missing external context** (Hard Wax-style `Comment` on `albums.csv`) → action: `external
  lookup`.
- **Physical work incomplete** (not printed / printed but not applied / sticker missing / BPM not
  written) → action: `physical labeling` (handled by `print-record-labels`/`mark-record-labels`,
  not by data enrichment).

A single track/release may have gaps in more than one category at once; report all of them, not
just the first one found.

### AI assessment integration (do not print AI interpretation)

Physical labels print **only** Ethan's canonical fields. `ai_track_assessments.csv` is never a
source for printed label content. It may only be used to annotate an audit result — e.g. "Ethan
data missing; AI assessment available (medium confidence)" — to help Ethan prioritize what to
listen to next. Never let this annotation read as if the AI's `ai_energy`/`ai_descriptors` were
Ethan's own `Energy`/`Tags`.

### Sticker color taxonomy

Never assume or infer what a sticker color means. Read `sticker-color-taxonomy.md`; if it has no
rows yet, say plainly that the taxonomy hasn't been captured and ask Ethan to define it rather
than guessing. Once defined, `suggest-sticker-color` may reason from it plus canonical data (e.g.
if Ethan's taxonomy says "Red = Energy 4-5"), but the taxonomy file itself is only ever written by
Ethan's own input, never inferred by the AI.

### Print batching and partial sheets

- Default: select entities that are `printable`/`complete` (data readiness) and not yet
  `label_printed`, in canonical order (album label, then its tracks in `Track ID`/side order;
  release grouping preserved across a shared sheet), unless Ethan explicitly asks for reprints.
- Avery 5160 = 30 labels/sheet (3 columns x 10 rows). Support starting at any of the 30 positions
  for partially-used sheets (`sheet_start_position` in `print_batches.csv`); never require wasting
  a partial sheet.
- Generating a `.tex`/PDF is not printing. Only Ethan's explicit confirmation
  (`mark-record-labels`) sets `label_printed`/`confirmed_printed`.
