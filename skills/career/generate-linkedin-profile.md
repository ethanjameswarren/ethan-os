# Skill: Generate LinkedIn Profile

## Purpose

Generate LinkedIn profile content from canonical Career Evidence.

LinkedIn is a professional discovery and narrative platform, not a duplicate of the user's resume.

## Inputs

- Career narrative and positioning
- `career.role_context` objects
- `career.work_artifact` objects
- `career.capability` objects
- Relevant technologies and business outcomes
- Current target roles, if available
- Existing LinkedIn profile content, if available

## Process

Invoke `skills/career/select-career-evidence.md` and `skills/career/validate-career-claims.md` as needed during generation.

## Outputs

### Headline

Produce:

- Primary version
- Alternate technical version
- Alternate leadership version

Requirements:

- Obey current LinkedIn headline character limit (~220 characters).
- Prioritize searchable professional concepts.
- Do not keyword-stuff.
- Communicate current professional identity rather than only job title.
- Reflect evidence-backed capabilities and seniority.

### About

Create a coherent first-person professional narrative.

Structure:

1. Current professional identity
2. Types of problems solved
3. Areas of technical depth
4. Evidence of scope / impact
5. Direction of career progression

Do not turn the About section into a bullet-for-bullet resume. Keep it conversational and discovery-oriented.

Apply `skills/career/compress-to-platform-limit.md` for the About section length (~2,600 characters maximum; prefer shorter and scannable).

### Experience

For each relevant role:

- 1–3 sentence role-level summary
- 3–6 selected accomplishment bullets
- Relevant technologies embedded naturally
- Evidence selected according to the user's desired positioning

Respect LinkedIn platform limits (~2,000 characters per experience description).

Do not repeat the same accomplishment across About, Experience, and Projects without a reason.

### Projects

Select work artifacts that stand alone as meaningful technical or analytical projects.

A project should:

- Demonstrate a distinct capability
- Have meaningful technical/business context
- Strengthen the user's target professional identity

Do not create a project entry for every piece of work.

For each project:

- Project title
- Associated role/employer
- Concise description (1–3 sentences or bullets)
- Technologies used
- Link to public artifact, if available and appropriate

### Skills

Recommend skills supported by Career Evidence.

Distinguish:

- Capabilities
- Technologies
- Methodologies
- Domains

Never recommend unsupported skills. Do not list every technology mentioned in evidence; prioritize those that reinforce the headline/About narrative.

### Optional: Featured section recommendations

If applicable, recommend items to feature (e.g., GitHub repos, public articles, project summaries, certifications) with brief rationale.

## Rules

- All claims trace to Career Evidence.
- Avoid duplicating exact resume phrasing unless the resume phrasing is also the clearest LinkedIn phrasing.
- Use LinkedIn-appropriate tone: confident, narrative, and discoverable.
- Do not invent metrics, titles, or responsibilities.
- Surface evidence gaps rather than filling them with generic language.

## Output

Return structured LinkedIn content:

```yaml
headline:
  primary: "..."
  technical: "..."
  leadership: "..."
about: "..."
experience:
  - role_id: ...
    role: "..."
    employer: "..."
    timeframe: "..."
    summary: "..."
    bullets:
      - "..."
projects:
  - title: "..."
    employer: "..."
    description: "..."
    technologies: [...]
skills:
  capabilities: [...]
  technologies: [...]
  methodologies: [...]
  domains: [...]
featured_recommendations: [...]
```

Store as `career.presentation_profile.linkedin` in `ethan-life/domains/career/presentation/linkedin/profile.yaml`.

## Confirmation policy

- Auto-execute: generating draft LinkedIn content from clear evidence.
- Ask for confirmation: when positioning is ambiguous, when a headline claim relies on inference, or when a project selection could overstate ownership/scope.
