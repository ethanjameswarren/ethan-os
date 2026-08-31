# Health Equipment Object Prompt

## Purpose

Define a single piece of exercise equipment at a training location.

## Required fields

- `id`: stable ID
- `schema`: `health.equipment`
- `schema_version`: `1`
- `title`
- `created_at`
- `provenance`
- `category`
- `equipment_type`: canonical type from `ethan-os/config/health/equipment-taxonomy.yaml`
- `confidence`: high | medium | low | unknown

## Optional fields

- `brand`
- `model`
- `product_family`
- `quantity`
- `weight_range`
- `capacity`
- `attachments`
- `features`
- `availability`: available | occupied | out_of_order | unknown
- `notes`
- `links`

## Instructions

- Use the canonical `equipment_type` from the taxonomy. If none fits, add to the taxonomy first.
- Mark `confidence` and `quantity` conservatively. Use `unknown` for unverified details.
- For dual-function machines, create one equipment record per function with a note referencing the shared machine.
