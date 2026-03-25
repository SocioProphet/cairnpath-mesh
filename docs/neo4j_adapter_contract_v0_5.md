# Neo4j CairnPath Adapter Contract v0.5

## Core rule
Neo4j `LIMIT` is not frontier-cap semantics. Frontier cap is enforced in the Cairn driver after expansion.

## Identity
- Default: `elementId(n)` (engine-local)
- Optional canonical equivalence: `n.uuid` or KB canonical id

## Opcode mapping (summary)
- expand: `apoc.path.expandConfig` to generate candidates, then Cairn invariant (dedup→rank→cap)
- optional_expand: same, but preserve context/frontier when no candidates
- sequence_expand: compile to APOC sequence constraints (where supported), enforce hop boundary caps
- filter: push down filters early (labelFilter/relationshipFilter) and/or apply Cypher on candidate set
- rank/dedup/cap: framework-level for cross-engine comparability
- materialize: Cypher + controlled subgraph extraction under policy budgets

## Mandatory metrics emitted each step
- fanout, dedup_ratio, cap_hit, elapsed_ms
- (if available) db_hits, cache_hits, materialized_bytes

## Replay requirement
Record:
- dataset_ref (snapshot/version)
- step args + policy ref
- result frontier
- supporting query digest/refs
