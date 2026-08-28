# Ethan OS Releases

## v0.1.0-beta

### What Ethan OS is

Ethan OS is a reusable, public behavior layer for personal AI systems. It keeps behavior (workflows, skills, schemas, validation, and runtime instructions) separate from private personal data, which lives in a companion repository.

### Highlights

- Core runtime: intent routing, workflow selection, skill loading, schema validation, deterministic tests, and demo flow.
- Knowledge domain: captures, sources, ideas, summaries, reviews, and typed relationships.
- Guided Reading: full reading lifecycle, library management, active recall, retention scheduling, source grounding, spoiler protection, explainable recommendations.
- Planning & Projects: goals, projects, tasks, weekly review, and schedule planning.
- Finance: accounts, transactions, budgets, and monthly review.
- Health: habits, log entries, medical notes, and weekly health review.
- Career: evidence, job targets, tailored resumes, and interview preparation.
- Music / DJ Workflows: collection management, DJ set building, record labels, and Spotify export.
- Downstream Bootstrap & Updates: create a personalized OS from Ethan OS and adopt upstream improvements safely while preserving local customizations, license, and attribution.

### Make it yours

You can create your own downstream OS from this release. See [Create your own OS](getting-started/create-your-own-os.md).

### Project status

See [ROADMAP.md](ROADMAP.md) for current capability statuses and next steps.

### Known limitations

- Several capabilities are in Beta and need broader real-world usage to refine prompts and edge cases.
- Notion live sync is defined and designed but not yet fully validated end-to-end.
- External integrations such as Spotify require manual environment setup and tokens.
- Schedule planning works without an external calendar; calendar integration is future work.
- Some optional features (vector search, Gmail capture, app/UI, voice) remain on the roadmap.

### Upgrade / lineage

Downstream OS instances bootstrapped from this release should record:

```yaml
upstream:
  project: Ethan OS
  installed_version: 0.1.0-beta
  installed_commit: <this release commit>
```

See `.os-upstream.yaml` and [Updating your OS](getting-started/updating-your-os.md).
