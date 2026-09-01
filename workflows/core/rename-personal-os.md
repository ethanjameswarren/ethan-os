# Workflow: rename-personal-os

## Purpose

Rebrand an existing `ethan-os` and `ethan-life` pair in place so they carry the person's name instead of Ethan's.

## Warning

This changes the upstream repository itself. If the goal is to keep `ethan-os` as a reusable upstream and create a separate personal OS, use `workflows/core/bootstrap-personal-os.md` instead.

## Triggers

- "I already have ethan-os and ethan-life, make them my name."
- "Rename my existing ethan-os and ethan-life."
- "Rebrand the OS and life repos I already cloned."

## Steps

1. Ask for the person's name (e.g., "John").
2. Propose new directory names and identifiers:
   - OS directory: `<identifier>-os` (default `<name>-os`)
   - Companion directory: `<identifier>-life` (default `<name>-life`)
3. Confirm the current `ethan-os` and `ethan-life` paths and the target paths. Stop if either target already exists.
4. Check for Python 3.10+.
5. Rename the directories on disk:
   - `ethan-os` -> `<identifier>-os`
   - `ethan-life` -> `<identifier>-life`
6. Update the companion pointer:
   - Rename `<identifier>-life/.ethan-os.yaml` to `.<identifier>-os.yaml`
   - Change the top-level key from `ethan_os` to `<identifier>_os`
   - Update `repository` to `../<identifier>-os`
   - Update `storage.path` to `../<identifier>-life` if a `storage` block exists
7. Update the OS identity:
   - Rewrite `<identifier>-os/README.md` title to `<name> OS`
   - Set `<identifier>-os/config/ethan-os.config.yaml` key `ethan_os.name` to `<name> OS`
8. Record provenance:
   - Add or update `<identifier>-os/.os-upstream.yaml` with `upstream.project: Ethan OS` and `downstream.project: <name> OS`
9. Confirm the new directories and updated files.
10. Provide next steps: validate with `python scripts/validate.py`, re-link git remotes if desired, and begin using `<identifier>-os` as the new OS.

## Output

- Renamed `<identifier>-os` and `<identifier>-life` directories.
- Updated companion pointer (`.<identifier>-os.yaml`).
- Updated OS display name in `README.md` and `config/ethan-os.config.yaml`.
- `.os-upstream.yaml` manifest recording the original `ethan-os`.

## Confirmation policy

Ask for explicit confirmation before renaming directories or rewriting files. Directory renames are medium-risk and not easily reversible.
