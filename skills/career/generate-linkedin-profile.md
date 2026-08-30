# Skill: Generate LinkedIn Profile

## Purpose

Generate LinkedIn profile content from canonical Career Evidence.

LinkedIn is a professional discovery and narrative platform, not a duplicate of the user's resume.

## Inputs

- Active `career.goal` object
- Career narrative and positioning
- `career.role_context` objects
- `career.work_artifact` objects
- `career.capability` objects
- Relevant technologies and business outcomes
- Current target roles, if available
- Existing LinkedIn profile content, if available

## Process

### 1. Load and align to the active career goal

Invoke `skills/career/align-to-career-goal.md` with the proposed LinkedIn output.

Use the goal to determine:

- Primary professional identity
- Capabilities and evidence dimensions to emphasize
- Framings to avoid
- Long-term career narrative

Do not generate a LinkedIn profile that ignores the active career goal. If the user requests a different positioning, evaluate it against the goal and note any misalignment.

### 2. Select, validate, and generate

Invoke `skills/career/select-career-evidence.md` and `skills/career/validate-career-claims.md` as needed during generation, applying the goal-aligned positioning.

## LinkedIn output contract

Generate content in the exact conceptual order the user encounters it on LinkedIn:

1. Headline
2. About
3. Experience
4. Projects
5. Skills

The primary output MUST be copy/paste-ready. Do not lead with analysis, recommendations, or alternative architectures. Put generation metadata at the bottom or in a separate file.

### Headline

Produce:

- Primary version
- Alternate technical version
- Alternate leadership version

Show the primary version first. Each headline must obey the current LinkedIn character limit (~220 characters). Report the character count.

### About

Create a concise professional thesis statement — an abstract for the rest of the profile, not a chronological retelling or list of accomplishments.

The About section should read like the thesis statement of an essay: it establishes the core claim, the domains of work, and the underlying philosophy. The Experience section and Projects section carry the specific evidence.

Target structure:

1. **Professional identity** — what you are and what you build
2. **Span of work** — the disciplines you operate across (e.g., data engineering, analytics, data science, AI)
3. **Domains / industries** — where this work happens
4. **Underlying philosophy or approach** — what distinguishes your work

Guidelines:

- Do not list specific projects, metrics, or role-by-role history in the About.
- Do not use the About as a summary of every major accomplishment.
- Avoid turning it into a bullet-for-bullet resume or cover letter.
- Keep it conversational, confident, and discovery-oriented.
- Prefer 3–5 short paragraphs over one dense block.
- Default to a general identity unless the user explicitly requests a target-role tilt.

Apply `skills/career/compress-to-platform-limit.md`. Report the character count (~2,600 characters maximum; prefer shorter and scannable).

### Experience format

Each Experience entry must contain:

1. Employer
2. Job title
3. Dates, when known
4. A concise 1–3 sentence role summary
5. 3–6 accomplishment / responsibility bullets

The role summary explains the overall scope of the position. Bullets provide specific evidence of ownership, technical work, scale, methodology, outcomes, and leadership.

Do not write generic job-description language when stronger Career Evidence exists.

Do not force all information into bullets.

Do not repeat the same accomplishment across About, Experience, and Projects without a reason.

Respect LinkedIn platform limits (~2,000 characters per experience description). Report the character count per entry.

### Projects

Select work artifacts that stand alone as meaningful technical or analytical projects. A project should demonstrate a distinct capability, have meaningful technical/business context, or strengthen the user's target professional identity.

For each project, output:

- Project title
- 2–4 sentence description ready to paste into LinkedIn's project description field
- Associated skills / technologies as a compact list

Do not create a project entry for every piece of work.

### Skills

Recommend skills supported by Career Evidence.

Distinguish:

- Capabilities
- Technologies
- Methodologies
- Domains

Output a numbered list of recommendations ready to add to LinkedIn. Never recommend unsupported skills. Do not list every technology mentioned in evidence; prioritize those that reinforce the headline/About narrative.

### Optional: Featured section recommendations

If applicable, recommend items to feature (e.g., GitHub repos, public articles, project summaries, certifications) as a brief list at the bottom.

## Rules

- All claims trace to Career Evidence.
- The About section is a thesis statement, not a summary of evidence. Do not embed specific projects, metrics, or role-by-role history there.
- Avoid duplicating exact resume phrasing unless the resume phrasing is also the clearest LinkedIn phrasing.
- Use LinkedIn-appropriate tone: confident, narrative, and discoverable.
- Do not invent metrics, titles, or responsibilities.
- Surface evidence gaps rather than filling them with generic language.

## Output format

Return a single Markdown file formatted for direct use. The body must be copy/paste-ready LinkedIn content in the order LinkedIn presents it.

Use YAML frontmatter with schema `career.presentation_profile` so the file is machine-readable, but the body should read like a finished profile, not a config object.

Example body structure:

```markdown
# LinkedIn Profile

## Headline

Senior Data & AI Systems Leader | Enterprise Forecasting, Experimentation, and Agentic AI Platforms

Character count: 103 / 220

---

## About

Data Consultant focused on building AI-enabled data platforms that bridge data engineering, analytics, data science, and enterprise operations.

I design systems that transform complex operational data into reliable, decision-ready products — spanning forecasting platforms, experimentation infrastructure, reusable analytics applications, and agentic AI workflows. My work sits across retail, manufacturing, and financial operations, where the common thread is turning ambiguous business problems into scalable technical architecture.

I care most about the connective tissue between business needs and implementation: clean data models, repeatable processes, and platforms that teams can maintain and extend long after the initial build.

Character count: 620 / 2,600

---

## Experience

### Lowe's Companies, Inc.
**Data Consultant — Store Operations AI / Computer Vision**
Jul 2026 – Present · Charlotte, NC

<1–3 sentence role summary>

- <achievement / responsibility>
- <achievement / responsibility>
- <achievement / responsibility>
- <achievement / responsibility>

Character count: X / 2,000

---

## Projects

### Store Operations AI Operating System

<2–4 sentence copy/paste project description>

Skills:
AI Agents · MCP · Context Engineering · Python · SQL · AI Governance

---

## Skills

Recommended skills to add or prioritize:

1. <skill>
2. <skill>
3. <skill>
...

---

# Generation Metadata

Selected capabilities:
- ...

Selected artifacts:
- ...

Excluded artifacts:
- ...

Character counts and validation:
- ...
```

Store the file as `ethan-life/domains/career/presentation/linkedin/profile.md`.

## Confirmation policy

- Auto-execute: generating draft LinkedIn content from clear evidence.
- Ask for confirmation: when positioning is ambiguous, when a headline claim relies on inference, or when a project selection could overstate ownership/scope.
