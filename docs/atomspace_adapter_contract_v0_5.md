# AtomSpace CairnPath Adapter Contract v0.5

## Core rule
AtomSpace’s matcher can return huge match sets; CairnPath bounds exploration via frontier discipline each hop.

## Identity/dedup
Choose one per dataset:
- identity: engine-local atom handle/pointer identity
- canonical_equivalence: canonical atom name or KB id attached to atoms

## Canonical one-hop expansion pattern (conceptual)
Return $to such that:
- $from ∈ frontier_set
- edge($from, $to) holds (represented as a predicate relation)

## Extraction semantics (must be specified in implementation)
Define:
- which container type is returned (queue/set)
- how to enumerate it deterministically into AtomIDs
- how to attach supporting_refs for replay (query digest, scheme snippet digest, engine ref)

## Ranking tiers
- metadata-only pre-materialize
- richer post-materialize
Rank policies may only reference available features.

## Mandatory metrics emitted each step
- fanout, dedup_ratio, cap_hit, elapsed_ms
- plus any matcher stats available
