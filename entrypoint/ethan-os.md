# Ethan OS Entrypoint

This is the canonical entrypoint for executing Ethan OS.

## Input

- user input (natural language)
- active working directory, expected to be an `ethan-life` repository
- `.ethan-os.yaml` in the active directory

## Repository routing rule

For any substantive Life OS request, the default execution order across repositories is:

1. `ethan-os` — determine the applicable domain, workflow, schemas, validation rules, and whether an `ethan-life` object must be created or updated.
2. `ethan-life` — create or update the canonical personal object/state.
3. `ethan-notion` — update Notion interface architecture/mappings only when the upstream state requires it.
4. Live Notion — apply changes to the rendered Notion workspace last, as a consequence of the upstream architecture.

Do not begin implementation or data changes in the Notion layer before the `ethan-os` and `ethan-life` implications are resolved.

Exception: If the user explicitly asks for a pure Notion infrastructure or presentation change (e.g., add a database property, fix a relation, update a database ID, change a mapping), work may start directly in `ethan-notion`.

## Runtime sequence

1. Locate `ethan-life/.ethan-os.yaml`.
2. Resolve the sibling `ethan-os` repository path.
3. Check version compatibility.
4. Load this entrypoint and core runtime documents.
5. Apply the repository routing rule.
   - For substantive Life OS requests, resolve the `ethan-os` domain/workflow implications and any required `ethan-life` state changes before touching `ethan-notion` or live Notion.
   - For pure Notion infrastructure/presentation requests, the routing rule permits starting directly in `ethan-notion`.
6. Classify intent from user input.
7. Determine domain (if any).
8. Select workflow.
9. Load required instructions in precedence order:
   - core invariants
   - mandatory policies
   - configurable policies
   - global instructions
   - domain instructions
   - workflow instructions
10. Load required context:
    - global context
    - domain context
    - object context (if referenced)
11. Load required skills.
12. Execute workflow.
13. Validate generated/updated objects against the schema registry.
14. Write to `ethan-life` (auto-execute for low-risk operations; confirm for material ambiguity or important semantic changes).
15. If the workflow or upstream state requires a Notion interface change, update the `ethan-notion` control plane and apply the change to live Notion only after the `ethan-life` state is resolved.
16. Return a concise result.

## Precedence

See `docs/architecture/instruction-precedence.md`. Context never overrides instructions. Mandatory policies cannot be overridden.

## Output

Concise summary of what was done, what objects were created or updated, and any items requiring user attention.
