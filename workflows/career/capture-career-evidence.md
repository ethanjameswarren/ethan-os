# Workflow: Capture Career Evidence

## Purpose

Convert raw descriptions of completed or ongoing professional work into structured, reusable career evidence.

This workflow preserves detailed evidence rather than prematurely converting work into resume bullets. Downstream outputs such as resumes, LinkedIn profiles, interview stories, promotion cases, and job-fit assessments consume this evidence later.

## Triggering phrases

- "Capture this for my career context."
- "Add this work to my resume context."
- "Learn this project for future job applications."
- "Update my career evidence from this document."
- "Capture what I've been working on lately."
- Any user-provided work artifact, role summary, project closeout, or repository context related to professional experience.

## Inputs

One or more of:

- User-described work
- Project summary
- Project closeout
- Repository context
- Existing Ethan OS / Ethan Life context
- Uploaded document
- Work notes
- Analysis results
- Existing work artifacts

## Process

### 1. Resolve context

Determine:

- Employer
- Role
- Team / domain
- Project or initiative
- Approximate timeframe
- Existing related work artifacts
- Existing role context
- Existing capability records

Use available context before asking the user for information. Do not ask for information merely because it is absent from the current input if it can be reliably resolved from existing career context.

### 2. Extract work artifact

Invoke `skills/career/extract-work-artifact.md`.

Capture:

- Context
- Problem
- User's role
- Actions
- Architecture / methodology
- Technologies
- Scope
- Results
- Business impact
- Decisions enabled
- Reusable outputs
- Evidence signals

Do not optimize language for a resume. Preserve technical detail and evidence. Never invent metrics.

### 3. Update role context

Invoke `skills/career/synthesize-role-context.md`.

Determine whether the new evidence:

- Introduces a responsibility
- Strengthens an existing responsibility
- Establishes a new technical area
- Changes the apparent seniority / scope of the role
- Demonstrates cross-functional ownership
- Changes how the role should be positioned

Update the canonical role context only when warranted. Role context should summarize recurring patterns across projects rather than duplicate individual project details.

### 4. Identify capabilities

Invoke `skills/career/synthesize-capabilities.md`.

Map the work artifact to demonstrated capabilities. Examples:

- Experimentation & Causal Measurement
- Analytics Engineering
- AI Platforms & Agentic Systems
- Data Infrastructure
- Forecasting
- BI Architecture
- Operational Analytics
- Technical Architecture
- Data Quality
- Financial Analytics
- Manufacturing Analytics
- Developer Enablement
- Technical Leadership

Prefer existing capability records when they represent the demonstrated capability. Create a new capability only when the evidence represents a materially distinct reusable competency.

### 5. Link evidence

Invoke `skills/career/link-career-evidence.md`.

Maintain relationships:

```
Role → Work Artifact
Work Artifact → Capabilities
Capability → Evidence / Work Artifacts
Work Artifact → Technologies
Work Artifact → Business Outcomes
```

Do not duplicate the complete artifact inside capability or role records. Use references.

### 6. Reconcile existing context

Invoke `skills/career/reconcile-career-context.md`.

Determine whether newly captured evidence contradicts, supersedes, expands, or duplicates existing evidence.

- Merge duplicates.
- Preserve historically meaningful distinctions.
- Do not silently replace stronger evidence with weaker summaries.

### 7. Report changes

Tell the user concisely:

- Work artifacts created / updated
- Role context changed
- Capabilities added / strengthened
- Important links established
- Unresolved evidence gaps, if relevant

Do not generate a resume unless explicitly requested.

## Outputs

- `career.work_artifact` object(s) in `ethan-life/domains/career/evidence/`
- Updated `career.role_context` object in `ethan-life/domains/career/roles/`
- Updated or new `career.capability` objects in `ethan-life/domains/career/capabilities/`
- Typed links between role, artifacts, capabilities, technologies, and outcomes

## Governing principle

Career evidence is the durable source of truth. Resume content and interview stories are derived from it, not the other way around.

## Confirmation policy

- Auto-execute: creating draft evidence, role context, and capability objects from clearly provided information.
- Ask for confirmation: changing role titles, marking evidence as verified, altering dates that affect other records, or when evidence appears to contradict existing canonical state.
