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
/Ethan/ethan-os
/Ethan/ethan-life
```

or

```
c:\Users\ethan\git\ethan-os
c:\Users\ethan\git\ethan-life
```

## Version compatibility

`.ethan-os.yaml` declares:

```yaml
ethan_os:
  version: 1.0.0
```

The runtime checks that `ethan-os` supports this version.

Rules:

- `ethan-os` may support multiple `ethan-life` schema versions.
- If `ethan-life` version is newer than `ethan-os` supports, stop and inform user.
- If older, attempt to run if backwards compatibility is maintained.

## Output

- resolved `ethan-os` path
- confirmed compatible version
