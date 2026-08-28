# Tailored Resume

## What you do

Give Ethan OS a target job and ask it to build the strongest truthful resume from your existing career evidence.

Example:

> **You:** "Tailor my resume for this Senior Data Engineer role."  
> *(paste the job description)*

## What Ethan OS does

1. **Understands the target role** — extracts the role title, seniority, responsibilities, required and preferred qualifications, and the underlying hiring intent.
2. **Retrieves your career evidence** — searches your stored career history for relevant roles, projects, accomplishments, technologies, leadership, and impact.
3. **Matches evidence to requirements** — classifies each match as strong, transferable, weak, genuine gap, or unknown. It does not pretend a gap is a match.
4. **Selects the best evidence** — ranks experiences by relevance, strength of impact, technical depth, recency, and differentiation. It avoids duplicate bullets.
5. **Reframes the selected evidence** — uses terminology from the job description where your actual experience supports it, without inflating titles, inventing metrics, or altering dates.
6. **Creates the resume content** — produces a `career.resume` object with a professional summary, skills, experience, and project bullets, all traceable to specific career evidence IDs.
7. **Renders output** — populates the LaTeX template and produces a PDF when the environment supports it.
8. **Surfaces the fit** — tells you the strongest matches, genuine gaps, and any claims that need your confirmation.

## Example interaction

> **You:** "Tailor my resume for this Senior Data Engineer role."  
> *(job description pasted)*  
> **OS:** "The role emphasizes streaming data pipelines, AWS, and mentoring. I found strong direct evidence for pipelines and AWS, lighter evidence for mentoring, and a genuine gap in Kafka experience. I'll frame your existing pipeline work for this role and flag the Kafka gap."  
> *(later)*  
> **OS:** "Draft resume generated. Every bullet is linked to a specific career evidence object. The strongest matches are your real-time analytics project and the migration to S3. Two bullets use mentoring evidence but stay within the actual scope of what you did."

## Core principle

**The OS tailors from evidence. It does not invent experience.**

If you do not have evidence for a requirement, the resume will either omit it or explicitly mark it as a gap, not dress up unrelated work.

## Outputs

- A `career.resume` object with canonical, evidence-backed content.
- A fit assessment with strongest matches, transferable matches, and genuine gaps.
- A `.tex` file and compiled PDF when the environment supports compilation.
- Links from every substantive claim back to specific career evidence.

## What gets saved

- **Job Target** (`career.job-target`) — the analyzed role.
- **Resume Content** (`career.resume`) — the tailored resume with provenance.
- **Career Evidence** — unchanged; it remains the source of truth.

## Safeguards

- Never fabricate metrics, titles, dates, or responsibilities.
- Never claim experience that is not in your evidence.
- Always link resume claims back to career evidence IDs.
- Flag genuine gaps and ask for confirmation on ambiguous claims.

## Technical details

- Workflow: `workflows/career/build-tailored-resume.md`
- Skills: `skills/career/analyze-job-description.md`, `skills/career/capture-career-evidence.md`
- Schemas: `schemas/domains/career/evidence.schema.yaml`, `job-target.schema.yaml`, `resume.schema.yaml`
- For the broader Career domain, see [Career](../capabilities/career.md).
