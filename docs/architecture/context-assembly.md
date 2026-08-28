# Context Assembly

## Purpose

Selectively load the personal state needed for a workflow, based on the user's intent and the desired depth. Avoid giant user profiles and unnecessary sensitive-domain access.

## Contract

- **Request**: `core.context-request` (intent, domains, entity refs, time horizon, desired depth, excluded domains).
- **Bundle**: `core.context-bundle` (current state, relevant history, related knowledge, active constraints, preferences, provenance).

## Goals

- Retrieve only what is relevant.
- Preserve provenance for every loaded item.
- Keep sensitive domains private by default.
- Make the assembled context explainable.
- Avoid overloading prompts.

## Privacy and permissions

- Domains outside the request's scope are not loaded unless the user explicitly asks or the workflow requires them.
- `avoid_domains` blocks domains even if the workflow normally uses them.
- Future permission controls can gate domain access by client or integration.

## Relationship to other horizontal services

- **Universal Personal Retrieval** may answer broad questions using the same selection logic, but as a query path rather than a workflow input.
- **Cross-Domain Reasoning** uses context bundles to find and surface connections across domains.
- **Review Orchestrator** uses context assembly to decide which reviews are relevant.

## Status

The contract is in place. Smart retrieval, semantic search, and automated permission enforcement are not yet implemented.
