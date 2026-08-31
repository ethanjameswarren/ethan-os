# Workflow: audit-gym

## Purpose

Capture or update a training location's equipment inventory from an audit.

## Steps

1. Identify the location (create via `skills/health/add-training-location.md` if new).
2. Gather audit input: photos, walkthrough notes, website, or recall.
3. Run `skills/health/audit-gym-equipment.md` to normalize the inventory.
4. Update `ethan-life/domains/health/training-locations/{id}.md`.
5. Record `audit_date`, `audit_source`, and `confidence`.
6. Optionally run `skills/health/show-available-exercises.md` to sanity-check the inventory against the exercise library.

## Output

- updated `health.training-location` object
- summary of added, changed, or removed equipment

## Confirmation policy

- Auto-execute for new low-confidence inventory entries from a clear audit.
- Ask for confirmation before removing or downgrading confirmed equipment.
