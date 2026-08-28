# Ethan OS Releases

## v0.1.1-beta

### Highlights

- **Beta Usage / Friction Tracking** — capture product friction and positive signals
  in normal conversation, keep actual entries private in `ethan-life`, and turn
  repeated patterns into structured evidence for fixes and evaluation cases.
  - New `core.friction-log` schema
  - New `skills/core/capture-friction.md` and `workflows/core/capture-friction.md`
  - New `workflows/core/review-friction-log.md`
  - New `scripts/core/friction_log.py` and `scripts/test-friction-capture.py`
  - New `docs/capabilities/beta-feedback.md`
- **Validation Matrix** — track real-world capability validation separately from
  maturity labels, with per-outcome use counts and coverage breadth.
  - New `ethan-life/domains/system/validation-matrix.yaml`
  - New `ethan-life/domains/planning/goals/goal-validate-ethan-os.md`
  - New `scripts/core/validation_matrix.py`

### Project status

See [ROADMAP.md](ROADMAP.md) for current capability statuses and next steps.

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

### Things you can do today

You can say things like:

- **Guided Reading:** "I finished pages 1–15."
- **Tailored Resume:** "Tailor my resume for this Senior Data Engineer role."
- **Monthly Financial Review:** "Review my budget for August."
- **Daily Schedule:** "Plan my day — I have dinner at 7."
- **DJ Set Building:** "Build me a 90-minute techno set."

Each of these uses your persistent personal context to produce a useful result without starting from scratch.

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
