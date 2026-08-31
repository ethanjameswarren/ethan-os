# Repository / Version Resolver

## Purpose

Resolve `ethan-os` location and verify compatibility.

## Repository resolution

`.ethan-os.yaml` declares:

```yaml
ethan_os:
  repository: ../ethan-os
```

Relative paths are resolved from `ethan-life` root. Absolute paths are accepted.

Sibling semantics are preferred. Example layouts:

```
/Users/example/ethan-os
/Users/example/ethan-life
```

or

```
c:\Users\example\git\ethan-os
c:\Users\example\git\ethan-life
```

## Version compatibility

`.ethan-os.yaml` declares:

```yaml
ethan_os:
  version: 0.1.1-beta
```

The runtime checks that `ethan-os` supports this version.

Rules:

- `ethan-os` may support multiple `ethan-life` schema versions.
- If `ethan-life` version is newer than `ethan-os` supports, stop and inform user.
- If older, attempt to run if backwards compatibility is maintained.

## Storage backend

`.ethan-os.yaml` may also declare a `storage` block so adapters know where user state lives and how to persist it. If absent, the default is the sibling `ethan-life` Git repository. See `docs/architecture/storage-config.md`.

```yaml
ethan_os:
  repository: ../ethan-os
  version: 0.1.1-beta
storage:
  backend: local_git
  path: ../ethan-life
```

## Output

- resolved `ethan-os` path
- confirmed compatible version
- resolved storage backend and user-state root
