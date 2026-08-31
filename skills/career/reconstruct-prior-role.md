# Skill: Reconstruct Prior Role

## Purpose

Reconstruct sparse or missing career evidence for a prior role so it can be truthfully positioned toward the active career goal. This skill is used when a role is under-documented relative to its tenure or importance, and before finalizing resumes, LinkedIn/Indeed profiles, or case-study libraries.

Reconstruction does not mean rewriting history or inflating scope. It means extracting, structuring, and validating the strongest evidence from what the user actually did.

## Triggering phrases

- "Reconstruct my prior role."
- "I need to capture missing context from my previous job."
- "My earlier role needs deeper evidence."
- "Fill in the gaps for my [employer/role] experience."
- "Build a capture mechanism for a past role."

## Inputs

- Employer and role title
- Approximate timeframe
- Active `career.goal` object
- Existing related `career.evidence` / `career.work_artifact` records, if any
- Existing `career.role_context` for the role, if any
- User's memory, notes, documents, code repositories, Jira/Confluence history, emails, presentations, or performance reviews

## Process

### 1. Audit the role's current evidence

- List existing work artifacts and role context for the role.
- Identify evidence density relative to tenure.
- Flag which strategic dimensions (architecture, scale, stakeholders, outcomes, leadership) are under-supported.

### 2. Define missing-context dimensions

Use the standard reconstruction dimensions:

1. **Problem** — what business or operational pain existed
2. **Business context** — where the work fit in the organization and planning cycles
3. **Scale** — stores, departments, users, data volume, frequency, regions
4. **Stakeholders** — who consumed, reviewed, or depended on the work
5. **My ownership** — individual contributor, lead, sole owner, co-owner
6. **Architecture** — design decisions, alternatives, trade-offs
7. **Technologies** — stack, platforms, tools, source systems
8. **Complexity** — what made this hard or non-obvious
9. **Decisions I made** — technical, prioritization, standards, process
10. **Measurable results** — quantified outcomes, performance, adoption
11. **Organizational impact** — behavior change, follow-on work, credibility
12. **Reusable systems created** — frameworks, libraries, documentation, standards
13. **Leadership / strategy demonstrated** — influence, mentoring, cross-functional alignment, executive communication

### 3. Build the capture questionnaire

Create or reuse a role-specific questionnaire object (e.g., `questionnaire-prior-<role>.md`) in `ethan-life/domains/career/reconstruction/`. The questionnaire should:

- Ask open-ended prompts for each dimension.
- Explicitly invite "unknown" answers.
- Avoid leading the user toward inflated claims.
- Group related questions into candidate project themes.

### 4. Create a reconstruction plan

Create or update a reconstruction plan object (e.g., `<role>-reconstruction-plan.md`) that defines:

- Objective
- Target number of additional work artifacts
- Candidate project/system themes to explore
- Step-by-step capture workflow
- Stop conditions and anti-fabrication rules
- Success criteria

### 5. Conduct capture sessions

For each theme or project the user can recall:

- Run `workflows/career/capture-career-evidence.md`.
- Invoke `skills/career/extract-work-artifact.md` to create/update a `career.work_artifact`.
- Distinguish confirmed facts, reasonable inferences, and unknowns.
- Do not invent metrics, ownership, titles, technologies, or outcomes.

### 6. Update role context

Invoke `skills/career/synthesize-role-context.md` to update the canonical `career.role_context` for the role. Reflect:

- New responsibilities
- Stronger scope or seniority signals
- Additional stakeholder exposure
- Additional technical domains
- Updated positioning guidance

### 7. Validate and reconcile

- Run `skills/career/validate-career-claims.md`.
- Run `skills/career/reconcile-career-context.md` to resolve contradictions or duplicates.
- Ensure the role context does not overstate seniority, title, or scope.

### 8. Regenerate downstream outputs

Once the role context is richer, regenerate:

- Master resume and targeted resume variants
- LinkedIn Experience section
- Indeed Experience section
- Case-study library entries
- Interview story bank
- Skills/capability map

## Output

- Role-specific reconstruction plan in `ethan-life/domains/career/reconstruction/`
- Role-specific questionnaire in `ethan-life/domains/career/reconstruction/`
- Updated or new `career.role_context` object in `ethan-life/domains/career/roles/`
- Additional `career.work_artifact` objects in `ethan-life/domains/career/evidence/`
- Updated `career.capability` objects as needed
- Gap list for dimensions that remain unknown

## Rules

- **Never fabricate experience or inflate titles.** Reconstruction is evidence extraction, not history rewriting.
- **Mark unknowns explicitly.** "I don't remember" is a valid answer and should be recorded.
- **Prefer verifiable signals.** Code commits, Jira tickets, Confluence pages, emails, presentations, and performance reviews are stronger than memory alone.
- **Distinguish fact from inference.** A reasonable inference is not a confirmed accomplishment.
- **Stop when evidence is exhausted.** Do not produce filler content to hit an artifact count.
- **Align to the active career goal.** Use the goal to determine which dimensions to emphasize, but do not force evidence to fit.
- **Update links.** Tie new work artifacts to the role context, capabilities, and downstream outputs.

## Confirmation policy

- Auto-execute: creating draft reconstruction plans, questionnaires, and role contexts from sparse existing evidence.
- Ask for confirmation: when a reconstruction implies a seniority or scope claim beyond what current evidence supports, or when the user provides information that contradicts existing canonical records.
