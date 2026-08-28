# Future Integration Boundaries

This document records future integration points. No adapters are implemented in v0.1.

## Potential future integrations

- Obsidian: read/write compatible Markdown vault
- Notion: sync structured objects
- Gmail: capture source and action extraction
- Financial data providers: Finance domain
- Fitness integrations: Health domain
- Postgres: structured query backend
- Vector databases / embeddings: semantic search backend
- API server: programmatic interface
- Desktop AI client bridge (e.g., MCP): non-IDE client access
- Web/mobile application: user interface
- Voice capture: low-friction input channel
- External automation: Zapier, Make, etc.

## Constraint

The core object model must remain valid without any adapter. Adapters translate between Ethan OS representations and external systems.

## Adding a domain

1. Add domain entry to `ethan-os/config/domains.yaml`.
2. Add domain instructions to `ethan-os/instructions/domains/<domain>/`.
3. Add domain schemas to `ethan-os/schemas/domains/<domain>/`.
4. Add domain skills/workflows as needed.
5. Add domain folder to `ethan-life/domains/<domain>/`.

Core orchestration does not change.
