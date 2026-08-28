# Skill: update-from-upstream

## Purpose

Adopt improvements from the upstream `ethan-os` repository into a personalized downstream OS without overwriting downstream customizations.

## Input

- Current downstream repository directory.
- `.os-upstream.yaml` manifest with the last incorporated upstream commit.
- Optionally, `--apply` to create a branch with safe changes; default is dry-run.

## Output

- A human-readable update plan classifying changes as safe, conflicted, downstream-only, or removed.
- If `--apply` is used, a new branch containing all safe updates and a manifest entry for this update.
- A list of conflicts that require human review before merging.

## Rules

1. Default to `--check` (dry run); never modify the downstream repo by surprise.
2. Preserve every file customized downstream unless the user explicitly resolves the conflict.
3. Never delete a downstream-only file because upstream removed something upstream.
4. Classify conflicts by type (text, behavior, schema, routing, config, removal).
5. Run validation after applying safe changes; do not commit if validation fails.
6. Update the manifest only after a successful apply.
7. Record rollback instructions if the update branch needs to be discarded.
