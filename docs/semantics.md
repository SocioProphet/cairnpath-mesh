# CairnPath Semantics v0

CairnPath is a bounded-frontier traversal framework. A traversal is not represented as one monolithic query string. It is represented as a CairnLine: an ordered sequence of typed CairnSteps that transform one Context into the next.

## Core objects

- **Context**: execution state for a traversal, including engine reference, dataset reference, seed entities, frontier, constraints, bindings, and timestamps.
- **Frontier**: the ordered working set of entity references at a step boundary.
- **CairnStep**: one typed operation such as `expand`, `optional_expand`, `sequence_expand`, `filter`, `rank`, `dedup`, `cap`, `materialize`, or `commit_view`.
- **CairnLine**: ordered list of CairnSteps rooted at a Context.
- **Result**: materialized or frontier-level output for a step.
- **StepTrace**: execution evidence for a step, including counts, metrics, digests, backend fingerprints, warnings, and policy decisions.

## Frontier invariant

Expansion-like operations MUST end in a bounded frontier unless explicitly marked unsafe by policy.

Normative shape:

```text
F[t+1] = TopK(Rank(Dedup(Expand(F[t], step_args))))
```

This invariant means CairnPath is usually a beam-bounded traversal system. It is not exhaustive unless a policy explicitly permits exhaustive traversal and the step trace records that unsafe choice.

## Expansion-like steps

The following opcodes are expansion-like:

- `expand`
- `optional_expand`
- `sequence_expand`

For these steps, the executor MUST produce metrics for:

- raw expanded candidate count,
- deduplicated count,
- final frontier count,
- whether the cap was hit,
- elapsed time,
- backend-specific work counters when available.

## Ranking and capping

A cap without deterministic ranking is not reproducible. Every capped operation MUST declare a rank policy or inherit one from policy. Ties MUST be broken deterministically by canonical entity reference ordering.

## Deduplication

Deduplication MUST use either identity or canonical equivalence. Backend-local identifiers MAY be used inside a single backend run, but cross-backend conformance MUST use canonical entity references.

## Optional expansion

Optional expansion is not a synonym for arbitrary outer-join behavior. It MUST declare an optional mode. The supported v0 modes are:

- `keep_frontier`: expansion miss keeps the input frontier unchanged.
- `empty_frontier`: expansion miss produces an empty frontier.
- `null_binding`: expansion miss keeps the source entity and records an explicit null/miss attachment.

## Lazy materialization

Navigation SHOULD operate on entity references and lightweight metadata. Heavy properties, full subgraphs, or packets MUST be fetched through an explicit `materialize` operation constrained by policy.

## Replay

Replay is deterministic only when the following are stable:

- dataset or snapshot reference,
- entity reference normalization,
- rank policy and version,
- tie-break rules,
- canonical serialization and digest rules,
- backend adapter version.

When a backend cannot provide stable snapshot semantics, the StepTrace MUST record replay as best-effort rather than deterministic.
