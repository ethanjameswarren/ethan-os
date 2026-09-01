# Workflow: bootstrap-personal-os

## Purpose

Create a new personal OS repository derived from the public `ethan-os` upstream.

## Triggers

- "Create my own OS called John OS."
- "Bootstrap a personal OS from Ethan OS."
- "I want to fork ethan-os for my own use."
- "I already have ethan-os and ethan-life and want to rebrand them to my name."

## Steps

1. If the person already has `ethan-os` and `ethan-life` and wants to rebrand them in place, stop and use `workflows/core/rename-personal-os.md` instead. Otherwise, ask for the person's name (e.g., "John").
2. Propose an OS display name (e.g., "John OS") and a short identifier (e.g., `john-os`) derived from the person's name, and ask for confirmation or a custom override.
3. Ask where the new repository should live (default sibling to `ethan-os`).
4. Determine the companion data repository name, default `<identifier>-life`.
5. Check for Python 3.10+. If it is not installed, explain the options and recommend one based on the person's comfort level:
   - **Beginner / not comfortable with the terminal:** install Python from the official python.org installer (Windows/macOS) or the Microsoft Store (Windows only). Make sure the "Add Python to PATH" option is selected.
   - **Comfortable with package managers:** install via the system package manager (`winget install Python.Python.3.12`, `brew install python`, `sudo apt install python3`).
   - **Already uses pyenv / asdf / version managers:** ask them to activate a Python 3.10+ version.
   - **Cannot install Python:** stop and explain that a Python interpreter is currently required for the bootstrap script.
6. Run `scripts/bootstrap-personal-os.py` with the collected inputs.
7. Confirm the new repository path, upstream commit, and companion repository name.
8. Provide next steps: create the companion repository, add its `.os.yaml` pointer, run validation.

## Output

- New downstream OS repository on disk.
- Git repository with `upstream` remote pointing to `ethan-os`.
- `.os-upstream.yaml` manifest.
- Customized README and `config/ethan-os.config.yaml`.

## Confirmation policy

Auto-execute once the target directory and identity are confirmed. Creating a new repository is low-risk and reversible.
