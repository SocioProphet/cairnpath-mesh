# CairnPath + TriRPC bundle v0.5

CairnPath Mesh is the canonical replay/materialization contract for bounded graph/hypergraph traversal, proof-carrying frame envelopes, and policy-bounded CairnLine execution.

This repository contains:

- TriRPC frame envelope schema
- CairnPath schemas: `Context`, `Step`, `Line`, `Result`, and `Materialize`
- policy schema: `CairnLimits`
- fixtures and validator tooling
- adapter contracts for Neo4j/APOC and AtomSpace
- a twin-economy reconciliation contract showing how domain packs must compose with the shared CairnPath spine

## Read first

- `docs/export_context_pack_v0_5.md` — canonical export context and design synthesis
- `docs/cairnpath_v0.md` — CairnPath semantics and invariant
- `docs/neo4j_adapter_contract_v0_5.md` — Neo4j/APOC adapter contract
- `docs/atomspace_adapter_contract_v0_5.md` — AtomSpace adapter contract
- `docs/twin-economy-cairn-reconciliation.md` — domain-pack reconciliation contract
- `docs/twin-economy-contested-logistics-fixture.md` — worked replay fixture notes

## Validate

```bash
python3 -m pip install jsonschema && python3 tools/validate.py
```

Validation checks schema syntax, internal schema references, frame envelopes, payload schemas, and canonical frame hashes for fixtures.

## Contract stance

CairnPath remains the canonical replay/materialization spine. Domain packs may add semantics, but they must map decision checkpoints, candidate actions, execution traces, outcomes, projections, and limits into the shared `Context` / `Step` / `Line` / `Result` / `Materialize` / `CairnLimits` model.
