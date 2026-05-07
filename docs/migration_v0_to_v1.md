# CairnPath Mesh v0 to v1 Migration

Status: draft
Scope: additive v1 payloads under the existing `frame.v0` envelope

## Strategy

Do not break `frame.v0`. The current envelope already supports typed payload routing through `frame_type`, `frame_kind`, `payload_schema`, `payload`, `links`, and `signatures`.

Migration is additive:

- keep `Cairn.Context v0`, `Cairn.Step v0`, `Cairn.Line v0`, and `Cairn.Result v0`
- add v1 semantic payloads for durable checkpoints, replay events, capability negotiation, and typed set commitments
- dual-write v0 and v1 payloads until old consumers migrate

## Mapping

| v0 object | v1 relationship | Notes |
|---|---|---|
| `Context.v0.frontier.dedup_set_hash` | `SetRef.v1` | v1 replaces a bare hash string with `{kind, hash_alg, value, count}`. |
| `Context.v0.frontier.cap_k` | `frontier_cap` | v1 uses `frontier_cap` as the framework invariant name. |
| `Context.v0.seed_entities` | `EntityRef.v1[]` or compatibility strings | v1 prefers structured business-key identity. |
| `Step.v0.opcode` | `Cairn.v1.op_name` | v1 keeps the current opcode family but adds durable before/after commitments. |
| `Step.v0.args.limit` | `engine_limit_hint` | Database limit is not frontier-cap semantics. |
| `Step.v0.args.cap_k` | `frontier_cap` | Framework cap after dedup/rank. |
| `Result.v0.frontier` | `Result.v1.out_set_ref` plus optional materialized frontier | v1 separates commitment from materialization. |
| `Line.v0.steps` | `Log.v1.events[]` | Line remains metadata; Log records replay/edit lineage. |
| `Line.v0.branch_of` | `Event.v1` type `BRANCH` | Branch is evented in v1. |

## New payloads

- `schemas/cairn/entity_ref.v1.jsonschema.json`
- `schemas/cairn/set_ref.v1.jsonschema.json`
- `schemas/cairn/cairn.v1.jsonschema.json`
- `schemas/cairn/event.v1.jsonschema.json`
- `schemas/cairn/log.v1.jsonschema.json`
- `schemas/cairn/capabilities.v1.jsonschema.json`
- `schemas/policy/cairn_limits.v1.jsonschema.json`

## Dual-write pattern

A runtime executing an expansion should emit:

1. `Cairn.Step v0` for compatibility.
2. `Cairn.Result v0` for compatibility.
3. `Cairn.v1` with `in_set_ref` and `out_set_ref`.
4. `Cairn.Event v1` of type `STACK`.

A restack should emit:

1. `Cairn.Event v1` of type `RESTACK`.
2. `Cairn.Event v1` of type `REPLAY`.
3. `Cairn.Event v1` of type `DIVERGENCE` if downstream commitments changed.

## Backward compatibility

The v1 layer does not require `frame.v1`. It uses the existing envelope through:

```json
{
  "frame_type": "Commit",
  "frame_kind": "Cairn.Event.v1",
  "payload_schema": "cairn/event.v1.jsonschema.json"
}
```

Capability negotiation uses:

```json
{
  "frame_type": "Capability",
  "frame_kind": "Cairn.ExecutorCapabilities.v1",
  "payload_schema": "cairn/capabilities.v1.jsonschema.json"
}
```
