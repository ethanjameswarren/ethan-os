# Architecture Overview

Ethan OS is split into two repositories:

- `ethan-os`: behavior, intelligence, schemas, workflows, skills, policies, validation, documentation, demo fixtures.
- `ethan-life`: personal information and generated artifacts.

## Core principle

> Ethan OS owns behavior. Ethan Life owns information.

## High-level flow

1. User provides input in `ethan-life` (natural language prompt/chat).
2. AI locates `ethan-life/.ethan-os.yaml` and resolves the sibling `ethan-os` repository.
3. AI loads the canonical entrypoint in `ethan-os/entrypoint/ethan-os.md`.
4. AI classifies intent, determines domain, selects workflow.
5. AI loads required instructions, policies, context, and skills in precedence order.
6. AI executes workflow.
7. AI validates generated objects against the schema registry and checks that every internal relationship target resolves.
8. AI writes validated objects back to `ethan-life`; uncaptured external inputs remain provenance references rather than internal links.
9. AI returns a concise result.

## Design goals

- High capture, low maintenance, useful synthesis.
- Portable: plain Markdown and YAML; no required database, app, or external service.
- Extensible: domains and adapters can be added later without redesigning the core.
- Privacy: public/private boundary is enforced by repository separation.
