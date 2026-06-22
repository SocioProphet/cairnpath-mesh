# CairnPath Identity Semantics v0

Entity identity is the keystone for CairnPath. Deduplication, ranking ties, frontier digests, replay, caching, and cross-backend conformance all depend on stable entity references.

## EntityRef

A CairnPath EntityRef is the canonical identity record for an entity in a frontier.

Required fields:

- `namespace`: authority or dataset namespace.
- `kind`: entity class or type, such as `User`, `Device`, `ConceptNode`, `PredicateNode`, or `Edge`.
- `key`: stable business key or canonical logical identifier.
- `canonical`: normalized string used for ordering, hashing, and conformance.

Optional fields:

- `backend`: backend that produced the entity, such as `neo4j` or `atomspace`.
- `backend_local_id`: backend-local id, handle, element id, or uuid.
- `labels`: normalized backend labels or type aliases.
- `equivalence`: alternate keys or semantic aliases.

## Canonical identity rule

The `canonical` string MUST be deterministic and SHOULD be built from normalized namespace, kind, and key:

```text
namespace + ":" + kind + ":" + key
```

All components MUST be Unicode-normalized to NFC before hashing or comparison.

## Backend-local identifiers

Backend-local identifiers MAY be recorded for traceability, but they MUST NOT be the only identity available for cross-backend conformance.

Examples:

- Neo4j element ids or internal ids may help within one backend execution, but conformance SHOULD use stable properties or mapped business keys.
- AtomSpace handles or uuid-like values may help within one AtomSpace execution, but conformance SHOULD map to canonical Atomese names or explicit logical keys when available.

## Deduplication

Deduplication modes:

- `identity`: compare EntityRef `canonical` values.
- `canonical_equivalence`: compare normalized equivalence classes defined by semantic-serdes or fixture-local alias maps.

## Ordering

Tie-breaks MUST sort by EntityRef `canonical` lexicographically unless a stricter fixture-specific ordering is declared.

## Cross-backend equivalence

Neo4j and AtomSpace results are equivalent only after backend-native objects are normalized to EntityRefs. Raw paths, rows, handles, or atoms are not conformance artifacts until normalized.
