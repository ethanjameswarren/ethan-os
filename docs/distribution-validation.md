# Distribution Validation

Status: **validated**

These capabilities were validated end-to-end on clean machines. They are not theoretical or untested roadmap items.

| Capability | Status | Evidence |
|---|---|---|
| Windows bootstrap | validated | Bootstrapped `John OS` from the public `ethan-os` repository on a clean Windows environment. |
| macOS bootstrap | validated | Bootstrapped a downstream OS from `ethan-os` on macOS. |
| GitHub authentication / publishing | validated | `scripts/test-bootstrap-auth.py` exercises the auth check and publishing resumption path; browser-based `gh auth login` confirmed as the recommended flow. |
| Downstream repository creation | validated | Bootstrap produces a working git repository with `upstream` remote pointing to `ethan-os`, personalized README, and `config/ethan-os.config.yaml` identity section. |
| Upstream → downstream updates | validated | `scripts/update-from-upstream.py --check` and `--apply` import upstream improvements without `git pull origin master`. |
| Three-way selective merge behavior | validated | Safe updates/additions/removals are applied; conflicts are flagged for human review; downstream-only files are untouched. |
| Downstream customization preservation | validated | User changes in downstream files are preserved when upstream also changes them (flagged as conflicts, not overwritten). |
| License / upstream provenance + downstream personalization | validated | `scripts/test-identity-personalization.py` confirms `LICENSE`, `NOTICE`, `.os-upstream.yaml`, and the `framework` section remain unchanged while user-facing `Ethan` / `Ethan OS` / `ethan-life` text is rewritten to the downstream identity. John identity test included. |

## Validation commands

```bash
python scripts/test-bootstrap-auth.py
python scripts/test-identity-personalization.py
python scripts/bootstrap-personal-os.py --target-dir /path/to/john-os --os-name "John OS" --identifier john-os
```

After bootstrap, the downstream repository should:

- Show `# John OS` in `README.md`.
- Still attribute the upstream framework (`Ethan OS` / `ethan-os`) in `README.md`, `.os-upstream.yaml`, `LICENSE`, and `NOTICE`.
- Contain `config/ethan-os.config.yaml` with a protected `framework` section and a personalized `identity` section.
- Have `upstream` remote set to the canonical `ethan-os` repository, not `origin`.

## What this unlocks

A person can start from the public `ethan-os` framework, create their own independent OS (e.g., `John OS`), publish it to GitHub, and continue receiving framework improvements without maintaining a dumb fork.
