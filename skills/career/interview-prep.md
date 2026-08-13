# Skill: interview-prep

## Purpose

Convert Ethan's Career Evidence and a job-target match analysis into structured, evidence-backed interview stories.

This skill consumes the same evidence-match result used by `workflows/career/build-tailored-resume.md`. Instead of producing resume bullets, it produces ready-to-tell stories organized by common interview frameworks.

## Input

- Job Target object (`career.job-target`)
- Evidence-match result (strong matches, transferable matches, genuine gaps)
- Selected Career Evidence objects (`career.evidence`)

## Interview story frameworks

Produce stories in these formats where the evidence supports them:

### STAR

- **Situation**: context and stakes
- **Task**: Ethan's specific responsibility
- **Action**: what Ethan actually did
- **Result**: measurable or observable outcome

### CAR

- **Context**
- **Action**
- **Result**

### SOAR

- **Situation**
- **Obstacle**
- **Action**
- **Result**

Choose the framework that best fits the evidence. Do not force every story into STAR.

## Story categories

Generate at least one story for each category where evidence exists:

- **Technical leadership**: led technical direction, architecture, or decision-making
- **Difficult stakeholder / cross-functional collaboration**: navigated conflicting priorities or unclear ownership
- **Architecture / system design decision**: made a meaningful technical choice with tradeoffs
- **Failure / lesson**: something that did not go as planned and what Ethan learned
- **Ownership / autonomy**: took ownership of an ambiguous problem and drove it to resolution
- **Mentoring / team development**: helped others grow or scaled team capability
- **Business impact / measurable outcome**: delivered clear business or technical results
- **Complexity / scale**: operated under meaningful constraints or at significant scale
- **Conflict resolution**: resolved interpersonal or technical conflict
- **Adaptability / learning**: picked up something new under pressure

If a category has no strong evidence, flag it as a genuine gap rather than invent a story.

## Story selection rules

- Use only confirmed facts and reasonable inferences from Career Evidence.
- Prefer specific, memorable stories over generic claims.
- Match stories to the Job Target's critical and important requirements.
- Avoid telling five stories that demonstrate the same capability.
- Surface the strongest evidence first; omit weak or unsupported stories.

## Output

Create or update an Interview Prep object in `ethan-life/domains/career/interview-prep/`.

Use schema `career.interview-prep` and version `1`.

The object should contain:

- `id`: stable ID
- `schema`: `career.interview-prep`
- `schema_version`: `1`
- `title`: target role and company, e.g. "Interview Prep — Senior Data Engineer at Acme"
- `target_id`: ID of the related Job Target
- `status`: `draft` | `validated` | `confirmed`
- `stories`: array of story objects with:
  - `category`: technical_leadership | stakeholder | architecture | failure_lesson | ownership | mentoring | business_impact | complexity | conflict | adaptability
  - `framework`: star | car | soar
  - `situation`
  - `task`
  - `obstacle` (if SOAR)
  - `action`
  - `result`
  - `lessons_learned` (optional)
  - `evidence_ids`: Career Evidence IDs supporting the story
  - `target_requirements`: job requirements this story addresses
  - `confidence`: high | medium | low
- `gaps`: categories where no strong evidence exists
- `tailoring_notes`: how to adjust delivery for this specific role
- `provenance`
- `links`: typed relationships to Job Target and Career Evidence objects

## Evidence rules

- Every story element must be traceable to Career Evidence.
- Distinguish confirmed facts from reasonable inferences.
- Never invent outcomes, scope, ownership, or stakeholder reactions.
- If a result is estimated, label it as estimated and explain the basis.

## Confidentiality

Do not include proprietary source code, SQL, internal dataset names, credentials, or confidential business details in interview stories. Generalize sensitive specifics while keeping the story truthful and useful.

## Confirmation policy

- Auto-execute: drafting stories from clear, confirmed evidence.
- Ask for confirmation: when a story relies on inference, estimated impact, or could imply ownership/seniority beyond what the evidence supports.

## Relationship types

Use typed relationships where applicable:

- `sourced_from` — the evidence-match result or Job Target that produced this prep object
- `applies_to` — job requirements this story addresses
- `related_to` — other interview prep objects for similar roles

## Note

This skill is an extension point for the future Career domain. It reuses the same evidence-match result as `build-tailored-resume` to avoid duplicating Career Evidence or matching logic.
