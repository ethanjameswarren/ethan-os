# Runtime Bootstrap

## Purpose

Locate `ethan-life/.ethan-os.yaml` and resolve the sibling `ethan-os` repository.

## Steps

1. Confirm the active working directory contains `.ethan-os.yaml`.
2. Read `.ethan-os.yaml`.
3. Extract `ethan_os.repository` path.
4. If relative, resolve relative to `ethan-life` root.
5. Verify `ethan-os/entrypoint/ethan-os.md` exists.
6. Load the canonical entrypoint.

## Error conditions

- Missing `.ethan-os.yaml`: stop and inform user.
- Missing `ethan-os` repository: stop and inform user.
- Missing entrypoint: stop and inform user.

## No duplicated logic

This document only describes bootstrap mechanics. All behavior lives in `ethan-os`.
