# Career

## What it does

Collect durable career evidence, analyze target roles, and build resumes and interview preparation that are grounded in real examples rather than invented claims.

## Why it exists

Resumes and interviews are most convincing when every claim traces back to specific evidence. Ethan OS keeps a canonical evidence base and reframes it for each target role, so you are never starting from a blank page.

## What you do

- Mention a project, achievement, skill growth, or feedback snippet.
- Define a target role.
- Ask for a tailored resume or interview prep.
- Point out missing evidence or ask for a different framing.

## What Ethan OS does

- Stores career evidence as a reusable source of truth.
- Tracks job targets with requirements and priority evidence gaps.
- Generates resume content that selects and reframes evidence for the target role.
- Produces interview prep with stories tied to specific evidence IDs.
- Reconstructs prior roles with facts, inferences, unknowns, and follow-up questions kept distinct.
- Synthesizes capability maps and aligns projects and presentation assets to an authoritative career goal.
- Generates copy/paste-ready LinkedIn, Indeed, and cover-letter assets with generation metadata.
- Keeps presentation separate from content; PDF generation uses templates.

## Key ideas

- **Evidence is the source of truth.** Every resume bullet and interview story links back to specific evidence IDs.
- **No fabrication.** The system never invents metrics, titles, or responsibilities.
- **Framing is role-specific.** The same evidence is expressed differently for different targets.
- **Unknowns are surfaced.** Missing evidence is reported, not hidden.

## Example interaction

> **You:** "I want to apply for a senior data-engineering role at a climate startup."  
> **OS:** "What requirements matter most for that role?"  
> **You:** "Streaming data pipelines, AWS, mentoring juniors, and cross-functional work."  
> **OS:** "I'll create a job target and map your evidence to those requirements. I see strong pipeline and AWS evidence; mentoring is lighter. I'll flag that gap."

## What gets saved

- **Career Evidence** — project, role, outcome, metrics, skills, and proof.
- **Job Target** — role, requirements, priority gaps, and linked evidence.
- **Resume Content** — role-specific bullets and sections derived from evidence.
- **Interview Prep** — stories with context, actions, results, and evidence links.
- **Career Goal and Presentation Profiles** — authoritative positioning plus derived platform-specific assets.
- **Role Reconstructions and Capability Maps** — reviewable evidence synthesis that preserves uncertainty.

## Important behaviors

- Never fabricate metrics or responsibilities.
- Always trace claims back to stored evidence.
- Flag gaps instead of filling them with generic language.
- Keep canonical resume content in `ethan-life`; presentation templates live in `ethan-os`.

## Related workflows

- [Tailor a resume or prepare for an interview](../workflows/career.md)

## Technical implementation

- Workflows: `workflows/career/`
- Skills: `skills/career/`
- Schemas: `schemas/domains/career/evidence.schema.yaml`, `job-target.schema.yaml`, `resume.schema.yaml`, `interview-prep.schema.yaml`
