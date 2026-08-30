# Skill: select-career-evidence

## Purpose

Choose the best career evidence to support a given platform, target role, or professional positioning.

This is the shared selection engine for LinkedIn, Indeed, resumes, and cover letters. Different outputs use the same evidence pool but prioritize differently.

## Inputs

- Active `career.goal` object
- Target platform (`linkedin`, `indeed`, `resume`, `cover-letter`)
- Desired positioning or target role summary
- Career evidence graph:
  - `career.role_context` objects
  - `career.work_artifact` objects
  - `career.capability` objects
  - Existing `career.presentation_profile`, if any
- Optional constraints (section count, bullet count, character limits)

## Selection criteria

Rank candidate evidence by:

1. **Alignment to active career goal** — does this artifact move the user toward the desired strategic direction?
2. **Relevance to positioning** — does this artifact directly demonstrate the target identity?
3. **Evidence strength** — how strong and direct is the evidence? (`0`–`5`)
4. **Business impact** — measurable outcomes, decisions enabled, scale
5. **Technical depth** — architectural ownership, complexity, cross-system work
6. **Recency** — more recent for current identity, but older evidence can support foundational depth
7. **Differentiation** — what makes this candidate stand out for the target?
8. **Complementarity** — does this add a new dimension rather than repeat an existing one?

## Platform-specific priorities

### LinkedIn

- Favor breadth, progression, and narrative cohesion across roles.
- Include projects that showcase public-facing or high-signal technical identity.
- Select experience entries that support About-section themes.

### Indeed

- Favor recruiter-scanning density: clear role identity, measurable scope, strong keywords.
- Prioritize recent roles and quantified outcomes.
- Keep narrative minimal; make accomplishments scannable.

### Resume

- Strictly align with the target job description.
- Select only evidence that matches required/important capabilities.
- Avoid bullets that do not advance the target narrative.

### Cover letter

- Select 2–4 complementary pieces of evidence that tell a coherent story.
- Prefer evidence with clear business stakes and natural narrative arc.
- Avoid listing every relevant project.

## Output

Return a structured evidence selection containing:

- `roles`: role contexts to include, with rationale
- `artifacts`: ranked work artifacts with evidence strength and relevance notes
- `capabilities`: capabilities to emphasize, mapped to artifacts
- `excluded`: notable evidence deliberately omitted and why
- `gaps`: genuine capability gaps relative to the positioning, if any

## Rules

- Never select evidence that is not backed by a `career.work_artifact` or `career.role_context`.
- Never inflate evidence strength.
- Do not select the same artifact twice for the same output unless it genuinely serves two distinct roles.
- Surface genuine gaps; do not hide them.
- If positioning is unspecified, infer the strongest default positioning from the evidence.

## Confirmation policy

- Auto-execute: selecting evidence from clear positioning and existing career evidence.
- Ask for confirmation: when evidence selection implies a seniority or scope claim that is borderline, or when multiple equally strong options require a strategic choice.
