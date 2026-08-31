# Windsurf / Cursor / VS Code IDE Adapter for Ethan OS

## Environment

An IDE with AI chat, memory/rules support, and file-system access. Examples: Windsurf, Cursor, GitHub Copilot Chat, VS Code with an agent extension.

## Bootstrap

The IDE's global or workspace rules can load `entrypoint/ethan-os.md` at the start of a session. Example Windsurf global-rule snippet:

```markdown
# Ethan OS bootstrap
Load `${workspaceFolder:ethan-os}/entrypoint/ethan-os.md` before substantive Ethan Life work.
```

Store these rules in IDE-specific settings, not in the `ethan-os` repo.

## Capabilities

- `load_config`: read `.ethan-os.yaml` from the active workspace or from a configured companion directory.
- `resolve_os`: locate the `ethan-os` repository by path or package reference.
- `load_instructions`: read Markdown files using the IDE's file/context tools.
- `run_deterministic_script`: run Python scripts in the IDE's integrated terminal when appropriate.
- `write_state`: use the IDE's file edit/write capabilities after validation and confirmation.

## Tool mapping

External lookups should be delegated to the IDE's web-search capability or to a local Ethan OS server if one is running.

## Notes

- This adapter is functionally similar to the Devin adapter because both assume a local repo + file-aware AI assistant.
- For non-technical users, prefer the `mcp-server/` or a future web/mobile adapter instead of an IDE.
