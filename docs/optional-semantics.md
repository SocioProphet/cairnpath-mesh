# CairnPath Optional Expansion Semantics v0

Optional expansion must be explicit. It is not a vague outer join. A CairnPath `optional_expand` step MUST declare an `optional_mode`.

## Modes

### keep_frontier

If expansion from a source entity yields no candidates, the source entity remains in the frontier.

Use this when the optional expansion is a probe and a miss should not stop traversal.

### empty_frontier

If expansion yields no candidates, the output frontier is empty.

Use this when the optional edge is logically required for continuation but should not be treated as an error.

### null_binding

If expansion from a source entity yields no candidates, the source entity remains and an explicit miss attachment is recorded.

Use this for outer-join-like enrichment where the source row/entity must survive and the missing relationship is evidence.

## Attachments

Optional expansion MAY produce attachments keyed by source EntityRef canonical value.

Attachment shape:

```json
{
  "source": "namespace:kind:key",
  "neighbors": ["namespace:kind:key"],
  "miss": false,
  "mode": "null_binding"
}
```

For a miss under `null_binding`:

```json
{
  "source": "namespace:kind:key",
  "neighbors": [],
  "miss": true,
  "mode": "null_binding"
}
```

## Replay and hashing

A StepTrace MUST state whether optional attachments are replay-critical.

If replay-critical, attachment digests MUST be computed from canonical source keys and ordered neighbor keys.

If not replay-critical, attachments are treated as materialized evidence rather than frontier semantics.

## Backend mapping

Neo4j/APOC optional expansion may use APOC `optional` or Cypher `OPTIONAL MATCH`, but the adapter MUST normalize results into one of the modes above.

OpenCog AtomSpace optional expansion is implemented by normalizing empty MeetLink/QueryLink grounding results according to the selected mode.
