# Skill: assess-kit-for-assembly

## Purpose

Evaluate a kit before the user starts gluing: push-fit vs glue, cleanup, fragile parts, alternate builds, subassembly recommendations, and magnetization flag.

## Input

- `hobby.collection-item` record.
- Knowledge of the kit/game system (use reliable external/game-system facts only; do not invent).
- Existing `hobby.technique-skill` records for `magnetization` and `subassemblies`.

## Output

- Updated collection item with `assembly_notes`, `fragile_parts`, `subassembly_recommendation`, and a `magnetization_status` recommendation.
- A clear list of warnings before permanent glue is applied.

## Instructions

1. Identify construction type: push-fit, glue required, or mixed. Note any plastic/resin/metal differences.
2. Identify mould-line locations and general cleanup level required.
3. List fragile or thin parts (weapons, antennae, chains, spindly limbs, etc.).
4. List alternate builds, weapon options, or optional heads/pose pieces.
5. Determine whether magnetization is worthwhile using `check-magnetization`. Output `not_applicable`, `recommended`, or `optional` with rationale.
6. Recommend subassemblies if painting would be substantially easier before final assembly (e.g., arms crossing chest, weapons blocking torso, cloaks covering legs, separate heads). Do not over-recommend; avoid excessive subassemblies that make assembly harder.
7. Warn explicitly before the user glues anything that has alternate options or would benefit from magnetization.
8. Update the collection item's `magnetization_status` and `notes`, and record an event if a decision was made.
