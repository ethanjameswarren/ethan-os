# Workflow: build-tailored-resume

## Goal

Given a job description, build the strongest truthful resume possible from Ethan's existing Career Evidence.

The workflow selects and frames existing evidence. It does not rewrite Ethan's history to match the job.

## Required inputs

- job description text or capture ID of an analyzed job description
- active `career.goal` object from `ethan-life/domains/career/goals/`
- access to `ethan-life/domains/career/evidence/`
- access to `ethan-life/domains/career/targets/` (optional, for previously analyzed roles)
- access to `ethan-life/global/design-philosophy.md` (loaded for artifact generation)

## Produced artifacts

- Career Resume Content object (`career.resume`) in `ethan-life/domains/career/resumes/`
- Rendered `.tex` file from `ethan-os/templates/resume.tex`
- Compiled PDF if the environment supports LaTeX compilation
- Match analysis retained in the resume object

## Steps

### 1. Load the active career goal

Read the active `career.goal` object from `ethan-life/domains/career/goals/`.

If no active goal exists, ask the user to confirm or create one before tailoring the resume. The career goal guides which evidence to emphasize and how to frame experience toward the user's desired strategic direction.

### 2. Analyze the target role

Run `skills/career/analyze-job-description.md`.

Create or load a Job Target object (`career.job-target`) in `ethan-life/domains/career/targets/`.

Evaluate the job target against the active career goal. If the role does not meaningfully advance the goal, note this to the user and ask whether to proceed, pivot the framing, or capture the role as a non-target learning opportunity.

### 3. Retrieve relevant context

Build a `core.context-request` with intent `tailored-resume`, domains `[career, planning, knowledge]`, and `avoid_domains: [health, finance, music]`.

Run `scripts/core/context_assembly.py` to produce a `core.context-bundle` containing:

- the active `career.job-target`
- relevant `career.evidence` (roles, projects, accomplishments, technologies, leadership, impact)
- relevant `planning.project` and `planning.task` that support the target
- relevant `knowledge.idea` and `knowledge.learning-program` that substantiate skills

Then search `ethan-life/domains/career/evidence/` if the bundle needs expansion.

### 4. Cross-domain reasoning

Run `skills/core/cross-domain-reasoning.md` with modes:

- `connection` — which projects support the job target
- `transfer_opportunity` — which learning could be framed as skill evidence
- `evidence_gap` — where a claimed capability lacks supporting evidence

Use the findings to guide which evidence to select and which gaps to surface honestly.

### 5. Match evidence to requirements

For each important job requirement, classify Ethan's evidence as:

- **strong direct match**
- **credible adjacent / transferable match**
- **weak match**
- **genuine gap**
- **unknown**

Provide provenance back to the underlying Career Evidence objects.

Never manufacture a match.

### 6. Rank available evidence

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

### 7. Determine resume strategy

Before writing, determine the narrative the resume should communicate. Examples:

- AI systems technical leader
- analytics / platform builder
- forecasting specialist
- data-product engineer
- cross-functional technical owner

Choose the narrative supported by both the target role and Ethan's actual evidence.

Do not fabricate a persona the evidence does not support.

### 8. Select experience

Select:

- most relevant roles
- most relevant projects
- strongest accomplishments
- appropriate technologies
- appropriate leadership evidence

Less relevant information may be shortened or omitted.

Do not alter employer, title, dates, education, or other factual records unless the canonical Career Evidence itself is corrected (use `revise` workflow).

### 9. Craft resume bullets

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

### 10. Perform evidence validation

Every substantive resume claim must be traceable to Career Evidence.

Flag any generated sentence containing a claim not adequately supported by the evidence.

Remove or revise unsupported claims before final generation.

### 11. Produce match analysis

Internally retain:

- strongest matches
- transferable matches
- genuine gaps
- evidence used
- evidence omitted
- rationale for major resume-selection decisions

Do not distort the resume to hide genuine gaps.

### 12. Apply Personal Design Philosophy

Before finalizing content, consult `ethan-life/global/design-philosophy.md`.

Interpret the global design philosophy for the LaTeX/PDF medium:

- restrained typography
- strong alignment
- generous but efficient whitespace
- clear hierarchy
- minimal decoration
- premium but honest tone

Apply these constraints without violating:

- factual correctness
- ATS readability
- canonical career data
- standard resume conventions

### 13. Generate canonical resume content

Generate the selected content:

- professional summary (if useful)
- skills
- experience
- project / accomplishment bullets
- education
- other approved sections

Keep the resume appropriately concise for the target level.

Store as a Career Resume Content object with schema `career.resume`.

### 14. Render using LaTeX

Populate `ethan-os/templates/resume.tex` with the canonical resume content.

Content and presentation must remain separate:

```
Career Evidence → Resume Content → LaTeX Template → PDF
```

Do not embed career facts directly into template logic.

Presentation decisions are centralized in `ethan-os/templates/ethan-resume.sty`. The template (`resume.tex`) only defines content macros:

- `\name{}`
- `\contacts{}`
- `\summary{}`
- `\skills{}`
- `\experience{}`
- `\projects{}`
- `\education{}`

Use `\resumeentry{role}{employer}{dates}{location}` for roles, projects, and education entries. The fourth argument is optional.

The LaTeX template reflects the Personal Design Philosophy loaded earlier (restrained typography, clear hierarchy, efficient whitespace, minimal decoration). See `ethan-os/templates/README.md` for template architecture and ATS-related compromises.

### 15. Validate final output

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
