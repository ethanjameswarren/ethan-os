# Workflow: Build Career Profile

## Purpose

Generate platform-specific career presentation content from canonical Career Evidence.

LinkedIn, Indeed, resumes, and cover letters are distinct outputs with different constraints, audiences, and tones. This workflow produces each from the same evidence graph without duplicating content or wording across platforms.

## Triggering phrases

- "Build my LinkedIn profile."
- "Update my Indeed profile."
- "Generate my LinkedIn About section."
- "Create a cover letter for this role."
- "Build career profiles from my evidence."
- "Generate platform-specific career content."

## Inputs

- Career evidence graph (`career.role_context`, `career.work_artifact`, `career.capability`)
- Target platform(s): `linkedin`, `indeed`, `resume`, `cover-letter`
- Desired positioning (optional)
- Existing presentation profile, if any
- For cover letters: job description and target company/role

## Process

### 1. Determine positioning

If the user specifies a target role or direction, use it. Otherwise infer a default positioning from the strongest evidence.

Positioning includes:

- Primary professional identity (e.g., AI platform engineer, analytics architect, experimentation lead)
- Secondary dimensions to emphasize (e.g., technical architecture, cross-functional leadership, forecasting)
- Target seniority level

### 2. Select evidence

Invoke `skills/career/select-career-evidence.md`.

Retrieve the strongest work artifacts, capabilities, role contexts, and outcomes for the requested platform and positioning.

### 3. Validate claims

Invoke `skills/career/validate-career-claims.md`.

Ensure every claim traces back to career evidence. Flag unsupported inferences, invented metrics, or ambiguous scope.

### 4. Generate platform content

Invoke the appropriate generator skill(s):

- `skills/career/generate-linkedin-profile.md`
- `skills/career/generate-indeed-profile.md`
- `skills/career/generate-cover-letter.md`

Resume generation uses the existing `workflows/career/build-tailored-resume.md` workflow.

### 5. Apply platform constraints

Invoke `skills/career/compress-to-platform-limit.md`.

Check and enforce character limits, section lengths, and formatting rules for the target platform.

### 6. Assemble presentation profile

Produce or update a `career.presentation_profile` object containing platform-specific sections. Detect drift from prior versions and surface significant changes.

### 7. Report

Tell the user:

- Which platforms were generated
- Key content highlights
- Any unsupported or compressed claims
- Where files were saved
- Recommended next steps (e.g., review LinkedIn About, tailor for a specific role)

## Outputs

- `career.presentation_profile` object in `ethan-life/domains/career/presentation/profile.yaml`
- `linkedin/` content: headline, about, experience, projects, skills recommendations
- `indeed/` content: summary, experience, skills
- `cover-letter/` content: generated cover letter for a specific target, if requested
- Resume content remains in `ethan-life/domains/career/resumes/` via the tailored-resume workflow

## Governing principle

Platform-specific wording is derived from evidence, not copied from another platform. LinkedIn gets narrative and progression; Indeed gets recruiter-scanning density; resumes get tight job-target alignment; cover letters get selective storytelling.

## Default output principle

Career Presentation outputs are intended for direct use on external platforms.

The default artifact MUST therefore be copy/paste-ready.

Do not primarily output:

- recommendations,
- outlines,
- evidence mappings,
- writing guidance,
- alternative content architecture,
- explanations of what the user could write.

Instead, produce the final text that belongs in each platform field.

Analysis and generation metadata are secondary outputs, stored separately or appended under a clear `# Generation Metadata` section. They should not interrupt the copy/paste-ready content.

Minor user edits should be optional rather than required.

## Confirmation policy

- Auto-execute: generating draft profile content from clear evidence and platform rules.
- Ask for confirmation: when positioning is ambiguous, a claim relies on inference, content exceeds platform limits and requires trade-offs, or before marking a profile as final.
