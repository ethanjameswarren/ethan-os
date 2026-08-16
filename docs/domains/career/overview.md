# Career Domain

The second fully implemented domain in Ethan OS.

## Purpose

Capture durable career evidence, analyze target roles, and build evidence-backed resumes and interview preparation.

## v0.1 objects

- Career Evidence (`career.evidence`)
- Job Target (`career.job-target`)
- Resume Content (`career.resume`)
- Interview Prep (`career.interview-prep`)

## Object flow

```
Career Evidence → Job Target → Resume Content → LaTeX Template → PDF
                              → Interview Prep
```

## Design principles

- Career Evidence is the single source of truth; downstream artifacts select and reframe it but never fabricate beyond it.
- Distinguish confirmed facts from inferences and unknowns.
- Every resume bullet and interview story traces back to specific evidence via `evidence_ids`.
- Content and presentation stay separate: canonical resume content lives in `career.resume` objects, presentation lives in `ethan-os/templates/`.
- Confidential implementation details are generalized before being retained.
