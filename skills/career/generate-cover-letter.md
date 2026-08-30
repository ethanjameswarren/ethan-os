# Skill: Generate Cover Letter

## Purpose

Generate a targeted cover letter by matching a specific job opportunity against Career Evidence.

## Inputs

- Job description text or analyzed `career.job-target`
- Target company
- Target role
- Career narrative and positioning
- Relevant `career.role_context`, `career.work_artifact`, and `career.capability` objects
- Existing resume version, if available
- Any constraints (word count, tone, required sections)

## Process

1. **Extract the role's needs**

   Identify the 3–5 most important needs from the job description: required capabilities, technical areas, leadership expectations, and business problems.

2. **Select evidence**

   Invoke `skills/career/select-career-evidence.md` for `cover-letter` platform. Retrieve 2–4 complementary work artifacts and capabilities that directly address the role's needs.

3. **Validate claims**

   Invoke `skills/career/validate-career-claims.md` to ensure selected evidence genuinely supports every intended claim.

4. **Build narrative**

   Construct a concise narrative explaining why the evidence matters to this role. Each paragraph should connect a demonstrated capability to a specific need.

5. **Add motivation**

   Include a concise statement of interest in the specific opportunity only when supported by available context. Do not invent company-specific enthusiasm or pretend knowledge of internal initiatives.

6. **Compress and validate**

   Invoke `skills/career/compress-to-platform-limit.md` to target 250–400 words unless the application specifies otherwise.

## Default structure

### Paragraph 1

Why this role + concise professional positioning.

### Paragraph 2

Strongest technical/business evidence relevant to the role.

### Paragraph 3

Second complementary capability or leadership example.

### Paragraph 4

Concise closing connecting prior evidence to what the candidate could contribute.

## Rules

- Do not summarize the resume line by line.
- Do not use generic enthusiasm filler.
- Do not invent company-specific motivations or pretend knowledge of internal initiatives.
- Prefer 250–400 words unless application requirements specify otherwise.
- Every material accomplishment must be traceable to Career Evidence.
- Use job-description terminology only where the underlying evidence supports it.
- Keep the letter focused on 2–4 pieces of evidence rather than listing every relevant project.

## Output format

The primary output is the finished cover letter text, formatted for direct use. It appears first in the file, not after analysis.

After the letter, include a `# Generation Metadata` section with:

- Target role/company
- Word count
- Evidence IDs used
- Any claims requiring user confirmation or gaps relative to the job description

Example structure:

```markdown
Dear Hiring Manager,

<finished cover letter paragraphs>

Sincerely,
Ethan Warren

---

# Generation Metadata

Target role: ...
Target company: ...
Word count: ...
Evidence IDs used:
- ...
Claims requiring confirmation:
- ...
Gaps relative to job description:
- ...
```

Store as a cover-letter-specific object in `ethan-life/domains/career/presentation/cover-letter/<company>-<role>-<date>.md` or a similarly stable naming scheme.

## Confirmation policy

- Auto-execute: generating draft cover letter from clear evidence and a specific job description.
- Ask for confirmation: when the role's needs are ambiguous, when a claim relies on inference, or when a capability gap exists that the user may want to address differently.
