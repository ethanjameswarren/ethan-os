# Music & DJ Workflows

## What it does

Track a physical and digital record collection, capture listening notes, build DJ sets, evaluate tracks for mixing, and export sets to Spotify while keeping your personal taste judgments separate from external metadata.

## Why it exists

A record collection is a combination of objective release data and subjective judgments. Ethan OS keeps the two separate, so external lookups enrich your collection but never overwrite your personal ratings, energy tags, or mix assessments.

## What you do

- Mention a release you want to catalog or a track you want to assess.
- Capture listening notes in your own words.
- Build a DJ set from your collection and audition it.
- Export a finished set to a private Spotify playlist.
- Review Spotify matches when external data differs from your catalog.

## What Ethan OS does

- Resolves releases against external sources, then stores the canonical version in your collection.
- Captures listening-session notes and structures your own judgments into fields like energy, base, and tags.
- Assesses tracks for DJ use based on your collection data and past set notes.
- Builds candidate DJ sets from a pool, filters, and ordering constraints.
- Manages set versions, auditions, and feedback.
- Exports to Spotify with minimal scopes and does not read your listening history.
- Renders physical record labels for sets if you want to mark records with set stickers.

## Key ideas

- **External lookup is enrichment, not authority.** Spotify and other sources provide release metadata; your judgments are yours.
- **Track IDs are stable.** Once a track is cataloged, its identifier does not change.
- **Judgments are never inferred.** Energy, rating, tags, and DJ-use comments come from your notes, not from genre or popularity.
- **Spotify is one-way export.** Canonical data stays in your collection; Spotify only receives a playlist.

## Example interaction

> **You:** "I'm auditioning the new warm-up set. Track three feels too energetic."  
> **OS:** "Got it. I'll capture that as feedback on the audition. Track A2 is currently marked energy 5. Should I lower it to 3, or leave the track rating and just note it does not fit the set flow?"  
> **You:** "Leave the track rating. Note it breaks the flow."  
> **OS:** "Done. I'll update the set feedback and keep the track rating unchanged."

## What gets saved

- **Collection data** — releases, tracks, labels, and your catalog judgments.
- **Listening notes** — your observations about tracks, releases, and listens.
- **DJ set definitions** — tracklists, order, and notes.
- **Audition feedback** — structured reactions and suggested changes.
- **Spotify export records** — playlist IDs and match logs.

## Important behaviors

- Never overwrite an existing catalog judgment with external data.
- Never fabricate BPM, key, or track titles when sources disagree.
- Never publish a Spotify playlist as public without explicit instruction.
- Never treat a Spotify-side manual edit as canonical collection data.

## Related workflows

- [Build a DJ set](../workflows/music.md)
- [Spotify setup](../domains/music/spotify-setup.md)

## Technical implementation

- Workflows: `workflows/music/`
- Skills: `skills/music/`
- Data: `ethan-life/data/music/`
- Scripts: `scripts/spotify/`
- Templates: `templates/`
