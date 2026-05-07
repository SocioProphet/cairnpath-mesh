# Neo4j/APOC Integration Contract v0

Neo4j/APOC is a CairnPath backend target for property-graph traversal.

## Scope

The Neo4j adapter compiles CairnPath steps into Cypher and APOC path expansion where appropriate. Neo4j is an executor, not the source of CairnPath semantics.

## Opcode mapping

| CairnPath opcode | Neo4j/APOC mapping |
| --- | --- |
| `expand` | Cypher `MATCH` or APOC `apoc.path.expandConfig` with relationship/label filters. |
| `optional_expand` | Cypher `OPTIONAL MATCH` or APOC optional expansion, normalized to CairnPath optional modes. |
| `sequence_expand` | APOC `apoc.path.expandConfig` `sequence` when the sequence is expressible as APOC alternating filters. |
| `filter` | Cypher `WHERE` or post-expansion adapter filter. |
| `rank` | Cypher `ORDER BY` or adapter-side deterministic rank. |
| `dedup` | Cypher `DISTINCT` plus adapter-level visited set when global uniqueness is required. |
| `cap` | Per-hop TopK in adapter or bounded Cypher subquery. Not equivalent to final result `LIMIT`. |
| `materialize` | Explicit Cypher projection/property fetch under policy caps. |

## Per-hop frontier cap

APOC `limit` is useful but is not the same as CairnPath per-hop TopK. CairnPath requires the adapter to enforce:

```text
Expand -> Dedup -> Rank -> TopK
```

for each expansion-like step.

If APOC can express a whole expansion safely, the adapter MAY use it. If per-hop ranking/capping is required, the adapter SHOULD execute hop-by-hop.

## Uniqueness

Supported mappings include:

- `NODE_GLOBAL`: maintain a global visited node set.
- `NODE_RECENT`: maintain a bounded recent window when memory must be capped.
- `RELATIONSHIP_GLOBAL`: maintain visited relationship ids.
- `NONE`: unsafe unless policy explicitly allows it.
- `ENGINE_DEFAULT`: allowed only for exploratory draft mode and not for conformance fixtures.

## Sequence expansion

CairnPath `sequence_expand` is a list of typed node/edge substeps. APOC `sequence` is an optimization target, not the canonical representation.

The adapter MUST preserve CairnPath semantics if APOC sequence syntax cannot express a substep exactly. In that case it MUST fall back to explicit step execution.

## Optional expansion

The adapter MUST normalize Neo4j/APOC optional behavior into one CairnPath optional mode:

- `keep_frontier`
- `empty_frontier`
- `null_binding`

Optional result attachments MUST be keyed by source EntityRef canonical value when replay-critical.

## Identity normalization

Neo4j backend-local ids are not sufficient for cross-backend conformance. The adapter SHOULD map nodes to EntityRefs using stable business keys when available. Backend-local ids MAY be included as trace metadata.

## Guardrails

The adapter SHOULD reject or warn on:

- unbounded variable-length path expansion,
- expansion-like steps without cap policy,
- `NONE` uniqueness without explicit unsafe policy,
- materialization beyond `CairnLimits`,
- path enumeration where entity-frontier traversal was requested.
