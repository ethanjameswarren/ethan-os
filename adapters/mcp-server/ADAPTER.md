# MCP Server Adapter for Ethan OS

## Environment

A local or hosted server that exposes Ethan OS capabilities through the Model Context Protocol (MCP) or a similar tool-calling API. Clients such as Claude Desktop, ChatGPT Desktop (via plugins), or any MCP-compatible host can connect to it.

## Why this adapter matters

The MCP server becomes the canonical runtime host. AI clients do not need to read the entire OS repo or edit files directly. They call tools exposed by the server, which enforces OS policies and writes to storage safely.

## Example tools

- `ethan_os_resolve_request(intent: string)` — classify intent, load instructions, return the workflow to run.
- `ethan_os_assemble_context(request: object)` — return a privacy-scoped context bundle.
- `ethan_os_run_workflow(workflow_id: string, inputs: object)` — run a workflow and return proposed changes.
- `ethan_os_validate_object(object: object)` — validate against `schemas/registry.yaml`.
- `ethan_os_write_state(dry_run: bool, changes: object)` — preview or apply validated writes.

## Capabilities

- `load_config`, `resolve_os`, `load_instructions`, `run_workflow`, `validate_object`, `write_state` are all handled server-side.
- `confirm_or_notify`: the server returns a proposed-change payload; the client presents it to the user for approval.
- `external_source_lookup`: server may use built-in API clients or delegate to the client.

## Deployment options

- **Local**: runs on the user's machine, keeps data local.
- **Self-hosted**: runs on a private server, supports multiple devices.
- **Hosted service**: easiest for non-technical users, but requires trust in the host.

## Status

Conceptual adapter. See `docs/ROADMAP.md` "Desktop AI Client Access" for planned work.
