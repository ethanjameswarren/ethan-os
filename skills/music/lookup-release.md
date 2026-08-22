# Skill: lookup-release

## Purpose

Identify a music release from minimal input and retrieve objective Album/Track metadata from external sources.

## Input

- `query`: the natural-language identifier provided by Ethan (e.g., `SK11X025`, `KW34`, `Holden Federico - Dust`).
- `existing_albums`: set of release catalog numbers already in the canonical collection.
- `existing_tracks`: optional tracklist data already in the canonical collection.

## Output

- `candidates`: list of candidate releases, each with:
  - `release` (catalog/release number)
  - `label`
  - `year`
  - `album` title
  - `artists`
  - `tracklist` (side, artist, track, length, optional BPM)
  - `source_urls`
  - `confidence`: high | medium | low
- `best_match`: the single best candidate, or `null` if none.
- `notes`: why the candidate was chosen, any ambiguity, and what remains unverified.

## Search priority

1. Exact catalog/release number (`SK11X025`, `KW34`, `RYCL016`).
2. Label + catalog number.
3. Artist + release title.
4. Other identifying information only if required.

## External sources

Use `web_search` and `webfetch` in this order:

1. **Discogs** — `site:discogs.com <identifier>`.
2. **Hard Wax** — `site:hardwax.com <identifier>`.
3. **Official label pages / Bandcamp** — `<identifier> <label> Bandcamp` or label site.
4. **Other reputable record stores** (Juno, Decks, Red Eye, etc.).
5. **SongBPM** — `https://songbpm.com/` for explicit track-level BPM values.
6. **Broader web search** only if the above fail.

## Instructions

- Always attempt at least Discogs + one other source when the first source returns a match.
- Cross-check tracklists across sources. If sources disagree on track names, positions, or the number of tracks, lower confidence and mention the conflict.
- Prefer the source that explicitly lists the catalog number matching the query.
- Do not fabricate missing values. Leave them blank.
- Do not pre-fill subjective fields (Energy, Rating, Special, Base, Tags, Comment).
- Apply the external-BPM policy: only include BPM if a credible source (e.g., SongBPM) explicitly lists it; do not infer it; do not overwrite an existing Ethan-entered BPM.

## Confidence rules

- **high**: exact catalog match, consistent tracklist across sources, label and year confirmed.
- **medium**: exact catalog match but only one source, or artist+title match with one clear release.
- **low**: multiple plausible releases, or only partial metadata found.
- **none**: no reliable match found.

## Ambiguity handling

If confidence is not high and more than one candidate exists:

- Present the top candidates (label, year, format/country if known, track count).
- Explain briefly how they differ.
- Ask Ethan to select the correct one before writing anything to the canonical store.
