# OpenCog AtomSpace Integration Contract v0

OpenCog AtomSpace is a CairnPath backend target for hypergraph traversal and pattern-matcher-driven expansion.

## Scope

The AtomSpace adapter compiles CairnPath expansion steps into Atomese query patterns and executes them through the AtomSpace query engine. AtomSpace is an executor and knowledge substrate; CairnPath semantics remain defined by this repository.

## Canonical query strategy

The v0 adapter SHOULD prefer Scheme/Atomese query construction for correctness-first behavior. Python may orchestrate execution, but the semantic query shape SHOULD remain Atomese-compatible.

## Relation encoding

The adapter MUST support the traditional labeled-edge idiom:

```scheme
(EvaluationLink
  (PredicateNode "REL")
  (ListLink FROM TO))
```

The adapter MAY support `EdgeLink` where available, but must normalize both forms into the same CairnPath EntityRef and StepTrace semantics.

## Opcode mapping

| CairnPath opcode | AtomSpace mapping |
| --- | --- |
| `expand` | MeetLink/QueryLink pattern returning candidate groundings. |
| `optional_expand` | MeetLink/QueryLink expansion normalized to optional mode when no groundings are returned. |
| `sequence_expand` | Driver-loop sequence of Atomese expansion patterns with per-substep frontier policy. |
| `filter` | Atomese predicate pattern or adapter-side filter. |
| `rank` | Adapter-side deterministic rank over normalized EntityRefs and lightweight metadata. |
| `dedup` | Adapter-side dedup by AtomSpace handle/uuid or canonical EntityRef. |
| `cap` | Adapter-side TopK frontier cap. |
| `materialize` | Explicit AtomSpace value/property/subgraph fetch under policy caps. |

## Result extraction

The adapter MUST normalize query results through documented Value extraction semantics.

Normative v0 extraction rule:

```scheme
(define result (cog-execute! query))
(define items (cog-value->list result))
```

For multi-variable groundings, result items may be tuple-like links. The adapter MUST extract tuple positions deterministically and normalize each bound Atom to an EntityRef.

## Identity normalization

AtomSpace handles/uuids may be recorded as backend-local ids. Cross-backend conformance SHOULD use canonical Atomese names or explicit logical keys when available.

## Sequence expansion

AtomSpace does not need to mimic APOC sequence syntax. The adapter compiles CairnPath `sequence_expand` into an ordered list of Atomese substep patterns and applies the CairnPath frontier invariant after each substep:

```text
Expand -> Dedup -> Rank -> TopK
```

## Optional expansion

If a query returns no groundings, the adapter MUST normalize according to the declared optional mode:

- `keep_frontier`
- `empty_frontier`
- `null_binding`

Under `null_binding`, optional misses MUST be recorded as attachments keyed by the source EntityRef canonical value.

## Guardrails

The adapter SHOULD reject or warn on:

- expansion-like steps without cap policy,
- unbounded sequence traversal,
- missing dedup strategy,
- non-deterministic rank policy,
- materialization beyond policy caps,
- backend-local identifiers used as the only conformance identity.
