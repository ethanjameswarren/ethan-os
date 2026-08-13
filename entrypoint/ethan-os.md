# Ethan OS Entrypoint

This is the canonical entrypoint for executing Ethan OS.

## Input

- user input (natural language)
- active working directory, expected to be an `ethan-life` repository
- `.ethan-os.yaml` in the active directory

## Runtime sequence

1. Locate `ethan-life/.ethan-os.yaml`.
2. Resolve the sibling `ethan-os` repository path.
3. Check version compatibility.
4. Load this entrypoint and core runtime documents.
5. Classify intent from user input.
6. Determine domain (if any).
7. Select workflow.
8. Load required instructions in precedence order:
   - core invariants
   - mandatory policies
   - configurable policies
   - global instructions
   - domain instructions
   - workflow instructions
9. Load required context:
   - global context
   - domain context
   - object context (if referenced)
10. Load required skills.
11. Execute workflow.
12. Validate generated/updated objects against the schema registry.
13. Write to `ethan-life` (auto-execute for low-risk operations; confirm for material ambiguity or important semantic changes).
14. Return a concise result.

## Precedence

See `docs/architecture/instruction-precedence.md`. Context never overrides instructions. Mandatory policies cannot be overridden.

## Output

Concise summary of what was done, what objects were created or updated, and any items requiring user attention.
