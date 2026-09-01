#!/usr/bin/env python3
r"""
Configure Devin/local-agent permissions for routine work in this OS.

This is an optional helper. When run, it updates the user-level Devin config
(%APPDATA%\devin\config.json on Windows, ~/.config/devin/config.json elsewhere)
to auto-approve common read/search/edit/script/test/local-commit actions
inside the approved repository directories, while still prompting for
destructive git ops, push/deploy, credentials, system-wide changes,
machine-wide installs, and actions outside the approved workspaces.

Run from inside your OS repository after bootstrap:

    python scripts/configure-devin-permissions.py \
        --os-dir . \
        --life-dir ../<your-life> \
        --notion-dir ../<your-notion>

It is idempotent: running it again will refresh the permissions section while
preserving other Devin settings.
"""

import argparse
import json
import os
import sys
from pathlib import Path


def devin_config_path() -> Path:
    """Return the user-level Devin config path for the current platform."""
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        if not appdata:
            raise RuntimeError("APPDATA environment variable is not set")
        return Path(appdata) / "devin" / "config.json"
    # XDG_CONFIG_HOME fallback for macOS/Linux.
    config_home = os.environ.get("XDG_CONFIG_HOME")
    if config_home:
        return Path(config_home) / "devin" / "config.json"
    return Path.home() / ".config" / "devin" / "config.json"


def to_glob_path(path: Path) -> str:
    """Convert an absolute path to a forward-slash glob prefix ending with /**."""
    abs_path = path.resolve()
    return abs_path.as_posix() + "/**"


def build_permissions(approved_paths: list[Path]) -> dict:
    """Build the permissions object for the approved repo directories."""
    read_allow = [f"Read({to_glob_path(p)})" for p in approved_paths]
    write_allow = [f"Write({to_glob_path(p)})" for p in approved_paths]

    return {
        "allow": [
            *read_allow,
            *write_allow,
            "Exec(git status)",
            "Exec(git diff)",
            "Exec(git log)",
            "Exec(git add)",
            "Exec(git commit)",
            "Exec(git show)",
            "Exec(git stash)",
            "Exec(git fetch)",
            "Exec(npm run)",
            "Exec(npm test)",
            "Exec(npm install)",
            "Exec(npm exec)",
            "Exec(npx)",
            "Exec(pnpm run)",
            "Exec(pnpm test)",
            "Exec(pnpm install)",
            "Exec(pnpm exec)",
            "Exec(pnpm dlx)",
            "Exec(yarn run)",
            "Exec(yarn test)",
            "Exec(yarn install)",
            "Exec(yarn dlx)",
            "Exec(node)",
            "Exec(python)",
            "Exec(python3)",
            "Exec(vitest)",
            "Exec(jest)",
            "Exec(tsc)",
            "Exec(turbo)",
            "Exec(eslint)",
            "Exec(prettier)",
            "Exec(make)",
            "Exec(cargo)",
            "Exec(go)",
            "Exec(bun)",
            "Exec(deno)",
            "Exec(vite)",
            "Exec(next)",
            "Exec(cypress)",
            "Exec(playwright)",
        ],
        "ask": [
            "Exec(git push)",
            "Exec(git pull)",
            "Exec(git reset)",
            "Exec(git rebase)",
            "Exec(git merge)",
            "Exec(git checkout)",
            "Exec(git switch)",
            "Exec(git restore)",
            "Exec(git clean)",
            "Exec(git branch -d)",
            "Exec(git branch -D)",
            "Exec(git tag -d)",
            "Exec(git tag -D)",
            "Exec(git remote)",
            "Exec(git commit --amend)",
            "Exec(git cherry-pick)",
            "Exec(git revert)",
            "Exec(git stash drop)",
            "Exec(git stash pop)",
            "Exec(git bisect)",
            "Exec(git submodule)",
            "Exec(git worktree)",
            "Exec(git clone)",
            "Exec(git init)",
            "Exec(vercel)",
            "Exec(netlify)",
            "Exec(flyctl)",
            "Exec(kubectl)",
            "Exec(helm)",
            "Exec(docker compose up)",
            "Exec(docker push)",
            "Exec(npm install -g)",
            "Exec(npm i -g)",
            "Exec(pnpm install -g)",
            "Exec(pnpm add -g)",
            "Exec(yarn global)",
            "Exec(winget)",
            "Exec(choco)",
            "Exec(scoop)",
            "Exec(msiexec)",
            "Exec(reg)",
            "Exec(netsh)",
            "Exec(sudo)",
            "Exec(rm)",
            "Exec(del)",
            "Exec(rd)",
            "Exec(rmdir)",
            "Read(**/.env*)",
            "Write(**/.env*)",
            "Read(**/.ssh/**)",
            "Write(**/.ssh/**)",
            "Read(**/credentials*)",
            "Write(**/credentials*)",
        ],
        "deny": [
            "Exec(rm -rf /)",
            "Exec(del /f /s /q C:)",
            "Exec(format)",
            "Exec(diskpart)",
            "Exec(shred)",
            "Exec(dd)",
        ],
    }


def load_config(path: Path) -> dict:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return {}
    return json.loads(text)


def save_config(path: Path, config: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(config, indent=2) + "\n"
    path.write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Apply Devin local-autonomy permissions for this OS."
    )
    parser.add_argument(
        "--os-dir",
        default=".",
        help="Path to the OS repository. Defaults to the current directory.",
    )
    parser.add_argument(
        "--life-dir",
        default=None,
        help="Path to the private companion (life) repository. If omitted, inferred from config/ethan-os.config.yaml.",
    )
    parser.add_argument(
        "--notion-dir",
        default=None,
        help="Optional path to a Notion integration repository.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the permissions that would be written without writing them.",
    )
    args = parser.parse_args()

    os_dir = Path(args.os_dir).resolve()
    if not os_dir.is_dir():
        print(f"ERROR: --os-dir is not a directory: {os_dir}")
        return 1

    approved_paths = [os_dir]

    if args.life_dir:
        life_dir = Path(args.life_dir).resolve()
        if not life_dir.is_dir():
            print(f"WARNING: --life-dir does not exist yet: {life_dir}")
        approved_paths.append(life_dir)
    else:
        # Try to infer the companion repo from the OS config and recommended layout.
        config_path = os_dir / "config" / "ethan-os.config.yaml"
        if config_path.exists():
            try:
                import yaml

                data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
                identity = data.get("identity", {})
                life_repo = identity.get("life_repo")
                if life_repo:
                    inferred = os_dir.parent / life_repo
                    if inferred.is_dir():
                        approved_paths.append(inferred)
                    else:
                        print(f"WARNING: inferred life repo not found: {inferred}")
            except Exception as exc:
                print(f"WARNING: could not read OS config to infer life repo: {exc}")

    if args.notion_dir:
        notion_dir = Path(args.notion_dir).resolve()
        if not notion_dir.is_dir():
            print(f"WARNING: --notion-dir does not exist yet: {notion_dir}")
        approved_paths.append(notion_dir)

    config_path = devin_config_path()
    config = load_config(config_path)
    config["permissions"] = build_permissions(approved_paths)

    if args.dry_run:
        print(f"Would write to: {config_path}")
        print(json.dumps(config["permissions"], indent=2))
        return 0

    save_config(config_path, config)
    print(f"Devin local-autonomy permissions written to: {config_path}")
    print("Approved directories:")
    for p in approved_paths:
        print(f"  - {p}")
    print("\nRestart any running Devin sessions for the rules to take effect.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
