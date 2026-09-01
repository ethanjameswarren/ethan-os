# Create Your Own OS from Ethan OS

Ethan OS is a reusable upstream foundation. You can create your own personal OS — for example, "John OS" — and evolve it independently while still adopting improvements from Ethan OS later.

This guide explains how to bootstrap a downstream OS and connect it to a private companion repository.

## What you get

A downstream OS repository contains:

- the full Ethan OS behavior layer (workflows, skills, schemas, validation, tests)
- your own OS identity in the README and config
- an `.os-upstream.yaml` manifest that records which Ethan OS version you started from
- an `upstream` git remote pointing back to Ethan OS so you can update later

Your private data lives in a separate companion repository (for example, `john-life`), not in your OS repo.

## Prerequisites

- Git installed.
- Python 3.10+ installed (for validation and scripts).
- A local copy of `ethan-os`.
- A place for your new OS repository, ideally as a sibling to your future companion repo.

## Recommended layout

```
~/git/
  ethan-os/          # upstream public project
  john-os/           # your downstream OS
  john-life/         # your private data
```

`ethan-os` and `john-os` are public. `john-life` is private.

## Before you begin: license and attribution

Ethan OS is licensed under the Apache License 2.0. When you create a downstream OS:

- The `LICENSE` file from Ethan OS is preserved in your downstream repo.
- The `NOTICE` file and upstream attribution are preserved.
- You choose your own project identity (for example, "John OS").
- You may add your own attribution notices in `NOTICE` without removing upstream notices.

See [project naming and attribution](../project-naming.md) for guidance on naming your downstream system.

## What happens during bootstrap

```
Ethan OS
   ↓  bootstrap
John OS
   ↓  customize
John OS evolves independently
   ↓  optional updates
Adopt compatible Ethan OS improvements
```

## Step 1: Bootstrap your OS

From inside `ethan-os`, run:

```powershell
python scripts/bootstrap-personal-os.py \
  --target-dir C:\git\john-os \
  --os-name "John OS" \
  --identifier john-os \
  --companion-repo john-life
```

Or on macOS/Linux:

```bash
python scripts/bootstrap-personal-os.py \
  --target-dir ~/git/john-os \
  --os-name "John OS" \
  --identifier john-os \
  --companion-repo john-life
```

What the script does:

1. Copies `ethan-os` into `john-os`.
2. Initializes a fresh git repository in `john-os`.
3. Adds `ethan-os` as the `upstream` remote.
4. Rewrites the README title and short description.
5. Updates `config/ethan-os.config.yaml` with `John OS` as the OS name.
6. Writes `.os-upstream.yaml` recording the exact upstream commit you started from.
7. Commits the initial downstream state.

The script does **not** copy any private `ethan-life` data. It also does not authenticate with or push to GitHub; publishing is a separate resumable step.

## Step 2: Authenticate and publish to GitHub

Do not paste a personal access token into a remote URL. Use one of the secure methods below, then publish with the provided script.

### Before you publish

Local Git must be able to push to GitHub. Being signed into your IDE, Devin, or Windsurf is not the same thing — those accounts are not available to the `git` command on this machine.

The recommended path for most users is the GitHub CLI browser flow:

```bash
# Install gh if you do not have it
winget install GitHub.cli        # Windows
brew install gh                  # macOS
sudo apt install gh              # Debian/Ubuntu

# Make git use the secure gh credential helper
gh auth setup-git
```

### Publish the repositories

Run the resumable publish script. If `gh` is installed and you are not logged in, it opens a browser window so you can click your GitHub account, then continues automatically.

On Windows:

```powershell
python scripts/publish-to-github.py \
  --os-dir C:\git\caitlin-os \
  --companion-dir C:\git\caitlin-life \
  --owner caitlin-github-username
```

On macOS or Linux:

```bash
python scripts/publish-to-github.py \
  --os-dir ~/git/caitlin-os \
  --companion-dir ~/git/caitlin-life \
  --owner caitlin-github-username
```

This will:

1. Check whether local Git can push to GitHub.
2. If `gh` is installed and you are not logged in, open `gh auth login --web` in a browser for you to click your account.
3. Create the `<identifier>-os` (public) and `<identifier>-life` (private) GitHub repositories if they do not exist.
4. Add an `origin` remote using `https://github.com/<owner>/<repo>.git` — never a PAT-in-URL.
5. Push both repositories to `origin`.

If `gh` is not installed, the script prints the exact install and login commands. Fix that and re-run the same command; it will resume from the publishing step. If you do not want to publish on GitHub, skip this step. The local repositories are already fully functional.

## Step 3: Set up the companion pointer

Create `john-life` as an empty private repository in your chosen location, for example `C:\git\john-life`.

Inside `john-life`, create a `.john-os.yaml` file pointing back to your OS:

```yaml
john_os:
  repository: ../john-os
  version: 0.1.1-beta
  domains:
    knowledge:
      enabled: true

# Storage backend for user state. The default is a sibling Git repository,
# but other backends (cloud folder, os_server, database) can be configured.
storage:
  backend: local_git
  path: ../john-life
```

The exact filename can be whatever your OS entrypoint expects. For Ethan OS-derived systems, this is typically `.<identifier>-os.yaml`. The runtime bootstrap in `john-os` will look for it.

## Step 4: Validate

From `john-os`, run:

```bash
python scripts/validate.py
```

This checks that all Markdown files have valid frontmatter and that schemas are consistent.

## Step 5: Customize

You can now change anything in `john-os`:

- Add new workflows in `workflows/`.
- Add new domains, schemas, and skills.
- Modify existing Ethan OS behavior to match your preferences.
- Update `docs/` with your own explanations.

The `.os-upstream.yaml` manifest ensures future updates know what you started from.

## What stays tied to Ethan OS

The following are managed upstream:

- core runtime behavior (`runtime/`, `entrypoint/`)
- schema contracts in `schemas/`
- validation scripts
- domain instructions unless you explicitly override them
- the `LICENSE` and `NOTICE` files (preserved and kept accurate)

You can still override any of these in your downstream repo; the update workflow will treat them as customizations and will not blindly overwrite them.

## License and attribution in your downstream OS

Your downstream repo keeps the Ethan OS `LICENSE` and `NOTICE`. The README uses your project name while still attributing Ethan OS as the upstream.

If you make material changes and redistribute the system, Apache-2.0 requires you to note modified files. Git history and conventional change tracking are used for this; you do not need to add a copyright header to every Markdown or YAML file.

## What does not get copied

- Any real `ethan-life` data.
- Private user fixtures or personal context.
- Git history from Ethan OS (you get a fresh history in `john-os`).

## Next

- [Updating your OS](updating-your-os.md) — adopt improvements from Ethan OS safely.
- [What is Ethan OS?](../concepts/what-is-ethan-os.md)
- [Core principles](../concepts/principles.md)
