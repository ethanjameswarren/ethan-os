# Ethan OS Adapter Contract

This document defines the contract between Ethan OS and any AI client, IDE, desktop assistant, CLI, mobile app, or future system that wants to use it. Adapters live in this directory. Ethan OS itself must remain independent of any specific client.

## Purpose

An adapter translates between a particular client/runtime environment and the Ethan OS runtime. It is responsible for:

1. Loading the user's OS configuration.
2. Resolving the active Ethan OS package.
3. Running the Ethan OS runtime sequence.
4. Reading and writing user state through the configured storage backend.
5. Enforcing confirmation and safety policies on behalf of the user.

The core OS does not know which adapter is running it.

## Required adapter capabilities

| Capability | Description | Why it matters |
|---|---|---|
| `load_config` | Read the user's `.ethan-os.yaml` (or equivalent) from the active storage backend. | Lets the same OS run against local files, cloud folders, or a server. |
| `resolve_os` | Locate the active `ethan-os` package using `config.ethan_os.repository` or a built-in package reference. | Supports local development, packaged installs, and hosted backends. |
| `load_runtime_manifest` | Read `runtime/manifest.yaml` to discover entrypoints, loader order, schemas, domains, and workflows. | Clients do not have to reverse-engineer directory conventions. |
| `classify_intent` | Turn natural-language user input into an intent and optional domain by consulting `runtime/intent-router.md` and domain configuration. | Required when the client handles routing. Optional when delegated to the OS server. |
| `load_instructions` | Load core invariants, mandatory policies, configurable policies, global instructions, domain instructions, and workflow instructions in precedence order. | Preserves the OS policy stack regardless of client. |
| `load_context` | Assemble relevant context from the user's personal state without over-sharing. | Enforces the privacy principle of selective retrieval. |
| `run_workflow` | Execute the selected workflow, either by reasoning over Markdown instructions or by calling an `ethan-os-server` endpoint. | Keeps behavior in the OS layer. |
| `validate_object` | Validate generated/updated objects against `schemas/registry.yaml` before any write. | Prevents corrupt or incomplete state. |
| `write_state` | Persist validated changes to the configured storage backend, respecting confirmation thresholds. | Safe, versioned writes. |
| `confirm_or_notify` | Ask the user for confirmation on material changes and surface friction/reviews. | Keeps the human in control. |
| `report_result` | Return a concise summary of what was done and what needs attention. | Consistent UX across clients. |

## Optional capabilities

- `run_deterministic_script`: Invoke local Python scripts (e.g., `scripts/core/context_assembly.py`) when the adapter has a local runtime.
- `external_source_lookup`: Search the public web or external APIs for enrichment (music metadata, job postings, etc.). The adapter decides how to perform the lookup; OS skills describe what to retrieve, not which tool to call.
- `render_artifact`: Compile LaTeX, generate PDFs, export to Notion/Spotify/Google Calendar, etc.
- `schedule_proactive_review`: Surface nudges at bounded intervals without spamming.

## What the adapter must NOT do

- Embed OS instructions, schemas, or policies in client-specific prompt hacks.
- Invent provenance, skip validation, or silently overwrite history.
- Bypass the precedence stack (invariants → mandatory policies → configurable → global → domain → workflow → context).
- Expose all personal data to every capability; respect domain-scoped access.

## Storage backend abstraction

Adapters read the `storage` block from `.ethan-os.yaml` to determine where user state lives:

```yaml
ethan_os:
  repository: ../ethan-os
  version: 0.1.0
storage:
  backend: local_git
  path: ../ethan-life
```

Supported backend types are documented in `docs/architecture/storage-config.md`. The adapter implements the I/O for its backend.

## Tool-name neutrality

OS workflows and skills describe *what* to look up or *what* to execute, not the specific client tool name. For example:

- OS: "Look up the release on Discogs and cross-check with Hard Wax."
- Adapter: decides whether to use `web_search`/`webfetch`, a built-in browser, an API client, or a server-side lookup.

Adapters may provide a tool mapping file (e.g., `adapters/<client>/tools.yaml`) if the client requires explicit tool names.

## Adding a new adapter

1. Create `adapters/<client>/`.
2. Write an `ADAPTER.md` describing the client environment, capabilities, and any limitations.
3. Provide a `tools.yaml` mapping if the client requires named tool calls.
4. Keep client-specific prompts, rules, or bootstraps inside `adapters/<client>/`; do not add them to the core OS repo.

## See also

- `runtime/manifest.yaml` — machine-readable runtime contract.
- `docs/architecture/storage-config.md` — storage backend specification.
- `docs/architecture/instruction-precedence.md` — precedence rules adapters must enforce.
- `entrypoint/ethan-os.md` — canonical prompt-based entrypoint (one valid adapter implementation).
