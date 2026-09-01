#!/usr/bin/env python3
r"""
Bootstrap a personalized downstream OS from ethan-os.

Example:
    python scripts/bootstrap-personal-os.py ^
        --target-dir D:\GIT\john-os ^
        --os-name "John OS" ^
        --identifier john-os ^
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

from personalize import Personalizer, load_config as load_identity_config

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
        return "https://github.com/<upstream-owner>/ethan-os.git"


def copy_upstream(upstream_dir: Path, target_dir: Path):
    if target_dir.exists():
        raise FileExistsError(f"Target directory already exists: {target_dir}")

    def ignore(path, names):
        rel = Path(path).relative_to(upstream_dir)
        if rel == Path("."):
            return EXCLUDED_TOP_LEVEL.intersection(names)
        return []

    shutil.copytree(upstream_dir, target_dir, ignore=ignore)


def rewrite_readme(target_dir: Path, os_name: str, identifier: str, remote: str, framework_name: str, owner_name: str, companion_repo: str):
    readme = target_dir / "README.md"
    text = readme.read_text(encoding="utf-8")

    # Load the upstream framework name from the copied config so attribution is accurate.
    framework_name = framework_name or "Ethan OS"

    # Replace the first-level heading with the new OS name.
    lines = text.splitlines()
    title_idx = None
    for i, line in enumerate(lines):
        if line.startswith(f"# {framework_name}"):
            lines[i] = f"# {os_name}"
            title_idx = i
            break

    identity_block = (
        f"\n{os_name} is a personal OS built from [{framework_name}]({remote}). "
        f"It reuses {framework_name} workflows and schemas while keeping {companion_repo} as the private companion repository.\n\n"
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


def rewrite_config(target_dir: Path, os_name: str, os_repo: str, companion_repo: str, owner_name: str):
    config_path = target_dir / "config" / "ethan-os.config.yaml"
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))

    # Keep the framework section exactly as upstream; only the identity section changes.
    if "framework" not in data:
        data["framework"] = data.pop("ethan_os", {})
    data["identity"] = {
        "owner_name": owner_name,
        "os_name": os_name,
        "os_repo": os_repo,
        "life_repo": companion_repo,
    }
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
    # Prevent accidental pushes to the upstream ethan-os remote. The separate
    # `publish-to-github.py` script will configure `origin` once the user is
    # authenticated with GitHub.
    run_git("config", "--local", "push.default", "nothing", cwd=target_dir)
    run_git("add", ".", cwd=target_dir)
    run_git(
        "commit",
        "-m",
        f"Bootstrap {target_dir.name} from ethan-os {version} ({datetime.now(timezone.utc).date().isoformat()})",
        cwd=target_dir,
    )


def configure_devin_permissions(
    target_dir: Path, life_dir: Path | None, notion_dir: Path | None
):
    """Optionally apply Devin local-autonomy permissions for the new OS."""
    helper = target_dir / "scripts" / "configure-devin-permissions.py"
    if not helper.exists():
        print(f"WARNING: Devin permissions helper not found: {helper}")
        return

    cmd = [sys.executable, str(helper), "--os-dir", str(target_dir)]
    if life_dir:
        cmd.extend(["--life-dir", str(life_dir)])
    if notion_dir:
        cmd.extend(["--notion-dir", str(notion_dir)])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"WARNING: Devin permissions configuration failed:\n{result.stderr.strip()}")
        return
    print(result.stdout.strip())


def main():
    parser = argparse.ArgumentParser(
        description="Bootstrap a personal downstream OS from ethan-os."
    )
    parser.add_argument("--target-dir", required=True, help="Path for the new downstream OS repository.")
    parser.add_argument("--os-name", required=True, help="Display name for the new OS, e.g. 'John OS'.")
    parser.add_argument("--owner-name", default=None, help="Person's name, e.g. 'John'. Defaults to <os-name> without ' OS'.")
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
    parser.add_argument(
        "--configure-devin-permissions",
        action="store_true",
        help="Write Devin local-autonomy permissions for the new OS and its companion repo.",
    )
    parser.add_argument(
        "--life-dir",
        default=None,
        help="Path to the private companion (life) repository. Defaults to <target-dir-parent>/<companion-repo>.",
    )
    parser.add_argument(
        "--notion-dir",
        default=None,
        help="Optional path to a Notion integration repository to include in Devin permissions.",
    )
    args = parser.parse_args()

    target_dir = Path(args.target_dir).resolve()
    upstream_dir = Path(args.upstream_repo).resolve() if args.upstream_repo else ROOT

    owner_name = args.owner_name or args.os_name.removesuffix(" OS").strip() or "User"
    os_repo = target_dir.name
    companion_repo = args.companion_repo or f"{owner_name.lower()}-life"

    life_dir = Path(args.life_dir).resolve() if args.life_dir else target_dir.parent / companion_repo
    notion_dir = Path(args.notion_dir).resolve() if args.notion_dir else None

    if not upstream_dir.exists():
        print(f"ERROR: upstream directory does not exist: {upstream_dir}")
        sys.exit(1)

    target_dir.parent.mkdir(parents=True, exist_ok=True)

    try:
        copy_upstream(upstream_dir, target_dir)
        commit = get_upstream_commit(upstream_dir)
        remote = args.upstream_repo or get_upstream_remote(upstream_dir)
        version = read_version(upstream_dir)

        # Read the upstream framework name from the copied config before it is overwritten.
        framework_config = yaml.safe_load((target_dir / "config" / "ethan-os.config.yaml").read_text(encoding="utf-8"))
        framework = framework_config.get("framework", framework_config.get("ethan_os", {}))
        framework_name = framework.get("name", "Ethan OS")

        rewrite_readme(target_dir, args.os_name, args.identifier, remote, framework_name, owner_name, companion_repo)
        rewrite_config(target_dir, args.os_name, os_repo, companion_repo, owner_name)

        # Apply the downstream identity layer to all user-facing content.
        identity, framework = load_identity_config(target_dir)
        Personalizer(target_dir, identity, framework).personalize_repo()

        write_manifest(target_dir, version, args.os_name, args.identifier,
                       companion_repo, remote, commit)
        init_git(target_dir, remote, version)

        if args.configure_devin_permissions:
            configure_devin_permissions(target_dir, life_dir, notion_dir)

        print(f"\nBootstrapped {args.os_name} at {target_dir}")
        print(f"Upstream:     ethan-os {version} ({commit})")
        print(f"Companion:    {companion_repo}")
        print(f"\nNext steps:")
        print(f"1. Authenticate local Git with GitHub:")
        print(f"     gh auth login")
        print(f"     gh auth setup-git")
        print(f"2. Publish to GitHub (resumable; safe, no PAT in URL):")
        print(f"     python scripts/publish-to-github.py \\")
        print(f"       --os-dir {target_dir} \\")
        print(f"       --companion-dir <path-to-{companion_repo}> \\")
        print(f"       --owner <your-github-username-or-org>")
        print(f"3. If you prefer not to use GitHub, skip publishing and use the local repositories.")
        print(f"4. Run validation: python scripts/validate.py")
        print(f"5. To update later: python scripts/update-from-upstream.py --check")
        print(f"6. To configure Devin/local-agent permissions for autonomous work in this OS and its companion repo:")
        print(f"     python scripts/configure-devin-permissions.py --os-dir {target_dir} --life-dir {life_dir}")

    except Exception as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
