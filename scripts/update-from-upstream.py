#!/usr/bin/env python3
"""
Assess and apply safe updates from upstream ethan-os to a downstream personal OS.

This script is meant to be run from inside a downstream OS repository that was
bootstrapped from ethan-os. It uses `.os-upstream.yaml` to know which upstream
commit the downstream repo was derived from.

Dry run (default):
    python scripts/update-from-upstream.py --check

Apply safe updates:
    python scripts/update-from-upstream.py --apply

The script refuses to modify files with downstream customizations unless those
changes are approved. It never deletes downstream-only work.
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

MANIFEST = ".os-upstream.yaml"


def run_git(*args, cwd=None, check=True):
    result = subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def load_manifest(repo: Path) -> dict:
    path = repo / MANIFEST
    if not path.exists():
        print(f"ERROR: {MANIFEST} not found. Is this a downstream repository bootstrapped from ethan-os?")
        sys.exit(1)
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def save_manifest(repo: Path, manifest: dict):
    (repo / MANIFEST).write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")


def upstream_head_ref(repo: Path) -> str:
    for ref in ["upstream/HEAD", "upstream/main", "upstream/master"]:
        try:
            return run_git("rev-parse", ref, cwd=repo)
        except RuntimeError:
            continue
    raise RuntimeError("Could not resolve upstream HEAD. Ensure the upstream remote is set.")


def upstream_branch_name(repo: Path) -> str:
    for ref in ["upstream/HEAD", "upstream/main", "upstream/master"]:
        try:
            run_git("rev-parse", ref, cwd=repo)
            return ref
        except RuntimeError:
            continue
    raise RuntimeError("Could not resolve upstream branch name.")


def git_diff_name_status(repo: Path, a, b):
    """Return list of (status, path1, path2) tuples from `git diff --name-status a..b`."""
    out = run_git("diff", "--name-status", "--find-renames=50%", f"{a}..{b}", cwd=repo)
    changes = []
    for line in out.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        status = parts[0]
        if status.startswith("R"):
            # rename: status\told\tnew
            changes.append((status, parts[1], parts[2]))
        else:
            changes.append((status, parts[1], None))
    return changes


LEGAL_ARTIFACTS = {"LICENSE", "NOTICE"}


def is_legal_artifact(path: str) -> bool:
    return path in LEGAL_ARTIFACTS


def classify_conflict(path: str, downstream_path: str, upstream_change: str, downstream_change: str) -> str:
    if is_legal_artifact(path):
        return "legal/project-lineage conflict"
    if downstream_change == "D" or upstream_change == "D":
        return "removal conflict"
    if path.startswith("schemas/"):
        return "schema conflict"
    if path.startswith("runtime/") or path == "entrypoint/ethan-os.md":
        return "routing conflict"
    if path.startswith("config/"):
        return "config conflict"
    if path.startswith(("workflows/", "skills/", "instructions/")):
        return "behavior conflict"
    return "text conflict"


def file_exists_in_tree(repo: Path, treeish: str, path: str) -> bool:
    try:
        run_git("cat-file", "-e", f"{treeish}:{path}", cwd=repo, check=True)
        return True
    except RuntimeError:
        return False


def read_upstream_file(repo: Path, ref: str, path: str) -> bytes:
    return run_git("show", f"{ref}:{path}", cwd=repo).encode("utf-8")


def discover_downstream_untracked(repo: Path):
    out = run_git("status", "--porcelain", "-u", cwd=repo)
    untracked = {}
    for line in out.splitlines():
        if line.startswith("?? "):
            rel = line[3:]
            untracked[rel] = "added downstream"
    return untracked


def check_clean_working_tree(repo: Path):
    out = run_git("status", "--porcelain", cwd=repo)
    if out.strip():
        return False
    return True


def build_update_plan(repo: Path, base_commit: str, upstream_commit: str, upstream_branch: str):
    downstream_commit = run_git("rev-parse", "HEAD", cwd=repo)

    upstream_changes = git_diff_name_status(repo, base_commit, upstream_commit)
    downstream_changes = git_diff_name_status(repo, base_commit, downstream_commit)

    downstream_index = {}
    for status, p1, p2 in downstream_changes:
        key = p1
        if status.startswith("R"):
            downstream_index[p1] = (status, p2)
            downstream_index[p2] = (status, p1)
        else:
            downstream_index[key] = (status, None)

    untracked = discover_downstream_untracked(repo)

    safe_updates = []
    safe_adds = []
    safe_removes = []
    conflicts = []
    legal_artifact_changes = []
    downstream_only = list(downstream_changes)

    for status, p1, p2 in upstream_changes:
        if status.startswith("R"):
            # Treat rename as delete old / add new for planning purposes.
            old_path, new_path = p1, p2
            if old_path in downstream_index:
                ds_status, ds_p2 = downstream_index[old_path]
                if ds_status == "D":
                    conflicts.append({
                        "path": old_path,
                        "upstream": "deleted",
                        "downstream": "deleted",
                        "type": "removal conflict",
                        "note": "Upstream renamed this file; downstream deleted it.",
                    })
                else:
                    conflicts.append({
                        "path": old_path,
                        "upstream": f"renamed to {new_path}",
                        "downstream": "modified",
                        "type": classify_conflict(old_path, "", "M", ds_status),
                        "note": f"Upstream renamed {old_path} to {new_path}; downstream modified the old path.",
                    })
            else:
                safe_removes.append({"path": old_path, "note": "Upstream renamed this file."})
                if new_path not in downstream_index and new_path not in untracked:
                    safe_adds.append({"path": new_path, "note": f"Renamed from {old_path}."})
                elif new_path in downstream_index or new_path in untracked:
                    conflicts.append({
                        "path": new_path,
                        "upstream": f"renamed from {old_path}",
                        "downstream": "exists/modified downstream",
                        "type": "text conflict",
                        "note": f"Upstream added/renamed {new_path}; it also exists downstream.",
                    })
            continue

        upstream_status = status
        downstream_status = downstream_index.get(p1)
        untracked_status = p1 in untracked

        legal = is_legal_artifact(p1)

        if upstream_status == "A":
            if downstream_status or untracked_status:
                ds = downstream_status[0] if downstream_status else "added downstream"
                conflicts.append({
                    "path": p1,
                    "upstream": "added",
                    "downstream": ds,
                    "type": classify_conflict(p1, "", upstream_status, ds),
                    "note": "Upstream added a file that already exists downstream.",
                })
            else:
                note = "Added upstream."
                item = {"path": p1, "note": note}
                safe_adds.append(item)
                if legal:
                    legal_artifact_changes.append(item)

        elif upstream_status == "M":
            if downstream_status:
                ds = downstream_status[0]
                conflicts.append({
                    "path": p1,
                    "upstream": "modified",
                    "downstream": ds,
                    "type": classify_conflict(p1, "", upstream_status, ds),
                    "note": "Changed by both upstream and downstream.",
                })
            else:
                note = "Upstream modified; downstream untouched."
                item = {"path": p1, "note": note}
                safe_updates.append(item)
                if legal:
                    legal_artifact_changes.append(item)

        elif upstream_status == "D":
            if legal:
                ds = downstream_status[0] if downstream_status else "unchanged"
                conflicts.append({
                    "path": p1,
                    "upstream": "deleted",
                    "downstream": ds,
                    "type": "legal/project-lineage conflict",
                    "note": "Upstream deleted a legal/project-lineage file.",
                })
            elif downstream_status:
                ds = downstream_status[0]
                conflicts.append({
                    "path": p1,
                    "upstream": "deleted",
                    "downstream": ds,
                    "type": "removal conflict",
                    "note": "Upstream deleted this file, but downstream has changes.",
                })
            else:
                safe_removes.append({"path": p1, "note": "Upstream deleted; downstream untouched."})

    # Untracked downstream files that upstream did not touch are preserved automatically.
    # Report them for visibility.
    preserved = list(untracked.keys())

    return {
        "base_commit": base_commit,
        "upstream_commit": upstream_commit,
        "downstream_commit": downstream_commit,
        "upstream_branch": upstream_branch,
        "safe_updates": safe_updates,
        "safe_adds": safe_adds,
        "safe_removes": safe_removes,
        "legal_artifact_changes": legal_artifact_changes,
        "conflicts": conflicts,
        "downstream_only": downstream_only,
        "preserved_untracked": preserved,
    }


def print_plan(plan: dict, manifest: dict):
    print(f"Update plan: {manifest['upstream']['project']} {manifest['upstream']['installed_version']} -> current upstream")
    print(f"Base (last incorporated upstream commit): {plan['base_commit']}")
    print(f"Upstream HEAD: {plan['upstream_commit']}")
    print(f"Downstream HEAD: {plan['downstream_commit']}")
    print()

    print(f"Safe updates: {len(plan['safe_updates'])}")
    for item in plan["safe_updates"]:
        print(f"  ~ {item['path']}")

    print(f"\nSafe additions: {len(plan['safe_adds'])}")
    for item in plan["safe_adds"]:
        print(f"  + {item['path']}")

    print(f"\nSafe removals: {len(plan['safe_removes'])}")
    for item in plan["safe_removes"]:
        print(f"  - {item['path']} ({item['note']})")

    if plan["legal_artifact_changes"]:
        print(f"\nLegal/project-lineage changes (still applied as safe updates): {len(plan['legal_artifact_changes'])}")
        for item in plan["legal_artifact_changes"]:
            print(f"  [legal] {item['path']} ({item['note']})")

    print(f"\nConflicts requiring review: {len(plan['conflicts'])}")
    for item in plan["conflicts"]:
        print(f"  ! {item['path']} ({item['type']})")
        print(f"    upstream:    {item['upstream']}")
        print(f"    downstream:  {item['downstream']}")
        print(f"    note:        {item['note']}")

    print(f"\nDownstream-only changes preserved: {len(plan['downstream_only'])}")
    for status, p1, p2 in plan["downstream_only"]:
        if status.startswith("R"):
            print(f"  * {p1} -> {p2}")
        elif status == "A":
            print(f"  + {p1}")
        elif status == "D":
            print(f"  - {p1}")
        else:
            print(f"  ~ {p1}")

    if plan["preserved_untracked"]:
        print(f"\nUntracked downstream files preserved: {len(plan['preserved_untracked'])}")
        for path in plan["preserved_untracked"]:
            print(f"  ? {path}")


def apply_safe_changes(repo: Path, plan: dict, upstream_branch: str):
    if not check_clean_working_tree(repo):
        print("ERROR: working tree is not clean. Commit or stash changes before applying an update.")
        sys.exit(1)

    branch_name = f"update-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    run_git("checkout", "-b", branch_name, cwd=repo)

    try:
        for item in plan["safe_updates"] + plan["safe_adds"]:
            run_git("checkout", upstream_branch, "--", item["path"], cwd=repo)

        for item in plan["safe_removes"]:
            # Only remove if it exists in the working tree.
            if (repo / item["path"]).exists():
                run_git("rm", "-f", item["path"], cwd=repo)

        run_git("add", ".", cwd=repo)

        # Nothing to commit if no safe changes affected staged content.
        diff_cached = run_git("diff", "--cached", "--stat", cwd=repo)
        if not diff_cached.strip():
            print(f"\nNo safe changes to apply on branch '{branch_name}'.")
            print(f"Review conflicts on the branch or discard it: git checkout - ; git branch -D {branch_name}")
            return branch_name

        # Validate before committing.
        validate = subprocess.run(
            ["python", "scripts/validate.py"],
            cwd=str(repo),
            capture_output=True,
            text=True,
        )
        if validate.returncode != 0:
            print("\nValidation failed after applying safe updates. Changes were not committed.")
            print(validate.stdout)
            print(validate.stderr)
            print(f"\nTo discard the update attempt and return to the previous state:")
            print(f"  git checkout -")
            print(f"  git branch -D {branch_name}")
            sys.exit(1)

        run_git(
            "commit",
            "-m",
            f"Update from {plan['base_commit'][:8]} to {plan['upstream_commit'][:8]} (safe changes only)",
            cwd=repo,
        )
        print(f"\nSafe updates committed on branch '{branch_name}'.")
        print(f"Remaining conflicts must be resolved manually before merging.")
        return branch_name
    except Exception as exc:
        print(f"ERROR during apply: {exc}")
        print(f"You may need to reset to the previous branch: git checkout - ; git branch -D {branch_name}")
        raise


def detect_new_capabilities(safe_adds: list, conflicts: list, base_commit: str, upstream_commit: str, repo: Path):
    """Very lightweight detection: new files under docs/capabilities or new workflow docs."""
    new_caps = []
    seen = set()
    for item in safe_adds + conflicts:
        p = item["path"]
        if p in seen:
            continue
        seen.add(p)
        if p.startswith("docs/capabilities/") or p.startswith("docs/workflows/"):
            new_caps.append(p)
    return new_caps


def update_manifest_after_apply(repo: Path, manifest: dict, plan: dict, branch_name: str):
    manifest["upstream"]["last_updated_commit"] = plan["upstream_commit"]
    manifest["upstream"]["last_updated_at"] = datetime.now(timezone.utc).isoformat()
    manifest["history"].append({
        "from_commit": plan["base_commit"],
        "to_commit": plan["upstream_commit"],
        "date": datetime.now(timezone.utc).isoformat(),
        "result": "success",
        "branch": branch_name,
        "conflicts_resolved": [],
        "skipped": [c["path"] for c in plan["conflicts"]],
    })
    save_manifest(repo, manifest)
    run_git("add", MANIFEST, cwd=repo)
    run_git("commit", "--amend", "--no-edit", cwd=repo)


def main():
    parser = argparse.ArgumentParser(
        description="Assess or apply updates from upstream ethan-os to a downstream OS."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        default=True,
        help="Dry-run: show the update plan without making changes (default).",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply safe updates to a new branch. Conflicts are left for manual review.",
    )
    args = parser.parse_args()

    repo = Path.cwd().resolve()
    if (repo / MANIFEST).exists():
        pass
    else:
        # If invoked from inside scripts/ but the repo root is the parent.
        repo = repo.parent
        if not (repo / MANIFEST).exists():
            print(f"ERROR: {MANIFEST} not found in current or parent directory.")
            sys.exit(1)

    manifest = load_manifest(repo)
    base_commit = manifest["upstream"].get("last_updated_commit") or manifest["upstream"]["installed_commit"]
    if not base_commit or base_commit == "unknown":
        print("ERROR: manifest does not record a usable upstream base commit. Cannot perform three-way update.")
        sys.exit(1)

    run_git("fetch", "upstream", cwd=repo)

    upstream_branch = upstream_branch_name(repo)
    upstream_commit = upstream_head_ref(repo)

    if base_commit == upstream_commit:
        print(f"Downstream {repo.name} is already up to date with upstream {upstream_commit[:8]}.")
        return

    plan = build_update_plan(repo, base_commit, upstream_commit, upstream_branch)
    new_caps = detect_new_capabilities(plan["safe_adds"], plan["conflicts"], base_commit, upstream_commit, repo)

    print_plan(plan, manifest)

    if new_caps:
        print("\nNew capabilities available in upstream:")
        for cap in new_caps:
            print(f"  * {cap}")

    if args.apply:
        if plan["conflicts"]:
            print("\nConflicts detected. Safe changes will be applied to a branch; conflicts must be resolved separately.")
        branch_name = apply_safe_changes(repo, plan, upstream_branch)
        update_manifest_after_apply(repo, manifest, plan, branch_name)
        print(f"\nManifest updated. Downstream is now based on upstream {upstream_commit[:8]}.")
        if plan["conflicts"]:
            print(f"Review conflicts on branch '{branch_name}', resolve them, then merge the branch.")
    else:
        print("\nThis was a dry run. Use --apply to create a branch with safe changes.")


if __name__ == "__main__":
    main()
