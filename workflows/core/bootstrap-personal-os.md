# Workflow: bootstrap-personal-os

## Purpose

Create a new personal OS repository derived from the public `ethan-os` upstream.

## Triggers

- "Create my own OS called John OS."
- "Bootstrap a personal OS from Ethan OS."
- "I want to fork ethan-os for my own use."

## Steps

1. Ask for the OS display name and a short identifier if not provided.
2. Ask where the new repository should live (default sibling to `ethan-os`).
3. Determine the companion data repository name, default `<identifier>-life`.
4. Run `scripts/bootstrap-personal-os.py` with the collected inputs.
5. Confirm the new repository path, upstream commit, and companion repository name.
6. Provide next steps: create the companion repository, add its `.os.yaml` pointer, run validation.

## Output

- New downstream OS repository on disk.
- Git repository with `upstream` remote pointing to `ethan-os`.
- `.os-upstream.yaml` manifest.
- Customized README and `config/ethan-os.config.yaml`.

## Confirmation policy

Auto-execute once the target directory and identity are confirmed. Creating a new repository is low-risk and reversible.
