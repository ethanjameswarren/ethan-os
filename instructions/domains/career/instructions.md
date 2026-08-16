# Career Domain Instructions

## Scope

Capture durable career evidence, analyze target roles, and build evidence-backed resumes and interview preparation.

## Object flow

```
Career Evidence → Job Target → Resume Content → LaTeX Template → PDF
                              → Interview Prep
```

## Evidence handling

- Use `skills/career/capture-career-evidence.md` to convert raw project, role, and accomplishment information into durable Career Evidence objects.
- Preserve Career Evidence in `ethan-life/domains/career/evidence/`.
- Career Evidence is the source of truth. Resume and interview outputs may select, prioritize, condense, and reframe it, but must never fabricate or exaggerate beyond it.
- Clearly separate confirmed `facts` from `inferences` and `unknowns`.

## Job target handling

- Use `skills/career/analyze-job-description.md` to convert a pasted job description into a Job Target object.
- Store Job Targets in `ethan-life/domains/career/targets/`.
- Prioritize requirements as critical / important / supporting / incidental.
- Never inflate requirements or invent qualifications.

## Resume handling

- Use `workflows/career/build-tailored-resume.md` to produce a Resume Content object and rendered LaTeX/PDF resume for a specific Job Target.
- Store Resume Content objects in `ethan-life/domains/career/resumes/`.
- Every substantive resume claim must be traceable to a Career Evidence object via `evidence_ids`.
- Content and presentation remain separate: canonical resume content lives in the object, presentation lives in `ethan-os/templates/resume.tex` and `ethan-os/templates/ethan-resume.sty`.
- Apply `ethan-life/global/design-philosophy.md` when rendering, without compromising factual correctness or ATS readability.

## Interview prep handling

- Use `skills/career/interview-prep.md` to convert a Job Target and its evidence-match result into structured, evidence-backed interview stories.
- Store Interview Prep objects in `ethan-life/domains/career/interview-prep/`.
- Every story element must be traceable to Career Evidence. Flag categories with no strong evidence as genuine gaps rather than inventing stories.

## Confidentiality

Across all Career objects, do not retain proprietary source code, SQL, credentials, internal dataset/table names, confidential business details, or restricted documents. Generalize sensitive implementation details while preserving career-relevant evidence.

## Relationships

- Use inline typed links (see `docs/architecture/relationships.md`).
- Common relations: `sourced_from` (evidence ← capture/source), `applies_to` (evidence/story → job requirement), `derived_from` (resume/interview-prep ← evidence), `related_to`, `revised_by`.

## Lifecycle

- Career Evidence: `draft` → `verified` → `generalized`.
- Job Target, Resume Content, Interview Prep: `draft` → `validated` → `confirmed`.
- Objects may move backward if new information changes confidence or accuracy.
