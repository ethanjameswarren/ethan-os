# Workflow: pre-build-magnetization-check

## Purpose

Before assembling a kit with alternate builds or weapon options, decide whether magnetization is worthwhile and record the decision.

## Trigger

- "Should I magnetize the Skorpekh Destroyers?"
- "About to build the Lokhust Heavy Destroyer."
- "The Overlord has multiple weapon options."

## Inputs

- Kit name and any known alternate options.
- User's current preference and uncertainty.

## Outputs

- Updated `magnetization_status` and `magnetization_note` on the collection item.
- A clear go/no-go recommendation for assembly.

## Steps

1. Run `ethan-os/skills/hobby/check-magnetization.md`.
2. If `magnetization_status` becomes `decided_yes`, ask whether to record a future magnetization session.
3. If status is `undecided`, block the collection item from `assembly_status: assembled` until resolved.
4. Confirm the recorded decision.
