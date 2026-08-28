# Workflow: Tailor a Resume

## What you do

Tell Ethan OS about a role you want to apply for and ask for a tailored resume.

Example:

> **You:** "I want to apply for a senior data-engineering role at a climate startup. They care about streaming pipelines, AWS, mentoring, and cross-functional work."

## What Ethan OS does

1. Loads your career evidence and job targets.
2. Matches the role's requirements against your evidence.
3. Identifies strong fits, weak fits, and gaps.
4. Reframes selected evidence into role-specific resume bullets.
5. Produces a resume content object that links every bullet to specific evidence IDs.

## Conceptual stages

- **Define** — capture the target role and its key requirements.
- **Map** — match requirements to stored career evidence.
- **Flag gaps** — surface requirements with little or no evidence.
- **Reframe** — express selected evidence in terms the role values.
- **Output** — produce resume content with provenance links.

## Outputs

- A Job Target object with requirements and evidence mapping.
- A Resume Content object with role-specific sections and bullets.
- A gap list for you to address.

## Safeguards

- Every claim links back to stored evidence.
- No metrics, titles, or responsibilities are fabricated.
- Gaps are surfaced, not filled with generic language.
- Presentation templates stay separate from canonical content.

## Technical details

- Workflows: `workflows/career/tailor-resume.md`
- Skills: `skills/career/map-evidence-to-target.md`, `skills/career/reframe-evidence.md`
- Schemas: `schemas/domains/career/evidence.schema.yaml`, `job-target.schema.yaml`, `resume.schema.yaml`
