# Skill: audit-gym-equipment

## Purpose

Create or update a training location's equipment inventory from an audit (photo, walkthrough, website, or memory).

## Input

A location id and an audit report (text, list, or photo-derived observations).

## Extract

- each equipment item
- `canonical_type` from the equipment taxonomy
- `brand`, `model`, `quantity` if visible
- `confidence` for each item
- `audit_date`
- `audit_source`

## Rules

- Prefer `health.training-location` updates over creating a new object.
- Use `unknown` for quantities, max weights, or model numbers not clearly confirmed.
- Dual-function machines should be represented by one record per function.
- Do not add free-weight exercises (barbell back squat, etc.) unless `barbell`, `rack`, and `weight_plates` are all confirmed.

## Output

Update the `equipment` section of the location object in `ethan-life/domains/health/training-locations/`.

## Relationship types

- `derived_from` — location object → originating capture/audit
