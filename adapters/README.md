# Adapters

This directory contains client-specific adapters that let AI clients, IDEs, desktop assistants, CLIs, mobile apps, and future interfaces run Ethan OS without polluting the core OS with tool-specific logic.

Each adapter implements the [adapter contract](adapter-contract.md):

- Load user configuration and resolve the active OS package.
- Follow the runtime sequence described in `entrypoint/ethan-os.md`.
- Enforce instruction precedence, validation, confirmation, and privacy policies.
- Read and write user state through the configured storage backend.

Adapters may be prompt-only, script-based, or server-backed, depending on the client environment.

## Current adapters

- `devin/` — Devin CLI/IDE adapter.
- `windsurf/` — Windsurf / Cursor / VS Code IDE adapter.
- `mcp-server/` — Model Context Protocol server for Claude Desktop and other MCP clients.
- `cli/` — Command-line adapter for local use.
- `chatgpt/` — ChatGPT custom GPT / actions adapter pattern.

## Design rules

1. Keep client-specific prompts, rules, and bootstraps inside the adapter directory.
2. Do not reference client tool names (e.g., `web_search`, `read_file`, `cursor`) in core OS workflows or skills.
3. Use the runtime manifest and storage-config abstraction so adapters do not hard-code filesystem layouts.
