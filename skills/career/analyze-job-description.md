# Skill: analyze-job-description

## Purpose

Convert a pasted job description into a structured target-role profile that downstream Career workflows can use.

This skill produces evidence, not a resume. It extracts and prioritizes what the company is actually hiring for, so that future resume or interview workflows can match Ethan's genuine experience against the role.

## Input

A full job description pasted by the user.

Accept pasted text in any format: plain text, Markdown, copied bullets, or partially formatted job postings.

## Extract and normalize

Identify, where present:

- company
- role title
- apparent seniority
- primary responsibilities
- required qualifications
- preferred qualifications
- technical skills
- platforms / tools
- domain knowledge
- leadership expectations
- architecture / system-design expectations
- communication / stakeholder expectations
- years-of-experience requirements
- education / certification requirements
- business capabilities
- repeated themes
- unusually important requirements

## Prioritize

Classify each requirement into one of:

### Critical

Likely fundamental to candidacy. Missing this makes passing unlikely.

### Important

Strongly valuable but not necessarily absolute.

### Supporting

Useful differentiators or secondary requirements.

### Incidental

Mentioned but unlikely to drive the hiring decision.

Prioritization must consider the apparent responsibility and emphasis of the role, not keyword frequency alone.

## Infer hiring intent

Produce a concise explanation of:

> What problem is this company actually hiring this person to solve?

Also identify the likely candidate archetype they appear to want.

## Matching vocabulary

Identify terminology from the job description that may appropriately be reflected in a resume **when the underlying experience supports it**.

Never recommend keyword insertion unsupported by Ethan's evidence.

## Output

Create or update a Job Target object in `ethan-life/domains/career/targets/`.

Use schema `career.job-target` and version `1`.

The object should contain:

- `id`: stable ID
- `schema`: `career.job-target`
- `schema_version`: `1`
- `title`: role title and company
- `company`
- `role_title`
- `seniority`
- `hiring_intent`: what problem the company is hiring this person to solve
- `candidate_archetype`: likely ideal candidate profile
- `responsibilities`: list of primary responsibilities
- `requirements`: list of structured requirements with fields:
  - `text`
  - `category`: technical | leadership | communication | domain | education | experience | business
  - `priority`: critical | important | supporting | incidental
  - `notes`: why this priority was assigned
- `themes`: repeated or emphasized themes
- `vocabulary`: terminology that could be reflected in matched evidence
- `evaluation_criteria`: criteria for matching Career Evidence against this target
- `provenance`: capture ID, source, and agent information
- `links`: typed relationships to related Career Evidence or other Job Targets

## Evidence rules

- Record what the job description actually says.
- Clearly distinguish direct requirement from reasonable inference.
- Do not inflate requirements or invent qualifications.
- Do not assume Ethan has or lacks any requirement.

## Confidentiality

Job descriptions are generally public, but remove or generalize any sensitive details such as:

- confidential project names
- unreleased product details
- internal team names
- salary bands if marked confidential
- recruiter-only notes

## Confirmation policy

- Auto-execute: creating a draft Job Target from a pasted job description.
- Ask for confirmation: when the role is ambiguous, seniority is unclear, or prioritization depends on an interpretation that could materially change matching strategy.

## Relationship types

Use typed relationships where applicable:

- `sourced_from` — the capture containing the pasted job description
- `related_to` — similar roles or related career evidence
- `applies_to` — target role that a piece of evidence may support

## Note

This skill is an extension point for the future Career domain. It does not write a resume or modify knowledge-domain objects.
