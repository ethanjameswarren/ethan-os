# Devin Adapter for Ethan OS

## Environment

Devin CLI / IDE with access to the local filesystem and the ability to load prompt context from a repository.

## Bootstrap

Before substantive Life OS work, the adapter loads `entrypoint/ethan-os.md` from the resolved `ethan-os` package.

A minimal Devin bootstrap rule outside the repo might look like:

```
Load <ethan-os-path>/entrypoint/ethan-os.md before substantive Ethan Life work.
```

That rule is a Devin-specific convenience, not part of Ethan OS. Store it in your Devin client configuration, not in this repo.

## Capabilities

- `load_config`: read `.ethan-os.yaml` from the active `ethan-life` directory.
- `resolve_os`: follow `ethan_os.repository` (relative or absolute path) to `ethan-os`.
- `load_instructions`: read Markdown files in precedence order using the Devin read tool.
- `run_deterministic_script`: execute Python scripts under `scripts/` when available.
- `external_source_lookup`: use `web_search` / `webfetch` for enrichment when a skill requests external sources.
- `write_state`: use the Devin file edit/write tools to update `ethan-life` after validation and confirmation.

## Tool mapping

If the OS skill asks for an "external source lookup," this adapter maps it to Devin's `web_search` and `webfetch` tools.

## Limitations

- Requires a local development environment.
- Not suitable for non-technical users who do not want an IDE or terminal.
