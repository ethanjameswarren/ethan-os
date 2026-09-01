#!/usr/bin/env python3
"""
Detect and recommend secure GitHub authentication for local Git.

This module never stores or prints credentials, tokens, or PATs. It only reports
whether the current environment is capable of pushing to GitHub and suggests the
next safe step.

Being signed into an IDE, Devin, or Windsurf does not count: those credentials
are not available to the local `git` executable. Only local Git/GitHub auth is
checked.
"""

import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd, cwd=None, check=False):
    """Run a command and return stdout/stderr without echoing secrets."""
    result = subprocess.run(
        list(cmd),
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{result.stderr.strip()}")
    return result.returncode, result.stdout, result.stderr


def gh_installed() -> bool:
    return shutil.which("gh") is not None


def gh_authenticated() -> tuple:
    """Return (ok, reason) using the GitHub CLI. Does not expose tokens."""
    if not gh_installed():
        return False, "GitHub CLI (gh) is not installed."
    code, _, _ = run(["gh", "auth", "status"])
    if code == 0:
        return True, "GitHub CLI is authenticated."
    return False, "GitHub CLI is installed but not logged in."


def ssh_authenticated() -> tuple:
    """Check whether an SSH key can reach github.com."""
    code, _, _ = run(
        ["ssh", "-o", "BatchMode=yes", "-o", "StrictHostKeyChecking=accept-new", "-T", "git@github.com"]
    )
    # ssh exits 1 even on successful auth because GitHub closes the connection.
    # We treat non-255 as likely success and rely on stderr if it is permission denied.
    if code == 255:
        return False, "SSH cannot connect to GitHub."
    return True, "SSH key appears to be accepted by GitHub."


class AuthState:
    AUTHENTICATED = "authenticated"
    NEEDS_AUTH = "needs_auth"
    UNKNOWN = "unknown"


def check_github_auth() -> tuple:
    """Return (state, message) describing local Git push capability."""
    if not shutil.which("git"):
        return AuthState.NEEDS_AUTH, "Git is not installed."

    gh_ok, gh_reason = gh_authenticated()
    if gh_ok:
        return AuthState.AUTHENTICATED, gh_reason

    ssh_ok, ssh_reason = ssh_authenticated()
    if ssh_ok:
        return AuthState.AUTHENTICATED, ssh_reason

    if gh_installed():
        return AuthState.NEEDS_AUTH, gh_reason

    return AuthState.NEEDS_AUTH, f"{gh_reason} {ssh_reason}"


def recommended_setup(technical_level: str = "beginner") -> str:
    """Return a single, safe, environment-appropriate recommendation."""
    if technical_level.lower() in ("beginner", "non-technical", "novice"):
        return (
            "Install the GitHub CLI and log in with the device flow:\n"
            "  1. Install `gh':\n"
            "       Windows: winget install GitHub.cli\n"
            "       macOS:   brew install gh\n"
            "       Linux:   sudo apt install gh  (or use the official package)\n"
            "  2. Run: gh auth login\n"
            "     Choose 'GitHub.com' and 'HTTPS'.\n"
            "     When asked, choose to authenticate with a web browser or one-time code.\n"
            "  3. Run: gh auth setup-git\n"
            "     This makes `gh' the secure credential helper for `git push' -- no PAT required.\n"
            "  4. Re-run the publish step."
        )

    return (
        "Choose one of these secure, token-free methods and then re-run the publish step:\n"
        "  - GitHub CLI:        gh auth login && gh auth setup-git\n"
        "  - SSH key:           ssh-keygen -t ed25519 -C 'you@example.com' and add the public key to GitHub\n"
        "  - Git Credential Manager: https://github.com/GitCredentialManager/git-credential-manager\n"
        "Do not use a PAT embedded in a remote URL."
    )


def main():
    state, message = check_github_auth()
    print(message)
    if state == AuthState.AUTHENTICATED:
        print("\nLocal Git is ready to push to GitHub.")
        return 0
    print("\n" + recommended_setup("beginner"))
    return 1


if __name__ == "__main__":
    sys.exit(main())
