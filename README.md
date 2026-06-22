# CairnPath Mesh

CairnPath Mesh is the canonical protocol, schema, fixture, policy, and conformance bundle for **CairnPath**: a bounded-frontier traversal framework for graph and hypergraph backends.

This repository is the normative home for CairnPath semantics. It is not the full production runtime. Runtime execution can live in AgentPlane or backend-specific runners, while this repository defines what a valid CairnPath line, step, context, result, materialization request, policy cap, and TriTRPC frame must mean.

## Core idea

CairnPath represents traversal as an ordered sequence of small, typed steps over a bounded frontier.

The central invariant is:

```text
F[t+1] = TopK(Rank(Dedup(Expand(F[t]))))
```

Where:

- `F[t]` is the current frontier.
- `Expand` is the backend-specific candidate expansion.
- `Dedup` canonicalizes candidates by identity or equivalence.
- `Rank` produces deterministic ordering under a named policy.
- `TopK` enforces a frontier cap.

This does not make graph traversal magically exhaustive or free. It makes deep traversal bounded, replayable, auditable, and portable across backends.

## Repository scope

This repository owns:

- CairnPath semantics and terminology.
- Cairn context, step, line, result, materialization, and policy schemas.
- TriTRPC/TriRPC frame payload integration for CairnPath messages.
- Backend adapter contracts for Neo4j/APOC and OpenCog AtomSpace.
- Worked examples and conformance fixtures.
- Validation tooling and canonical hashing rules.

This repository does not own:

- TriTRPC transport internals.
- Production runner orchestration.
- Workspace governance.
- Long-term storage and benchmark infrastructure.

Those belong to their respective platform repos. This repository defines the traversal contract they consume.

## Current bundle contents

- `schemas/envelope/frame.v0.jsonschema.json` — TriTRPC/TriRPC frame envelope.
- `schemas/cairn/*.v0.jsonschema.json` — CairnPath context, step, line, result, and materialization schemas.
- `schemas/policy/cairn_limits.v0.jsonschema.json` — bounded traversal policy caps.
- `fixtures/` — validation fixtures.
- `tools/validate.py` — schema and frame validation with canonical JSON hashing.

## Integration targets

Initial backend targets:

- **Neo4j/APOC** for property-graph traversal, sequence expansion, optional expansion, and bounded frontier examples.
- **OpenCog AtomSpace** for hypergraph pattern matching, MeetLink/QueryLink-based expansion, and grounding extraction.

Initial platform integrations:

- **TriTRPC** for frame/envelope and deterministic message transport.
- **AgentPlane** for execution/replay lifecycle.
- **Sociosphere** for workspace composition and governance.
- **semantic-serdes** for entity normalization, aliases, and parity matrices.
- **socioprophet-standards-storage** for persisted traces, benchmark workloads, and evidence datasets.

## Validation

```bash
python3 -m pip install jsonschema && python3 tools/validate.py
```

## Status

Draft v0 bundle. The repository is being hardened toward a v0.1 spec lock. The v0.1 lock requires:

1. stable identity and frontier digest semantics,
2. deterministic ranking and tie-break rules,
3. explicit optional expansion attachment semantics,
4. Neo4j/APOC and OpenCog AtomSpace worked examples,
5. golden StepTrace fixtures,
6. validator coverage for schema and frame payloads.
