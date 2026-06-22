# CairnPath Materialization Semantics v0

CairnPath separates traversal from materialization.

Traversal SHOULD operate over EntityRefs and lightweight metadata. Expensive payloads, full property maps, subgraphs, packets, and external artifacts MUST be fetched through an explicit `materialize` operation governed by policy.

## Materialization modes

The v0 materialization schema supports:

- `metadata_only`: fetch identifiers, labels/types, and minimal ranking metadata.
- `properties`: fetch declared properties for declared targets.
- `full_subgraph`: fetch a bounded subgraph around declared targets.
- `packet`: fetch or create a transportable evidence packet.

## Projection discipline

A materialization request MUST declare targets and maximum bytes. Future versions SHOULD also declare projection fields, redaction rules, and purpose tags.

## Minimum necessary principle

Executors SHOULD delay materialization until after frontier narrowing. A typical safe flow is:

```text
expand -> dedup -> rank -> cap -> materialize
```

rather than:

```text
expand -> materialize everything -> filter later
```

## Replay and evidence

A materialization result MAY be replay-critical or evidence-only.

- Replay-critical materialized values must be digestible and stable.
- Evidence-only materialized values may be stored by reference and excluded from frontier digest semantics.

A StepTrace or Result MUST make this distinction explicit when materialized values are emitted.

## Policy interaction

Materialization MUST respect CairnLimits such as:

- `max_materialize_bytes`,
- allowed namespaces,
- privacy mode,
- allowed predicates or relations,
- execution budget.

Materialization denied by policy MUST emit a structured warning or failure rather than silently dropping requested data.
