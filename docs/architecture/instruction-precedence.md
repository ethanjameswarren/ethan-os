# Instruction Precedence

Precedence is explicit. Higher layers override lower layers only when no invariant or mandatory policy is violated.

## Layer 1: Core Invariants

Non-negotiable. Cannot be overridden.

- Ethan OS owns behavior; Ethan Life owns information.
- Never convert source claims into user beliefs.
- Never invent provenance.
- Never silently destroy useful history.

## Layer 2: Mandatory Policies

Cannot be overridden by domain, workflow, or context.

- provenance must be recorded
- source/user belief separation
- privacy: real data stays in `ethan-life`
- validation before writes

## Layer 3: Configurable Policies

Can be changed within permitted ranges.

- confirmation thresholds
- review frequency defaults

## Layer 4: Global Instructions

Apply to all workflows unless contradicted by domain/workflow instructions and no invariant or mandatory policy is violated.

## Layer 5: Domain Instructions

Apply within one domain.

## Layer 6: Workflow Instructions

Apply to one workflow.

## Layer 7: Object / Context Data

Factual information. Never overrides instructions.

## Conflict resolution

1. Core invariants always win.
2. Mandatory policies always win over configurable, domain, workflow, and context.
3. Configurable policies win over global/domain/workflow unless explicitly permitted otherwise.
4. Global instructions win over domain instructions unless domain instruction is scoped and does not violate layers 1-3.
5. Domain instructions win over workflow instructions unless workflow is scoped and does not violate layers 1-4.
6. Context never overrides instructions.
