# Workflow: update-from-upstream

## Purpose

Adopt improvements from the upstream `ethan-os` repository into a downstream personal OS safely.

## Triggers

- "Check for Ethan OS updates."
- "Update John OS from upstream."
- "What changed upstream?"
- "Can I upgrade to Ethan OS 1.5?"

## Steps

1. Confirm the current repository is a downstream OS with a `.os-upstream.yaml` manifest.
2. Read the recorded upstream base commit from the manifest.
3. Fetch the latest upstream changes.
4. Run `scripts/update-from-upstream.py --check` to produce a dry-run update plan.
5. Present the plan in plain language:
   - safe updates,
   - safe additions,
   - safe removals,
   - conflicts requiring review,
   - downstream-only customizations preserved,
   - new capabilities available.
6. For each conflict, explain what upstream changed, what downstream changed, the likely impact, and a recommended resolution.
7. Ask whether to apply safe changes and which conflicts to resolve.
8. If approved, run `scripts/update-from-upstream.py --apply`.
9. After application, run validation tests. If they fail, report failure and provide rollback instructions.
10. If validation passes, update the manifest and summarize the result.

## Output

- A dry-run plan or a new branch with safe upstream changes applied.
- A list of unresolved conflicts (if any) with human-readable explanations.
- Updated `.os-upstream.yaml` manifest after successful application.

## Confirmation policy

- Dry-run is auto-executed and read-only.
- Applying safe changes requires explicit approval when any conflict exists.
- Applying safe changes when no conflicts exist is low-risk but should still be confirmed.
- Conflict merges require human review before writing.
