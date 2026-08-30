# Skill: Generate Indeed Profile

## Purpose

Produce concise, recruiter-searchable Indeed profile content from Career Evidence.

Indeed favors a dense, scannable employment profile and resume summary rather than a narrative professional story.

## Inputs

- Career narrative and positioning
- `career.role_context` objects
- `career.work_artifact` objects
- `career.capability` objects
- Relevant technologies and outcomes
- Target roles, if available
- Existing Indeed profile or resume summary, if available

## Process

Invoke `skills/career/select-career-evidence.md` and `skills/career/validate-career-claims.md` as needed during generation.

## Indeed output contract

The primary output MUST be copy/paste-ready. Generate content in the order a recruiter or applicant encounters it on Indeed:

1. Professional Summary / Profile
2. Experience
3. Education
4. Skills

Do not lead with analysis, recommendations, or evidence mappings. Put generation metadata at the bottom or in a separate file.

### Professional Summary / Profile

Requirements:

- Target <= 500 characters unless current platform rules differ.
- Emphasize role identity, experience, strongest capabilities, and measurable scope.
- Optimize for rapid recruiter scanning.
- Avoid first-person narrative unless platform style favors it.
- Lead with the most important identity and value proposition.

Apply `skills/career/compress-to-platform-limit.md` and report the character count.

### Experience

For each relevant role, output:

1. Company
2. Job title
3. Dates
4. Concise role summary (1–2 sentences)
5. 3–5 high-value bullets

Prioritize measurable responsibility and results. Include terminology commonly used in job descriptions. Embed relevant technologies naturally.

Use reverse-chronological order.

### Education

Include institution, degree, field of study, and year if available.

### Skills

Produce a platform-ready skills list using:

- Technical skills
- Methodologies
- Business/domain skills
- Capabilities

Rank by:

1. Target-role relevance
2. Evidence strength
3. Recency
4. Repeated demonstration

Distinguish capabilities from technologies where the platform permits it. Do not list unsupported skills.

### Optional: Resume summary

If generating an Indeed-compatible resume summary, produce 2–4 sentences focused on identity, core strengths, and measurable impact.

## Rules

- All claims trace to Career Evidence.
- Prefer density and scannability over narrative.
- Use strong action verbs and measurable outcomes.
- Do not list every technology; prioritize those tied to demonstrated capabilities.
- Avoid generic soft-skill claims without evidence.
- Do not invent company-specific or role-specific motivations.

## Output format

Return a single Markdown file formatted for direct use. The body must be copy/paste-ready Indeed content in the order Indeed presents it.

Use YAML frontmatter with schema `career.presentation_profile` so the file is machine-readable, but the body should read like a finished profile.

Example body structure:

```markdown
# Indeed Profile

## Professional Summary

<copy/paste-ready summary>

Character count: X / 500

---

## Experience

### Lowe's Companies, Inc.
**Data Consultant — Store Operations AI / Computer Vision**
Jul 2026 – Present

<1–2 sentence role summary>

- <achievement / responsibility>
- <achievement / responsibility>
- <achievement / responsibility>
- <achievement / responsibility>

---

## Education

California Polytechnic State University — B.S. Economics, 2018

---

## Skills

Technical:
Python, SQL, BigQuery, Airflow, Power BI, R, ...

Methodologies:
A/B Testing, Difference-in-Differences, Cohort Analysis, ...

Domains:
Retail Operations, Workforce Planning, Manufacturing Analytics, ...

---

# Generation Metadata

Selected capabilities:
- ...

Selected artifacts:
- ...

Character counts and validation:
- ...
```

Store the file as `ethan-life/domains/career/presentation/indeed/profile.md`.

## Confirmation policy

- Auto-execute: generating draft Indeed content from clear evidence.
- Ask for confirmation: when summary positioning is ambiguous or when skill recommendations could overstate capability.
