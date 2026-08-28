# Core Principles

These principles guide how Ethan OS is designed and how it behaves.

## Conversation over forms

The user speaks or writes naturally. The system extracts structure behind the scenes. It does not force the user to fill out fields, pick from rigid categories, or confirm every minor detail.

## The user talks; the OS manages structure

The user's job is to express what matters. The OS's job is to organize, connect, preserve provenance, and surface useful information later. Reading should not feel like homework; planning should not feel like ticketing; logging should not feel like accounting.

## One canonical source of truth

For any piece of information, there is exactly one place that owns it. Reading progress lives in reading state. Book metadata lives in the source object. Personal context lives in `ethan-life`. Downstream systems like Notion or Spotify are projections, never authorities.

## Behavior separated from personal data

`ethan-os` owns how the system works. `ethan-life` owns what the system knows about you. The public repo never contains private information; the private repo never contains behavior logic.

## Inspectable, portable storage

Canonical state is stored as plain Markdown and YAML. You can read it, version it, move it, and inspect it without a special client. There is no hidden database or proprietary format.

## Provenance matters

The system distinguishes:

- what the user said,
- what the source claims,
- what the AI inferred or synthesized.

These are never collapsed into a single indistinguishable summary.

## Minimal-change behavior

The system changes only what is needed. It does not silently overwrite useful history. It does not promote every fleeting observation to a durable object. It asks before material semantic changes.

## Human control

The user can override, skip, pause, archive, or delete. They can say "not now," "I don't care about remembering this," or "this one is important." Defaults are conservative; explicit user intent wins.

## Integrations are projections

External systems display or extend `ethan-life` data; they do not own it. If Notion or Spotify disagree with `ethan-life`, `ethan-life` wins.

## Extend existing architecture rather than duplicate it

New capabilities reuse existing objects, relationships, and workflows. A book is a source; a session insight is like a capture; a retention item references an idea. Avoiding parallel silos keeps the system coherent.

## Progressive disclosure for complexity

The system should be simple in normal use and powerful when needed. A casual user should not see schemas, routing tables, or validation internals. A builder should be able to drill down into all of them.

## Do not fabricate certainty or provenance

The system does not claim to have read text it has not retrieved. It does not claim a preference is known without evidence. It does not invent sources, quotes, or history.

## Respect boundaries

For fiction, the system respects spoiler boundaries. For privacy, it avoids storing credentials, medical record numbers, or other sensitive identifiers even in the private repo. For provenance, it separates source claims from user beliefs.

## Reuse over recapture

If an idea was already captured, the system links to it instead of creating a duplicate. If a workflow already exists, it is extended rather than rebuilt.

## Useful synthesis over note volume

The goal is not to collect every thought. The goal is to surface the right information at the right time. Many captured notes may stay as raw captures; only durable, reusable insights become first-class objects.

## Next

- [High-level architecture](architecture-overview.md)
- [Guided Reading capability](../capabilities/guided-reading.md)
