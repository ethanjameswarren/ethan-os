# Personal Design Philosophy

Ethan OS supports a global Personal Design Philosophy that influences how all user-facing artifacts are generated.

## Ownership

- The logic for interpreting design preferences belongs to `ethan-os`.
- Ethan's actual preferences belong in `ethan-life/global/design-philosophy.md`.
- Do not hard-code Ethan's taste into public `ethan-os` instructions or templates.

## Global design profile

`ethan-life/global/design-philosophy.md` captures human-readable preferences such as:

- overall aesthetic philosophy
- information density
- hierarchy
- whitespace
- typography preferences
- layout philosophy
- visual restraint
- color philosophy
- preferred level of polish
- modern vs traditional preferences
- technical vs editorial character
- preferred references and inspirations
- disliked patterns
- strong preferences
- flexible preferences
- things to avoid
- things never to use
- evolution of important preferences

No large configuration schema is required. The file is Markdown for human readability and AI interpretation.

## Global inheritance

Artifact-generation workflows should consult the Personal Design Philosophy by default.

Do not load it into workflows that do not create or materially alter user-facing output, such as purely deterministic validation.

The runtime determines when design context is relevant and loads it at the appropriate precedence level.

## Precedence

The Personal Design Philosophy sits at the **object/context data** layer. It must never override:

- core invariants
- mandatory policies
- factual correctness
- accessibility
- ATS or other technical requirements
- artifact-specific technical constraints

When design preferences conflict with functional requirements, preserve function and apply the closest appropriate expression of Ethan's taste.

## Medium-specific interpretation

Do not apply identical formatting rules to every medium. Instead:

```
Personal Design Philosophy
  → medium/artifact interpretation
  → output
```

### Markdown

Interpret through heading hierarchy, section structure, whitespace, bullet usage, information density, emphasis, readability, concision, and consistency.

### LaTeX / PDF

Interpret through typography, margins, spacing, alignment, dividers, hierarchy, page composition, and restrained visual treatment.

### Presentation

Interpret through slide density, typography, whitespace, composition, visual hierarchy, use of imagery, and restrained styling.

### Dashboard / App

Interpret through design system, layout, component density, navigation, typography, spacing, interaction patterns, and color system.

## Consistency goal

Artifacts produced across Ethan OS should feel recognizably like they belong to the same person and system without being visually identical.

## Integration with Career / Resume

The resume renderer consumes the same global Personal Design Philosophy. Resume-specific constraints (ATS readability, section conventions) are layered on top, not defined independently.

A resume-specific aesthetic override may be added later if the global philosophy cannot adequately express resume requirements.
