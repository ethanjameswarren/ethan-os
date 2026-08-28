# Ethan OS

Ethan OS is a modular personal AI operating system. It owns behavior: instructions, schemas, skills, workflows, policies, and validation.

`ethan-life` is the private repository that owns information: captures, sources, ideas, summaries, reviews, and personal context.

## Quick start

1. Ensure `ethan-os` and `ethan-life` are sibling directories.
2. Capture something in `ethan-life` or run a workflow from `ethan-os/entrypoint/ethan-os.md`.
3. The runtime bootstraps from `ethan-life/.ethan-os.yaml`, loads `ethan-os`, classifies intent, selects a workflow, and executes.

## Repository separation

- `ethan-os` is safe to make public. It contains generic logic, fake demo fixtures, schemas, workflows, skills, policies, documentation, and tests.
- `ethan-life` must remain private. It contains all real personal data.

## v0.1 interaction intents

- capture
- process learning notes
- start reading
- continue reading
- discuss reading
- finish reading
- reading status
- review reading
- update reading profile
- manage book library
- book recommendation
- ask / retrieve
- summarize
- review
- revise
- status

## Documentation

See `docs/architecture/` for the full architecture.
