# Skill: classify-domain

## Purpose

Determine which domain should handle the input.

## Input

- parsed user input
- enabled domains from `ethan-life/.ethan-os.yaml`

## Output

- domain name or `none`
- confidence
- reasoning

## v0.1 behavior

Only `knowledge` is enabled by default. Other domains are documented as extension points but not created.

If input clearly belongs to a disabled domain (e.g., food recipe), flag it and either store a generic capture or inform the user that the domain is not active.

## Instructions

- Do not require the user to know internal routing.
- If only one domain is enabled, route there unless input is clearly outside that domain.
- If ambiguous, use intent and context.
