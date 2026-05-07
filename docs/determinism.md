# CairnPath Determinism and Replay v0

CairnPath replay is deterministic only when identity, ordering, ranking, policy, backend adapter behavior, and dataset snapshot semantics are stable.

## Deterministic frontier order

A frontier is an ordered list. The order is semantically relevant because TopK keeps a prefix of that ordered list.

Executors MUST order a frontier as:

1. descending or ascending rank according to the declared rank policy,
2. then lexicographic order by EntityRef `canonical` as a deterministic tie-break.

If a step has no rank policy, the executor MUST use lexicographic EntityRef ordering unless the policy declares the step order-insensitive.

## Stable digests

Frontier digests MUST hash the canonical ordered frontier representation, not backend-native object representations.

The canonical digest input SHOULD include:

- schema version,
- ordered EntityRef canonical values,
- optional score values when score-sensitive replay is required,
- snapshot reference when available.

## Snapshot references

A Context SHOULD include a dataset or snapshot reference. If the backend supports transaction-consistent or as-of reads, the snapshot reference MUST identify that state.

If no stable snapshot is available, StepTrace MUST record replay mode as `best_effort`.

## Rank policy versioning

Rank policies MUST be versioned. A replay under a different rank policy version is not deterministic replay; it is a re-execution under changed semantics.

## Backend adapter fingerprint

A StepTrace SHOULD include a backend query fingerprint and adapter version. This lets conformance distinguish semantic divergence from backend implementation drift.

## Non-deterministic backend behavior

When a backend returns unordered results, the adapter MUST normalize before emitting a frontier. Backend-native order MUST NOT leak into CairnPath frontier order unless explicitly declared and justified.
