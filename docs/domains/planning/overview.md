# Planning Domain

The third fully implemented domain in Ethan OS.

## Purpose

Capture goals, break them into projects and tasks, track status, and surface what to do next.

## v0.1 objects

- Goal (`planning.goal`)
- Project (`planning.project`)
- Task (`planning.task`)

## Object flow

```
Goal → Project → Milestones → Tasks
Goal → Task (directly, for small goals)
```

## Design principles

- A goal without success criteria cannot be meaningfully reviewed later — ask for them.
- Not every goal needs a project; only create one when multiple coordinated steps are required.
- Every project and task links back to the goal it serves, unless intentionally standalone.
- Review surfaces findings; it never silently changes status. Status changes go through `workflows/core/revise.md`.
