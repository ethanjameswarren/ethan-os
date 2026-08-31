# Storage Backend Configuration

This document specifies how an Ethan OS-derived system declares where user state (`ethan-life`) lives. It is part of the adapter contract and keeps the core OS independent of any particular storage mechanism.

## Purpose

The same Ethan OS package should run against:

- a local Git repository on a developer's machine,
- a local folder without Git,
- a cloud-backed folder (Google Drive, Dropbox, OneDrive, iCloud),
- a hosted object/document store,
- an `ethan-os-server` that manages persistence.

Adapters implement the I/O for each backend type. The OS layer only reads the storage declaration.

## Configuration location

Storage is declared in the user's OS config file, conventionally named `.<os-identifier>-os.yaml`. For Ethan OS itself this is `.ethan-os.yaml`.

## Schema

```yaml
ethan_os:
  repository: ../ethan-os        # path or URL to the active OS package
  version: 0.1.1-beta            # expected OS schema/runtime version
  # ... other OS-level settings

storage:
  backend: local_git              # required; see supported backends below
  path: ../ethan-life           # required for filesystem backends; absolute or relative to config file
  # Optional backend-specific settings:
  options:
    auto_commit: true             # for local_git
    branch: main
    remote: origin
```

### Supported backends

| Backend | Description | Use case |
|---|---|---|
| `local_git` | A Git repository on the local filesystem. | Developer power users; full version history. |
| `local_folder` | A plain folder on the local filesystem. | Quick testing; no version history. |
| `cloud_folder` | A folder synced by a cloud provider (Google Drive, Dropbox, OneDrive, iCloud). | Non-technical users who want files they can see. |
| `os_server` | An `ethan-os-server` endpoint manages persistence. | Web/mobile app, hosted service, or multi-device use. |
| `database` | A structured store (SQLite, Postgres, etc.). | Future backends; not required for file-based state. |

### Backend-specific fields

#### `local_git`

- `path` (required): path to the companion repository root.
- `options.auto_commit` (optional, default `true`): commit writes automatically.
- `options.branch` (optional, default `main`): branch to use.

#### `local_folder`

- `path` (required): path to the companion folder root.

#### `cloud_folder`

- `path` (required): absolute or provider-relative path to the synced folder.
- `options.provider` (optional): `google_drive`, `dropbox`, `onedrive`, `icloud`.

The adapter is responsible for translating this into the provider's API or local sync client.

#### `os_server`

- `url` (required): base URL of the server, e.g., `http://localhost:8080` or `https://my-os.example.com`.
- `options.api_key_env` (optional): environment variable holding an API key.

The server is the source of truth for persistence and versioning.

## Backward compatibility

If `storage` is absent, adapters default to:

```yaml
storage:
  backend: local_git
  path: <sibling ethan-life>
```

This preserves today's default layout where `.ethan-os.yaml` sits in `ethan-life` and points to a sibling `ethan-os`.

## Adapter responsibilities

For any backend, the adapter must implement:

- `read_object(path)`: read a file/object from storage.
- `write_object(path, content)`: write a file/object to storage.
- `list_objects(pattern)`: list files/objects (e.g., `domains/knowledge/**/*.md`).
- `commit_or_sync(changes, message)`: persist changes in a backend-appropriate way (Git commit, sync, API call).
- `history(path)`: return prior versions if supported.

Adapters must still validate objects against `schemas/registry.yaml` before writing.

## Migration between backends

User state is plain Markdown/YAML. Migration is generally a file copy. Adapters should support an export/import helper that preserves:

- file paths,
- frontmatter and IDs,
- provenance,
- and optionally Git history (via clone/push).

## Relationship to the runtime

The runtime resolves the OS package from `ethan_os.repository`. It then loads `schemas/`, `workflows/`, and `instructions/` from that package. The adapter resolves the user's state using `storage`. This split keeps OS behavior portable across storage backends.

## See also

- `adapters/adapter-contract.md`
- `runtime/resolver.md`
- `runtime/manifest.yaml`
