# Skill: validate-career-claims

## Purpose

Ensure every claim in generated career presentation content can be traced back to canonical Career Evidence and is not inflated, invented, or ambiguously phrased.

## Inputs

- Draft platform content (LinkedIn, Indeed, resume, cover letter)
- Career evidence graph (`career.role_context`, `career.work_artifact`, `career.capability`)
- Target platform constraints

## Validation checks

For each substantive claim, determine:

### Direct evidence

- Is the claim supported by a specific `career.work_artifact` or `career.role_context`?
- Is the evidence level sufficient for the phrasing used?

### Metrics

- Are numbers, percentages, scale, or timeframes sourced from evidence?
- Are approximations clearly marked as approximate if not exact?

### Scope and ownership

- Does the phrasing accurately reflect whether the user led, built, designed, contributed to, or supported the work?
- Is there any implication of authority or scope beyond what the evidence supports?

### Technologies

- Is each technology or tool explicitly mentioned in evidence?
- Is the phrasing current and not speculative?

### Inferences vs. facts

- Are inferences presented as evidence or framed with appropriate uncertainty?
- Is business impact stated only where supported?

### Platform fit

- Does the claim meet the target platform's style and constraints?
- Is the claim redundant with another section on the same platform?

## Output

Return:

- `valid_claims`: list of claims with supporting evidence IDs
- `flagged_claims`: claims that need revision, with explanation and suggested fix
- `unsupported_claims`: claims with no evidence; must be removed or rephrased
- `inference_claims`: claims that are reasonable inferences and should be framed accordingly

## Rules

- Never approve an invented metric.
- Never approve a technology claim not in evidence.
- Never approve inflated ownership or seniority.
- Treat "likely" outcomes as inferences, not facts.
- If a claim cannot be fixed, remove it and note the gap.

## Confirmation policy

- Auto-execute: validating draft content against clear evidence.
- Ask for confirmation: when a claim is borderline, when rephrasing would materially change meaning, or when a potentially strong claim has only indirect evidence.
