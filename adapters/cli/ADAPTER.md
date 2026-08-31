# CLI Adapter for Ethan OS

## Environment

A terminal or shell script on a machine with Python and optional Git. Best for power users and automation.

## Usage pattern

```bash
ethan-os run "What should I work on today?" --life-root ~/git/ethan-life --os-root ~/git/ethan-os
ethan-os validate --life-root ~/git/ethan-life --os-root ~/git/ethan-os
ethan-os workflow start-reading --input "I'm starting Dune" --life-root ~/git/ethan-life
```

## Capabilities

- `load_config`: read `.ethan-os.yaml`.
- `resolve_os`: accept `--os-root` or resolve via config.
- `load_instructions`, `run_workflow`, `validate_object`, `write_state`: can be implemented as Python wrappers around existing scripts or a future `ethan-os-server`.
- `confirm_or_notify`: prompt in the terminal for material changes.

## Notes

The CLI adapter is a thin wrapper. Heavy lifting should be delegated to the runtime scripts or an MCP/API server so behavior stays in the OS layer.
