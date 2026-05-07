# Canonicalization Profile v1

Status: draft
Applies to: Cairn v1 payloads, Cairn.Event v1 payloads, Cairn.Log v1 payloads, signed frame hash derivation

## Purpose

CairnPath needs deterministic inscriptions: two semantically identical cairns must produce identical canonical bytes and identical hashes. This document defines the canonicalization and hash profile used by the v1 Cairn semantic layer.

## Normative profile

The canonical JSON profile is `jcs.rfc8785`.

Implementations MUST NOT normalize Unicode strings before hashing. In particular, implementations MUST NOT apply NFC/NFD/NFKC/NFKD transforms as part of canonicalization. Strings are hashed exactly as present in the parsed JSON value.

Implementations MUST reject non-finite numbers. For portable signatures, v1 fixtures SHOULD avoid floating point values in signed semantic inscriptions unless the implementation uses a fully compliant RFC 8785 JSON Canonicalization Scheme encoder.

## Frame hash

For `frame.v0` envelopes, the frame hash is computed over the frame object with this field removed:

- `signatures`

The remaining object is encoded with the canonical JSON profile and hashed with SHA-256.

## Cairn inscription hash

For `cairn.v1`, the semantic inscription hash is computed over a `CairnInscription` projection. The projection is the cairn object with the following fields removed:

- `inscription`
- `cost`
- `created_at`

Everything else remains in scope, including:

- `cairn_id`
- `line_id`
- `parent_cairn_id`
- `replaces_cairn_id`
- `opcode`
- `op_name`
- `args_schema`
- `args`
- `identity_mode`
- `uniqueness_mode`
- `frontier_cap`
- `unsafe_unbounded`
- `in_set_ref`
- `out_set_ref`
- `graph_snapshot_ref`
- `cairnface`
- `cairn_weight`
- `evidence_refs`
- `policy_tags`

Then:

```text
inscription.jcs_sha256 = SHA256(JCS(CairnInscription))
```

`cost` and `created_at` are evidence metadata, not semantic identity. They remain in the cairn but are excluded from the semantic inscription hash so timing and runtime counter variance do not destroy equality.

## SetRef hash

`set_ref.v1` commits to the canonical ordered frontier.

Small sets may use:

```text
SHA256(join("\n", canonical_entity_ref_strings))
```

Large sets may use a Merkle root with explicit domain separation:

```text
leaf_i = SHA256("cairn.set.leaf.v1" || uint64_be(i) || chunk_bytes)
node   = SHA256("cairn.set.node.v1" || left_hash || right_hash)
```

The `SetRef` object records `kind`, `hash_alg`, `value`, `count`, and, when Merkle is used, chunking metadata.

## Validator requirements

The validator MUST:

1. Validate the envelope schema.
2. Resolve and validate the referenced payload schema.
3. Hash frames using the canonical JSON profile with `signatures` excluded.
4. Reject engine-local identity without `graph_snapshot_ref`.
5. Reject expansion-like opcodes without `frontier_cap` unless `unsafe_unbounded=true`.
6. Warn when v0 `args.limit` is present and recommend `engine_limit_hint`.
