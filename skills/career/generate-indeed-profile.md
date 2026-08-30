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

## Outputs

### Professional Summary / Profile

Requirements:

- Target <= 500 characters unless current platform rules differ.
- Emphasize role identity, experience, strongest capabilities, and measurable scope.
- Optimize for rapid recruiter scanning.
- Avoid first-person narrative unless platform style favors it.
- Lead with the most important identity and value proposition.

Apply `skills/career/compress-to-platform-limit.md` to enforce the 500-character target.

### Experience

For each relevant role:

- Concise role summary (1–2 sentences)
- 3–5 high-value bullets
- Prioritize measurable responsibility and results
- Include terminology commonly used in job descriptions
- Embed relevant technologies naturally

Use reverse-chronological order.

### Skills

Produce a platform-ready skills list using:

- Technical skills
- Methodologies
- Business/domain skills

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

## Output

Return structured Indeed content:

```yaml
summary: "..."
experience:
  - role_id: ...
    role: "..."
    employer: "..."
    timeframe: "..."
    summary: "..."
    bullets:
      - "..."
skills:
  technical: [...]
  methodologies: [...]
  domains: [...]
  capabilities: [...]
```

Store as `career.presentation_profile.indeed` in `ethan-life/domains/career/presentation/indeed/profile.yaml`.

## Confirmation policy

- Auto-execute: generating draft Indeed content from clear evidence.
- Ask for confirmation: when summary positioning is ambiguous or when skill recommendations could overstate capability.
