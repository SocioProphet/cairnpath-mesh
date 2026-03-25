
# CairnPath v0 (Normative semantics)

CairnPath is a progressive traversal framework for graphs/hypergraphs.

## Invariant
After each hop:

1) candidates = EXPAND(frontier, args)   (engine-specific)
2) candidates = DEDUP(candidates)        (identity or canonical equivalence)
3) candidates = RANK(candidates)         (metadata-only unless materialized)
4) frontier  = CAP(candidates, K)        (fixed or policy-bounded)

This makes total work ~O(hops*K) under stable K.

## Replay
A CairnLine is replayable if dataset_ref is a stable snapshot and each step+result is signed.

## Policy
Policy.CairnLimits bounds: max_hops, max_cap_k, allowed opcodes, and materialization budgets.
