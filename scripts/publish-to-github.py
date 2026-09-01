#!/usr/bin/env python3
"""
Publish a downstream OS and its companion repository to GitHub.

This script is resumable: if it stops for authentication or a network failure,
simply run it again after fixing the issue. It will skip steps already completed.

It never creates, reads, or writes GitHub tokens or PATs. Authentication is
provided by the local environment (GitHub CLI, SSH, or a git credential manager).
"""

import argparse
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from github_auth import AuthState, check_github_auth, gh_installed, recommended_setup


class PublishError(RuntimeError):
    pass


def run_git(*args, cwd=None, check=True):
    result = subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        raise PublishError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def run_gh(*args, check=True):
    if not gh_installed():
        raise PublishError("GitHub CLI (gh) is required for repo creation but is not installed.")
    result = subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        raise PublishError(f"gh {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def repo_exists(owner, repo):
    """Return True if the GitHub repo already exists."""
    if not gh_installed():
        # Fallback: try a lightweight ls-remote over HTTPS. Requires auth already in place.
        result = subprocess.run(
            ["git", "ls-remote", f"https://github.com/{owner}/{repo}.git"],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    result = subprocess.run(
        ["gh", "repo", "view", f"{owner}/{repo}"],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def create_repo(owner, repo, private=False):
    """Create a GitHub repo. Does nothing and returns False if it already exists."""
    if repo_exists(owner, repo):
        return False
    visibility = "--private" if private else "--public"
    run_gh("repo", "create", f"{owner}/{repo}", visibility)
    return True


def set_origin(repo_dir, owner, repo, use_ssh=False):
    """Set origin to an HTTPS or SSH URL with no token in it."""
    if use_ssh:
        url = f"git@github.com:{owner}/{repo}.git"
    else:
        url = f"https://github.com/{owner}/{repo}.git"

    existing = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=str(repo_dir),
        capture_output=True,
        text=True,
    )
    if existing.returncode == 0:
        current = existing.stdout.strip()
        if current == url:
            return url
        run_git("remote", "set-url", "origin", url, cwd=repo_dir)
    else:
        run_git("remote", "add", "origin", url, cwd=repo_dir)

    # Ensure pushes go to origin, not upstream (ethan-os).
    run_git("config", "--local", "remote.pushDefault", "origin", cwd=repo_dir)
    return url


def current_branch(repo_dir):
    return run_git("branch", "--show-current", cwd=repo_dir)


def push_repo(repo_dir, branch=None):
    if branch is None:
        branch = current_branch(repo_dir)
    run_git("push", "-u", "origin", branch, cwd=repo_dir)


def ensure_companion(companion_dir, identifier, os_dir):
    """Make sure a local companion repo exists with the .os.yaml pointer."""
    companion = Path(companion_dir).resolve()
    companion.mkdir(parents=True, exist_ok=True)

    git_dir = companion / ".git"
    if not git_dir.exists():
        run_git("init", cwd=companion)

    pointer = companion / f".{identifier}-os.yaml"
    if not pointer.exists():
        content = (
            f"{identifier}_os:\n"
            f"  repository: {os_dir}\n"
            f"  version: 0.1.1-beta\n"
            f"  domains:\n"
            f"    knowledge:\n"
            f"      enabled: true\n"
            f"\n"
            f"storage:\n"
            f"  backend: local_git\n"
            f"  path: .\n"
        )
        pointer.write_text(content, encoding="utf-8")

    readme = companion / "README.md"
    if not readme.exists():
        readme.write_text(
            f"# {companion.name}\n\n"
            f"Private companion repository for {identifier}-os.\n",
            encoding="utf-8",
        )

    run_git("add", ".", cwd=companion)

    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=str(companion),
        capture_output=True,
        text=True,
    )
    if status.stdout.strip():
        run_git(
            "commit",
            "-m",
            f"init {companion.name} ({datetime.now(timezone.utc).date().isoformat()})",
            cwd=companion,
        )

    return companion


def verify_repo_is_git(repo_dir):
    git_dir = Path(repo_dir).resolve() / ".git"
    if not git_dir.exists():
        raise PublishError(f"{repo_dir} is not a git repository.")


def publish_os(os_dir, owner, create_repos=True, use_ssh=False):
    os_path = Path(os_dir).resolve()
    verify_repo_is_git(os_path)
    repo_name = os_path.name

    if create_repos:
        print(f"Ensuring GitHub repo {owner}/{repo_name} exists...")
        create_repo(owner, repo_name, private=False)

    url = set_origin(os_path, owner, repo_name, use_ssh=use_ssh)
    print(f"Set origin: {url}")

    print("Pushing OS repository...")
    push_repo(os_path)
    print(f"Published {repo_name} to {url}")


def publish_companion(companion_dir, owner, identifier, os_dir, create_repos=True, use_ssh=False):
    companion = ensure_companion(companion_dir, identifier, os_dir)
    repo_name = companion.name

    if create_repos:
        print(f"Ensuring GitHub repo {owner}/{repo_name} exists...")
        create_repo(owner, repo_name, private=True)

    url = set_origin(companion, owner, repo_name, use_ssh=use_ssh)
    print(f"Set origin: {url}")

    print("Pushing companion repository...")
    push_repo(companion)
    print(f"Published {repo_name} to {url}")


def main():
    parser = argparse.ArgumentParser(
        description="Publish a downstream OS and optional companion repo to GitHub."
    )
    parser.add_argument("--os-dir", required=True, help="Path to the local OS repository.")
    parser.add_argument("--companion-dir", default=None, help="Path to the local companion repository. If not given, only the OS is published.")
    parser.add_argument("--owner", required=True, help="GitHub username or organization that owns the repos.")
    parser.add_argument("--create-repos", action="store_true", default=True, help="Create the GitHub repositories if they do not exist.")
    parser.add_argument("--no-create-repos", action="store_false", dest="create_repos", help="Do not attempt to create GitHub repositories.")
    parser.add_argument("--ssh", action="store_true", default=False, help="Use SSH (git@github.com) URLs instead of HTTPS.")
    parser.add_argument("--identifier", default=None, help="Short identifier used for the companion .os.yaml filename. Defaults to the OS directory name with '-os' removed.")
    args = parser.parse_args()

    print("Checking local Git/GitHub authentication...")
    state, message = check_github_auth()
    print(message)

    if state != AuthState.AUTHENTICATED:
        print("\n" + recommended_setup("beginner"))
        print("\n" + "=" * 60)
        print("Bootstrap local setup is already complete.")
        print("After authenticating, re-run the same command to continue publishing:")
        print("  " + " ".join(sys.argv))
        print("=" * 60)
        return 1

    # When using GitHub CLI, make sure git uses it for HTTPS credentials.
    if not args.ssh and gh_installed():
        try:
            subprocess.run(["gh", "auth", "setup-git"], capture_output=True, text=True, check=False)
        except Exception:
            pass

    identifier = args.identifier
    if not identifier:
        # Derive identifier from os_dir name by stripping a trailing -os or -OS.
        os_name = Path(args.os_dir).resolve().name
        if os_name.lower().endswith("-os"):
            identifier = os_name[:-3]
        else:
            identifier = os_name

    try:
        publish_os(args.os_dir, args.owner, create_repos=args.create_repos, use_ssh=args.ssh)

        if args.companion_dir:
            publish_companion(
                args.companion_dir,
                args.owner,
                identifier,
                Path(args.os_dir).resolve(),
                create_repos=args.create_repos,
                use_ssh=args.ssh,
            )

        print("\n" + "=" * 60)
        print("All repositories published successfully.")
        print("=" * 60)
        return 0

    except PublishError as exc:
        print(f"\nERROR: {exc}")
        print("\n" + "=" * 60)
        print("Local setup is already complete. Fix the error and re-run:")
        print("  " + " ".join(sys.argv))
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
