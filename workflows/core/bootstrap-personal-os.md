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
2. Propose an OS display name (e.g., "John OS") and a short identifier (e.g., `john-os`) derived from the person’s name, and ask for confirmation or a custom override.
3. Ask where the new repository should live (default sibling to `ethan-os`).
4. Determine the companion data repository name, default `<identifier>-life`.
5. Ask for the GitHub owner/organization (e.g., `john-doe`). Record `none` if they are not using GitHub or want to set remotes manually.
6. Check for Python 3.10+. If it is not installed, explain the options and recommend one based on the person's comfort level:
   - **Beginner / not comfortable with the terminal:** install Python from the official python.org installer (Windows/macOS) or the Microsoft Store (Windows only). Make sure the "Add Python to PATH" option is selected.
   - **Comfortable with package managers:** install via the system package manager (`winget install Python.Python.3.12`, `brew install python`, `sudo apt install python3`).
   - **Already uses pyenv / asdf / version managers:** ask them to activate a Python 3.10+ version.
   - **Cannot install Python:** stop and explain that a Python interpreter is currently required for the bootstrap script.
7. Run `scripts/bootstrap-personal-os.py` with the collected inputs. If a GitHub owner was given, pass `--github-owner <owner>` so the new OS's `origin` remote points to `https://github.com/<owner>/<identifier>-os.git` and `git push` cannot accidentally target `ethan-os`.
8. Confirm the new repository path, upstream commit, companion repository name, and origin URL if applicable.
9. Provide next steps: create the GitHub repositories (if not already created), add the companion `.os.yaml` pointer, push to `origin`, run validation.

## Output

- New downstream OS repository on disk.
- Git repository with `upstream` remote pointing to `ethan-os`.
- `origin` remote pointing to the person's GitHub repo (if owner was provided), otherwise `push.default` set to `nothing` for safety.
- `.os-upstream.yaml` manifest.
- Customized README and `config/ethan-os.config.yaml`.

## Confirmation policy

Auto-execute once the target directory and identity are confirmed. Creating a new repository is low-risk and reversible.
