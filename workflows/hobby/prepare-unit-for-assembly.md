# Workflow: prepare-unit-for-assembly

## Purpose

Inspect a kit before assembly, warn about anything that should not be glued permanently yet, and record the assembly plan.

## Trigger

- "I'm about to build the Skorpekh Destroyers."
- "Should I subassemble the Overlord?"
- "What do I need to watch out for on the Doomstalker?"

## Inputs

- Collection item title or ID.

## Outputs

- Updated `hobby.collection-item` with assembly notes and magnetization/subassembly decisions.
- A clear go/no-go checklist before glue.

## Steps

1. Run `ethan-os/skills/hobby/assess-kit-for-assembly.md`.
2. If magnetization is `recommended`, run `ethan-os/skills/hobby/check-magnetization.md` and require an explicit decision before proceeding.
3. List push-fit vs glue points, mould-line cleanup areas, and fragile parts.
4. State whether subassemblies are recommended and which parts to keep separate.
5. Warn explicitly: "Do not glue X until you decide Y."
6. Record the plan in the collection item and confirm next steps.
