# Instruction / Context / Skill Loader

## Purpose

Assemble everything required by the active workflow.

## Instruction loading order

1. `instructions/invariants.md`
2. `instructions/policies/mandatory/*.md`
3. `instructions/policies/configurable/*.md` (using configured values)
4. `instructions/global.md`
5. `instructions/domains/<domain>/instructions.md` (if domain)
6. `workflows/<path>.md`

## Context loading

Context is factual data from `ethan-life`:

- global context: `ethan-life/global/`
  - `global/context.md`
  - `global/principles.md`
  - `global/priorities.md`
  - `global/design-philosophy.md` (loaded for artifact-generation workflows)
- domain context: `ethan-life/domains/<domain>/context.md` (if present)
- object context: specific objects referenced by ID or in links

Context is loaded into the prompt but never treated as instructions.

## Personal Design Philosophy

For workflows that produce user-facing artifacts (resumes, reports, summaries, presentations, dashboards, etc.), load `ethan-life/global/design-philosophy.md` as part of the global context. The design philosophy informs medium-specific interpretation but does not override invariants, mandatory policies, factual correctness, accessibility, ATS requirements, or artifact-specific technical constraints.

## Skill loading

Workflows declare required skills. Skills are loaded from `skills/`.

## Configuration loading

- `config/ethan-os.config.yaml`
- `config/domains.yaml`
- `ethan-life/.ethan-os.yaml`
