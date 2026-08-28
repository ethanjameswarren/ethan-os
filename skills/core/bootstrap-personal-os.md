# Skill: bootstrap-personal-os

## Purpose

Create a personalized downstream OS repository from the public `ethan-os` upstream, preserving the upstream project identity while giving the new OS its own name and companion repository.

## Input

- Target directory for the new downstream repository.
- OS display name (e.g., "John OS").
- Identifier (e.g., `john-os`).
- Optional companion repository name (defaults to `<identifier>-life`).
- Optional upstream repo path or URL (defaults to the repository containing this script).

## Output

- A new git repository containing a copy of `ethan-os`.
- A downstream README with the new OS identity and attribution to `ethan-os`.
- `config/ethan-os.config.yaml` updated with the new OS name.
- `.os-upstream.yaml` recording the upstream project, version, commit, and install date.
- Upstream set as a git remote so future updates can be fetched.

## Rules

1. Do not copy private `ethan-life` data or any real personal data.
2. Do not blindly replace every occurrence of "Ethan" or "ethan-os".
3. Preserve upstream project attribution in the README and manifest.
4. Record the exact upstream commit so future updates can compare safely.
5. Keep demo fixtures; they are public, generic, and used by tests.
