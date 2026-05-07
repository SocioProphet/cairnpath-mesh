# CairnShare Spec v0.1 — Normative Rules

This document defines normative behavior for CairnShare artifacts. If an implementation diverges from this, it must be treated as a different protocol.

## 0. Artifacts

CairnShare defines these artifacts:

- **AB**: Analysis Bundle (`kind = cairnshare.analysis-bundle`)
- **SP**: Share Policy (`kind = cairnshare.share-policy`)
- **ER**: Execution Receipt (`kind = cairnshare.execution-receipt`)
- **DR**: Dry-Run Report (`kind = cairnshare.dryrun-report`) — explainer output

AB and SP are the intent plus constraints. ER is the evidence of what ran under what constraints. DR is the portable dependency explainer.

## 1. Canonical JSON

All digests MUST be computed over canonical JSON.

CairnShare v0.1 uses RFC 8785 / JCS-style canonicalization:

1. UTF-8 encoding.
2. Object keys sorted lexicographically by Unicode code point.
3. No insignificant whitespace.
4. Numbers encoded minimally: no trailing zeros, no plus sign, no NaN, no Infinity.
5. Arrays preserve order.
6. Strings use JSON escaping rules.

### Consequence

If two nodes serialize the same AB, SP, or ER differently, they MUST still compute the same digest.

## 2. Digests

All v0.1 digests MUST use this format:

```text
sha256:<lowercase-hex>
```

The hex string MUST be 64 lowercase hexadecimal characters.

Future versions may allow `blake3:` or other algorithms, but v0.1 is sha256-only for interoperability.

### 2.1 Program digest

The program digest MUST be computed from canonical JSON containing:

- `language`
- `text`
- `parameters`

We do not hash only the query string. We hash the query plus parameters so replay is exact.

### 2.2 AB digest

The AB digest MUST be computed from canonical AB JSON with `signatures` removed. Signatures are over the AB digest.

### 2.3 SP digest

The SP digest MUST be computed from canonical SP JSON with `signatures` removed.

### 2.4 Inputs digest

The inputs digest MUST include canonical JSON of:

- identity claims actually used, such as `user_id`, groups, and token-bound claims
- dataset refs actually used and resolved
- runtime flags that affect scope, projection, inference, or replay

This prevents the ambiguity of “same policy, different context.”

## 3. Execution Receipt requirements

An ER MUST include:

- engine name and version
- optional engine config digest
- AB digest
- SP digest
- program digest
- inputs digest
- effective policy after group, token, TTL, and runtime resolution
- result verdict
- result digest
- started timestamp and ideally finished timestamp

## 3.1 Result digest

The result digest MUST be computed from canonical JSON of a normalized result envelope.

The normalized result envelope MUST exclude timestamps, random IDs, and non-deterministic values. It MUST include only projected fields that the policy allows.

## 4. Projection enforcement is mandatory

Even if the underlying engine claims property-level security, CairnShare implementations MUST apply projection enforcement at the gateway or adapter layer, or prove an equivalent enforcement boundary.

This is a core safety invariant. Engines differ. CairnShare cannot rely on engine-specific permission semantics alone.

## 5. Bounded execution is mandatory

Adapters MUST enforce:

- `timeout_ms`
- frontier cap / max expansions
- `max_results`
- depth cap when policy or AB requires it

If a bound is exceeded, the adapter MUST terminate the execution and return WARN or FAIL with a violation explaining which bound was hit.

## 6. Inference is OFF by default

Inference, reasoning, rule expansion, or any operation that can expand visible scope MUST be disabled unless:

- AB controls explicitly request it with `allow_inference: true`
- SP query profile explicitly allows it with `allow_inference: true`
- the adapter applies an inference sandbox with whitelisted rules and bounded chaining

AtomSpace and other hypergraph systems are especially sensitive to this rule.

## 7. Dry-run report is the universal dependency explainer

Dry-run MUST report:

- `allowed`: true or false
- missing actions
- missing scopes
- missing capabilities
- blocked operations
- blocked procedures
- blocked inference
- human-readable `explain[]`

The dry-run report is the portable answer to: “what is required for this user to run or share this graph analysis?”

## 8. Adapter conformance

An adapter MUST NOT be advertised as CairnShare-compatible unless it passes conformance tests for:

- schema validity
- canonical digest stability
- projection enforcement
- scope enforcement
- bounded execution
- blocked dangerous operations
- engine-specific sandboxing requirements

## 9. FogMesh compatibility

CairnShare maps onto the FogMesh grammar:

Offer → Request → Execute → Prove → Commit → Replay

- Offer: adapter publishes `capabilities()`
- Request: user submits AB and SP
- Execute: adapter runs bounded sandbox
- Prove: adapter emits ER
- Commit: ER is appended to the evidence/event log
- Replay: nodes verify digests and re-run against declared dataset snapshots
