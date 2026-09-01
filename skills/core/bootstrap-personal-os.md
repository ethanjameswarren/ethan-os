# Skill: bootstrap-personal-os

## Purpose

Create a personalized downstream OS repository from the public `ethan-os` upstream, preserving the upstream project identity while giving the new OS its own name and companion repository. Local bootstrap and GitHub publishing are separate steps.

## Input

- Target directory for the new downstream repository.
- OS display name (e.g., "John OS").
- Identifier (e.g., `john-os`).
- Optional companion repository name (defaults to `<identifier>-life`).
- Optional upstream repo path or URL (defaults to the repository containing this script).
- Optional GitHub owner/organization, only asked if the user chooses to publish.

## Output

- A new git repository containing a copy of `ethan-os`.
- A downstream README with the new OS identity and attribution to `ethan-os`.
- `config/ethan-os.config.yaml` carrying both a protected `framework` section (`ethan-os` / `Ethan OS`) and a personalized `identity` section (owner, `os_name`, `os_repo`, `life_repo`).
- `.os-upstream.yaml` recording the upstream project, version, commit, and install date.
- User-facing `Ethan` / `Ethan OS` wording in personalizable docs, workflows, and skills rewritten to the new owner/OS using `scripts/personalize.py`.
- `upstream` remote pointing to `ethan-os` and `push.default` set to `nothing` so nothing can be pushed upstream by accident.
- Optionally, published GitHub repositories and `origin` remotes after the user authenticates.

## Rules

1. Do not copy private `ethan-life` data or any real personal data.
2. Do not blindly replace every occurrence of "Ethan" or "ethan-os".
3. Preserve upstream project attribution in the README, `NOTICE`, `LICENSE`, `.os-upstream.yaml`, and `config/ethan-os.config.yaml` `framework` section.
4. Record the exact upstream commit so future updates can compare safely.
5. Keep demo fixtures; they are public, generic, and used by tests.
6. Never store, print, or suggest embedding a GitHub PAT or token in a remote URL, repository file, or log.
7. Separate local bootstrap from authenticated publishing. If GitHub authentication is missing, stop after the local setup is complete and give the user the exact resumption command.
8. Use `scripts/personalize.py` to apply the downstream identity layer; protected provenance files/fields must never be rewritten.
