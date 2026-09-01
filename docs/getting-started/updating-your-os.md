# Importing Upstream Updates into Your OS

Ethan OS evolves over time. Your downstream OS can import improvements from upstream and then update its own repo, all without losing its customizations.

This is an import, not a `git pull` from `ethan-os`. The process fetches the latest upstream state, compares it to your OS, and applies only safe changes to a new branch in your own repository. Conflicting files are left untouched for you to review.

This guide explains the safe import workflow.

## The basic idea

Your downstream repository remembers the exact upstream Ethan OS commit it was derived from. When you run an update, the system compares:

- **Base** — the Ethan OS commit your downstream OS was last based on
- **Upstream** — the latest Ethan OS commit
- **Downstream** — your current `john-os` repository

For every changed file, the update tool decides whether the change is safe to apply or whether it conflicts with something you customized.

## Safety rules

- **Dry run first.** The default `update-from-upstream` command shows the plan without changing anything.
- **Preserve downstream customizations.** If you changed a file and upstream also changed it, the update tool flags a conflict and does not overwrite your version.
- **Never delete downstream work.** If upstream removed a file but you modified it, the file is preserved and you are warned.
- **Validate after applying.** Safe updates are committed on a branch only if validation passes.
- **No silent adoption.** You choose whether to apply safe changes and you review conflicts before merging.

## Step 1: Check for updates

From inside your downstream OS repository (`john-os`), run:

```bash
python scripts/update-from-upstream.py --check
```

This produces a report like:

```
Update plan: ethan-os 0.1.0 -> current upstream
Base:         abc1234
Upstream:    def5678

Safe updates: 3
  ~ schemas/registry.yaml
  ~ scripts/validate.py
  ~ docs/domains/knowledge/overview.md

Safe additions: 1
  + docs/capabilities/schedule-planning.md

Safe removals: 0

Conflicts requiring review: 1
  ! workflows/knowledge/start-reading.md (behavior conflict)
    upstream:    modified
    downstream:  modified
    note:        Changed by both upstream and downstream.

New capabilities available:
  * docs/capabilities/schedule-planning.md
```

If there are no changes, the tool says so and exits.

## Step 2: Review conflicts

Conflicts are classified by type:

| conflict type | what it means |
|-----------------|---------------|
| Text conflict | Both sides changed the same file in overlapping ways. |
| Behavior conflict | A workflow, skill, or instruction changed on both sides. |
| Schema conflict | Upstream changed an object contract and your downstream workflows depend on it. |
| Routing conflict | Upstream changed runtime routing and you have custom routing. |
| Config conflict | Upstream changed configuration defaults that you customized. |
| Removal conflict | Upstream deleted a file that you modified or still use. |

For each conflict, the report explains:

- what upstream changed
- what you changed
- why it matters
- the recommended resolution

You can resolve the conflict manually in your editor or by asking your OS to help merge the changes.

## Step 3: Apply safe changes

When you are ready, run:

```bash
python scripts/update-from-upstream.py --apply
```

This:

1. Creates a new branch.
2. Applies all safe updates and additions.
3. Leaves conflicted files untouched.
4. Runs validation.
5. If validation passes, commits the safe changes and updates `.os-upstream.yaml`.

You will still need to merge or resolve any conflicts on the branch before it becomes your main branch.

## Step 4: Resolve conflicts

If conflicts remain:

```bash
git status
# edit conflicted files
git add <resolved files>
git commit -m "Resolve upstream update conflicts"
git checkout main
# or your default branch
git merge update-YYYYMMDD-HHMMSS
```

If you decide you do not want the update at all, you can delete the branch:

```bash
git checkout main
git branch -D update-YYYYMMDD-HHMMSS
```

Your main branch and manifest are unchanged.

## Licensing and attribution during updates

Upstream license and NOTICE requirements remain intact. The update tool treats `LICENSE` and `NOTICE` as protected legal/project-lineage artifacts:

- If upstream changes `LICENSE` or `NOTICE` and your downstream copy is unchanged, the change is applied but flagged for your awareness.
- If you added downstream notices and upstream also changed `NOTICE`, the file is treated as a conflict and your additions are preserved.
- The tool never silently strips upstream attribution or deletes your downstream notices.

You are responsible for ensuring any public distribution of your downstream OS complies with the Apache License 2.0.

## Failure and rollback

If validation fails after safe changes are applied, the script stops before committing. The branch with the attempted changes is left in place so you can inspect it. To discard it:

```bash
git checkout main
git branch -D update-YYYYMMDD-HHMMSS
```

The manifest is only updated after a successful apply, so your OS remains based on the previous upstream commit.

## Selective adoption

You do not have to enable every new upstream capability immediately. The update tool reports new capabilities, but it does not automatically turn them on. You can:

- Apply safe changes and ignore a new workflow until you are ready.
- Skip an update entirely.
- Add a new capability to your OS by copying or merging the relevant files after reviewing them.

## Keeping `.os-upstream.yaml` accurate

Do not edit this file by hand unless you know what you are doing. It records the upstream commit your OS is based on, which is required for the next three-way update.

## Example: John OS update

```
Ethan OS 1.4.0
  |
  +-- John OS bootstrapped (customized README, added garden workflow)
  |
Ethan OS 1.5.0 released
  |
  +-- John runs update-from-upstream --check
        Safe: 12 files
        Conflict: 1 workflow John customized
  |
  +-- John resolves the conflict in the update branch
  |
  +-- John merges the branch
        John OS is now based on Ethan OS 1.5.0
```

## Next

- [Create your own OS](create-your-own-os.md)
- [Core principles](../concepts/principles.md)
- [High-level architecture](../concepts/architecture-overview.md)
