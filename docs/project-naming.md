# Project Naming and Attribution

Ethan OS is a public upstream project. You are encouraged to create your own personal OS from it, but your downstream system should have its own identity.

## Upstream project

- **Ethan OS** refers to the upstream project hosted at the canonical Ethan OS repository.
- It is licensed under Apache License 2.0.
- It provides the behavior layer: workflows, skills, schemas, validation, and documentation.

## Downstream projects

When you bootstrap your own OS, choose a distinct name. Examples:

- John OS
- Alex OS
- Jamie OS

The downstream README and config should use the new name. The upstream lineage should remain clear — for example:

> "John OS is a personalized operating system built from Ethan OS."

This makes it obvious which system is the original upstream and which is the personal derivative.

## What to preserve

- The `LICENSE` file from Ethan OS.
- The `NOTICE` file and any applicable upstream attribution.
- References to Ethan OS as the upstream project in lineage metadata.

## What not to do

- Do not rename "Ethan OS" inside the `LICENSE` or `NOTICE` files.
- Do not imply that a materially modified fork is the official Ethan OS release.
- Do not remove upstream attribution from legal/project-lineage files.

## Trademarks

This document is informational. It does not establish any registered trademark policy. If Ethan OS develops a formal trademark policy in the future, this document will be updated to point to it.

## Practical guidance

If you publish a fork or derivative:

1. Use a distinct project name.
2. Keep the `LICENSE` and `NOTICE` files intact.
3. Add your own attribution in a separate section of `NOTICE` rather than deleting upstream notices.
4. Link back to the Ethan OS upstream repository.

For the technical mechanism, see [Create your own OS](getting-started/create-your-own-os.md) and [Updating your OS](getting-started/updating-your-os.md).
