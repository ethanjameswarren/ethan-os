# Workflow: build-tailored-resume

## Goal

Given a job description, build the strongest truthful resume possible from Ethan's existing Career Evidence.

The workflow selects and frames existing evidence. It does not rewrite Ethan's history to match the job.

## Required inputs

- job description text or capture ID of an analyzed job description
- access to `ethan-life/domains/career/evidence/`
- access to `ethan-life/domains/career/targets/` (optional, for previously analyzed roles)

## Produced artifacts

- Career Resume Content object (`career.resume`) in `ethan-life/domains/career/resumes/`
- Rendered `.tex` file from `ethan-os/templates/resume.tex`
- Compiled PDF if the environment supports LaTeX compilation
- Match analysis retained in the resume object

## Steps

### 1. Analyze the target role

Run `skills/career/analyze-job-description.md`.

Create or load a Job Target object (`career.job-target`) in `ethan-life/domains/career/targets/`.

### 2. Retrieve relevant career evidence

Search `ethan-life/domains/career/evidence/` across:

- roles
- projects
- accomplishments
- technologies
- leadership evidence
- impact
- architecture experience
- domain experience
- skills

Retrieve based on semantic relevance to the Job Target, not just keyword matching.

### 3. Match evidence to requirements

For each important job requirement, classify Ethan's evidence as:

- **strong direct match**
- **credible adjacent / transferable match**
- **weak match**
- **genuine gap**
- **unknown**

Provide provenance back to the underlying Career Evidence objects.

Never manufacture a match.

### 4. Rank available evidence

Score candidate experiences based on:

- relevance to the role
- strength of evidence
- business impact
- technical depth
- leadership / ownership
- recency where relevant
- differentiation
- level / scope appropriate to the target role

Avoid selecting multiple bullets that demonstrate essentially the same capability.

### 5. Determine resume strategy

Before writing, determine the narrative the resume should communicate. Examples:

- AI systems technical leader
- analytics / platform builder
- forecasting specialist
- data-product engineer
- cross-functional technical owner

Choose the narrative supported by both the target role and Ethan's actual evidence.

Do not fabricate a persona the evidence does not support.

### 6. Select experience

Select:

- most relevant roles
- most relevant projects
- strongest accomplishments
- appropriate technologies
- appropriate leadership evidence

Less relevant information may be shortened or omitted.

Do not alter employer, title, dates, education, or other factual records unless the canonical Career Evidence itself is corrected (use `revise` workflow).

### 7. Craft resume bullets

Generate concise accomplishment-oriented bullets.

Prefer format:

> action + problem/technical contribution + scope + outcome

where the evidence supports each component.

Use terminology from the job description naturally when Ethan's evidence genuinely supports it.

Avoid:

- keyword stuffing
- vague buzzwords
- invented metrics
- inflated ownership
- unsupported seniority
- repetitive bullets

### 8. Perform evidence validation

Every substantive resume claim must be traceable to Career Evidence.

Flag any generated sentence containing a claim not adequately supported by the evidence.

Remove or revise unsupported claims before final generation.

### 9. Produce match analysis

Internally retain:

- strongest matches
- transferable matches
- genuine gaps
- evidence used
- evidence omitted
- rationale for major resume-selection decisions

Do not distort the resume to hide genuine gaps.

### 10. Generate canonical resume content

Generate the selected content:

- professional summary (if useful)
- skills
- experience
- project / accomplishment bullets
- education
- other approved sections

Keep the resume appropriately concise for the target level.

Store as a Career Resume Content object with schema `career.resume`.

### 11. Render using LaTeX

Populate `ethan-os/templates/resume.tex` with the canonical resume content.

Content and presentation must remain separate:

```
Career Evidence → Resume Content → LaTeX Template → PDF
```

Do not embed career facts directly into template logic.

The LaTeX template controls formatting, spacing, typography, and section layout.

### 12. Validate final output

Check:

- every claim is evidence-backed
- dates / titles / employers remain canonical
- no important requirement was falsely represented
- no obvious duplicate bullets
- no unsupported technologies
- no invented metrics
- target terminology is used only where appropriate
- resume remains readable and concise
- LaTeX compiles successfully (if environment supports it)

## User-facing output

Return:

1. tailored resume (Markdown and rendered PDF when possible)
2. concise fit assessment
3. strongest evidence used
4. genuine gaps worth knowing about
5. any claims that require Ethan's confirmation
6. generated `.tex` file path
7. compiled PDF path when the environment supports compilation

## Governing principle

The workflow may:

- select
- prioritize
- condense
- reframe
- tailor wording

It may **not**:

- fabricate
- exaggerate
- silently modify canonical career history

The Career Evidence repository is the source of truth.

## Confirmation policy

- Auto-execute: generating draft resume content and candidate bullets from clear evidence.
- Ask for confirmation: when a claim relies on inference rather than confirmed fact, when seniority/ownership scope is ambiguous, when a generated bullet changes the implied scope of Ethan's role, or before marking the resume as final.
