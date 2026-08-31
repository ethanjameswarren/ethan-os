# ChatGPT Adapter Pattern for Ethan OS

## Environment

ChatGPT Web, ChatGPT Desktop, or a custom GPT that can call external actions/APIs.

## Challenge

ChatGPT cannot directly read local files or edit a user's filesystem. Therefore, a ChatGPT adapter requires a backend companion:

1. An `ethan-os-server` or cloud-hosted service owns the OS runtime and storage.
2. ChatGPT calls the server's tools/actions to read context and write changes.

## Pattern: custom GPT actions

Expose a small set of actions to the GPT:

- `GET /context?query=...&domains=...` — retrieve a scoped context bundle.
- `POST /run` — run a workflow and return proposed changes.
- `POST /validate` — validate proposed objects.
- `POST /write` — apply validated changes (with user confirmation surfaced by the GPT).

## Capabilities

- `load_config`, `resolve_os`, `load_instructions`, `run_workflow`, `validate_object`, `write_state` are server-side.
- The GPT's only client-specific behavior is calling the action endpoints and rendering results.

## Non-technical path

A hosted "Ethan OS Cloud" service with a ChatGPT action is the simplest experience for non-technical users: they chat with ChatGPT and the service handles storage, versioning, and safety.
