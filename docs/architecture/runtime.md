# Runtime / Bootstrap Architecture

## Bootstrap in `ethan-life`

`ethan-life/.ethan-os.yaml` is the only behavioral pointer in `ethan-life`.

It contains:

- `ethan_os.repository`: path to the sibling `ethan-os` repository
- `ethan_os.version`: compatible Ethan OS version
- `ethan_os.domains`: enabled domains and their configuration

## Canonical entrypoint

`ethan-os/entrypoint/ethan-os.md` is the single place execution begins.

## Runtime sequence

```
User input
→ locate .ethan-os.yaml
→ resolve ethan-os repository
→ check version compatibility
→ load canonical entrypoint
→ classify intent
→ determine domain
→ select workflow
→ load instructions / policies / context / skills
→ execute workflow
→ validate objects
→ write to ethan-life
→ return concise result
```

## Runtime documents

- `runtime/bootstrap.md`: how to find `.ethan-os.yaml` and resolve `ethan-os`
- `runtime/resolver.md`: repository path resolution and version compatibility
- `runtime/loader.md`: instruction precedence and context assembly
- `runtime/intent-router.md`: intent classification and workflow selection
- `runtime/validator.md`: deterministic validation against schema registry

## Separation of concerns

`ethan-life` contains no behavioral logic. All behavior lives in `ethan-os`.
