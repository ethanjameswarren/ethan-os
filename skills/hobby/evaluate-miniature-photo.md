# Skill: evaluate-miniature-photo

## Purpose

Provide a focused visual evaluation of a miniature photograph during a painting phase.

## Input

- Current painting phase and plan.
- User-uploaded photograph.
- `hobby.technique-skill` and `hobby.paint-supply` context.

## Output

- Structured feedback: correct, must-fix, worthwhile improvement, optional refinement.
- Specific correction instructions.

## Instructions

1. Look at the overall miniature first: identify the visual category (Cyan/Red/Purple) and whether the army-wide scheme is readable.
2. Compare against the current phase's intended outcome. Do not judge phases the user has not attempted yet.
3. Use plain language. Avoid jargon unless the user has demonstrated familiarity.
4. Provide a short list:
   - **Correct** — what matches the plan.
   - **Must fix** — what will be hard to correct later or breaks readability.
   - **Worthwhile improvement** — what will noticeably improve the model if corrected now.
   - **Optional refinement** — fine detail that can wait.
5. For each must-fix, give a concrete correction: which paint/tool, which brush, where to apply, what to avoid touching.
6. If the photo quality makes judgment uncertain (glare, blur, poor color balance), say so and request another angle or better lighting.
7. End with a clear recommendation: proceed, fix first, or consider a longer session if multiple issues exist.
