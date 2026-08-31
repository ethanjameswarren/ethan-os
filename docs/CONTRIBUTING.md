# Contributing to Ethan OS

Ethan OS is designed to be a portable, user-owned personal AI operating system. This guide helps contributors keep it that way.

## Core design constraints

### 1. Keep the core OS client-agnostic

The core OS — `entrypoint/`, `runtime/`, `instructions/`, `workflows/`, `skills/`, `schemas/`, `docs/concepts/`, and `docs/architecture/` — must not depend on a specific AI client, IDE, agent framework, or model provider.

- Use generic terms like "AI client" or "adapter."
- Do not name Devin, Cursor, Windsurf, ChatGPT, Claude, OpenAI, Anthropic, or any other product in core OS logic, instructions, or workflows.
- Do not check in `.cursorrules`, `.windsurfrules`, `.devin/`, `.claude/`, `.codeium/`, `environment.yaml`, or similar client-specific configuration at the repository root.

Client-specific prompts, bootstrap rules, tool mappings, and integrations belong in `adapters/`.

### 2. Use the adapter contract

Any new integration with an AI client or external service should follow `adapters/adapter-contract.md`. If you add a capability that requires client-specific behavior, also add or update the relevant adapter documentation in `adapters/<client>/`.

### 3. Prefer declarative, machine-readable configuration

- Add schemas to `schemas/`.
- Add workflows to `workflows/`.
- Add skills to `skills/`.
- Register domain-level metadata in `config/domains.yaml`.
- If the runtime needs to discover something programmatically, prefer adding it to `runtime/manifest.yaml` over hard-coding directory traversal in clients.

### 4. Keep `ethan-os` behavior separate from `ethan-life` state

- Never store real personal data in the `ethan-os` repository.
- Never reference absolute paths to a user's private files.
- Scripts that read `ethan-life` should accept a configurable root (e.g., `--life-root`) rather than assuming a sibling directory.

### 5. Maintain portability of state

New features should not lock user state into a proprietary format or a single client. Plain Markdown + YAML remains the canonical interchange format. Database, vector, or cloud backends are optional adapters, not requirements.

### 6. Validate changes

Run `python scripts/validate.py` before committing. If your change touches context assembly, retrieval, or cross-domain reasoning, run the relevant test scripts in `scripts/`.

## Where to put things

| What | Where |
|---|---|
| Core OS behavior | `entrypoint/`, `runtime/`, `instructions/`, `workflows/`, `skills/`, `schemas/` |
| Domain configuration | `config/domains.yaml` |
| Client-specific adapters | `adapters/<client>/` |
| External service integrations | `integrations/` or `adapters/integrations/` (not core OS) |
| Docs | `docs/` |
| Deterministic tests and helpers | `scripts/` |

## Questions?

Open an issue or refer to:

- `docs/concepts/principles.md`
- `docs/architecture/overview.md`
- `adapters/adapter-contract.md`
- `runtime/manifest.yaml`
