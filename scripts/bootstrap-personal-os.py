#!/usr/bin/env python3
"""
Bootstrap a personalized downstream OS from ethan-os.

Example:
    python scripts/bootstrap-personal-os.py \
        --target-dir D:\GIT\john-os \
        --os-name "John OS" \
        --identifier john-os \
        --companion-repo john-life

The script:
1. Copies the current ethan-os repository into a new downstream directory.
2. Initializes git and records the upstream project + commit in `.os-upstream.yaml`.
3. Rewrites the downstream README and config with the new OS identity.
4. Preserves upstream project attribution ("Built from Ethan OS").
"""

import argparse
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def read_version(upstream_dir: Path) -> str:
    version_path = upstream_dir / "VERSION"
    if version_path.exists():
        return version_path.read_text(encoding="utf-8").strip()
    return "unknown"


EXCLUDED_TOP_LEVEL = {
    ".git",
    ".os-upstream.yaml",
    "_check_links.py",
}


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


def get_upstream_commit(upstream_dir: Path) -> str:
    try:
        return run_git("rev-parse", "HEAD", cwd=upstream_dir)
    except (RuntimeError, FileNotFoundError) as exc:
        print(f"Warning: could not determine upstream git HEAD ({exc}). Using 'unknown'.")
        return "unknown"


def get_upstream_remote(upstream_dir: Path) -> str:
    try:
        return run_git("remote", "get-url", "origin", cwd=upstream_dir)
    except (RuntimeError, FileNotFoundError):
        # Fall back to a generic canonical URL.
        return "https://github.com/ethanjameswarren/ethan-os.git"


def copy_upstream(upstream_dir: Path, target_dir: Path):
    if target_dir.exists():
        raise FileExistsError(f"Target directory already exists: {target_dir}")

    def ignore(path, names):
        rel = Path(path).relative_to(upstream_dir)
        if rel == Path("."):
            return EXCLUDED_TOP_LEVEL.intersection(names)
        return []

    shutil.copytree(upstream_dir, target_dir, ignore=ignore)


def rewrite_readme(target_dir: Path, os_name: str, identifier: str):
    readme = target_dir / "README.md"
    text = readme.read_text(encoding="utf-8")

    # Replace the first-level heading with the new OS name.
    lines = text.splitlines()
    title_idx = None
    for i, line in enumerate(lines):
        if line.startswith("# Ethan OS"):
            lines[i] = f"# {os_name}"
            title_idx = i
            break

    identity_block = (
        f"\n{os_name} is a personal OS built from [Ethan OS](https://github.com/ethanjameswarren/ethan-os). "
        f"It reuses Ethan OS workflows and schemas while keeping {identifier}-life as the private companion repository.\n\n"
    )
    if identity_block.strip() not in text:
        if title_idx is not None:
            # Insert right after the title line.
            insert_idx = title_idx + 1
            lines.insert(insert_idx, identity_block.rstrip())
        else:
            # No Ethan OS title found; prepend at top.
            lines.insert(0, f"# {os_name}")
            lines.insert(1, identity_block.rstrip())

    text = "\n".join(lines)
    readme.write_text(text, encoding="utf-8")


def rewrite_config(target_dir: Path, os_name: str):
    config_path = target_dir / "config" / "ethan-os.config.yaml"
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    data["ethan_os"]["name"] = os_name
    config_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def write_manifest(target_dir: Path, version: str, os_name: str, identifier: str,
                     companion_repo: str, remote: str, commit: str):
    manifest = {
        "upstream": {
            "project": "Ethan OS",
            "identifier": "ethan-os",
            "repository": remote,
            "license": "Apache-2.0",
            "installed_version": version,
            "installed_commit": commit,
            "installed_at": datetime.now(timezone.utc).isoformat(),
            "last_updated_commit": commit,
            "last_updated_at": datetime.now(timezone.utc).isoformat(),
        },
        "downstream": {
            "project": os_name,
            "name": os_name,
            "identifier": identifier,
            "companion_repository": companion_repo,
        },
        "update": {
            "strategy": "safe_merge",
        },
        "history": [
            {
                "from_commit": commit,
                "to_commit": commit,
                "date": datetime.now(timezone.utc).isoformat(),
                "result": "bootstrap",
                "conflicts_resolved": [],
                "skipped": [],
            }
        ],
    }
    (target_dir / ".os-upstream.yaml").write_text(
        yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8"
    )


def init_git(target_dir: Path, remote: str, version: str):
    run_git("init", cwd=target_dir)
    run_git("remote", "add", "upstream", remote, cwd=target_dir)
    run_git("add", ".", cwd=target_dir)
    run_git(
        "commit",
        "-m",
        f"Bootstrap {target_dir.name} from ethan-os {version} ({datetime.now(timezone.utc).date().isoformat()})",
        cwd=target_dir,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Bootstrap a personal downstream OS from ethan-os."
    )
    parser.add_argument("--target-dir", required=True, help="Path for the new downstream OS repository.")
    parser.add_argument("--os-name", required=True, help="Display name for the new OS, e.g. 'John OS'.")
    parser.add_argument("--identifier", required=True, help="Short identifier, e.g. 'john-os'.")
    parser.add_argument(
        "--companion-repo",
        default=None,
        help="Private companion repository name. Defaults to <identifier>-life.",
    )
    parser.add_argument(
        "--upstream-repo",
        default=None,
        help="Path or URL to upstream ethan-os. Defaults to the repository containing this script.",
    )
    args = parser.parse_args()

    target_dir = Path(args.target_dir).resolve()
    upstream_dir = Path(args.upstream_repo).resolve() if args.upstream_repo else ROOT
    companion_repo = args.companion_repo or f"{args.identifier}-life"

    if not upstream_dir.exists():
        print(f"ERROR: upstream directory does not exist: {upstream_dir}")
        sys.exit(1)

    target_dir.parent.mkdir(parents=True, exist_ok=True)

    try:
        copy_upstream(upstream_dir, target_dir)
        commit = get_upstream_commit(upstream_dir)
        remote = args.upstream_repo or get_upstream_remote(upstream_dir)
        version = read_version(upstream_dir)

        rewrite_readme(target_dir, args.os_name, args.identifier)
        rewrite_config(target_dir, args.os_name)
        write_manifest(target_dir, version, args.os_name, args.identifier,
                       companion_repo, remote, commit)
        init_git(target_dir, remote, version)

        print(f"\nBootstrapped {args.os_name} at {target_dir}")
        print(f"Upstream:     ethan-os {version} ({commit})")
        print(f"Companion:    {companion_repo}")
        print(f"\nNext steps:")
        print(f"1. Create a private companion repository named '{companion_repo}'.")
        print(f"2. Add a .{args.identifier}-os.yaml file at its root pointing back to this directory.")
        print(f"3. Run validation: python scripts/validate.py")
        print(f"4. To update later: python scripts/update-from-upstream.py --check")

    except Exception as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
