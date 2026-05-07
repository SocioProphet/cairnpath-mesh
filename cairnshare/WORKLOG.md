# CairnShare Worklog and Continuity Record

## Purpose

This document preserves the CairnShare workstream so it can be resumed without relying on chat memory.

CairnShare is the open-source, DataWalk-purged successor to the earlier link-analysis shareability work. It is designed for CairnPath Mesh / FogMesh and focuses on verifiable, bounded, shareable graph analysis across AtomSpace, Neo4j, and other graph engines.

## Origin question

The starting question was:

> What is required for a user to be able to share a link analysis?

The generalized form is:

> Can a user share a graph/hypergraph analysis with another user such that the recipient can execute or inspect exactly the intended analysis, without receiving raw graph access, and with proof of what ran and what was returned?

## Key insight

Sharing a graph analysis is not the same thing as granting database access. The safe primitive is a bounded, policy-enforced analysis lens plus a receipt.

Raw graph access is too broad. Static exports are non-reproducible. CairnShare introduces a third path: share a live, bounded, replayable analysis with enforced projection and cryptographic evidence.

## Project name

**CairnShare**

Tagline:

> Verifiable graph analysis sharing across AtomSpace, Neo4j, and beyond.

A cairn is a trail marker. In this system, a Cairn is a signed, replayable marker through graph space: what path was taken, what rules constrained it, and what evidence resulted.

## Core artifacts

### Analysis Bundle (AB)

The Analysis Bundle captures what the sharer intended to run.

It includes:
- engine target (`atomspace`, `neo4j`, `sparql`, etc.)
- query/program language (`atomese`, `cypher`, `sparql`, etc.)
- query/program text
- parameters
- scope hints
- projection intent
- bounded execution controls
- optional dataset snapshot references
- optional signatures

### Share Policy (SP)

The Share Policy captures who is allowed to run or inspect the analysis and under what constraints.

It includes:
- subject (`user`, `group`, `role`, `public-link`, `token-bound`)
- actions (`analysis.execute`, `result.read`, `result.export`, etc.)
- scope restrictions (`namespace`, `subgraph`, `seeded-expansion`, `label-rel`, `atomtype-predicate`)
- projection controls
- query profile controls
- inference/procedure restrictions
- enforcement mode (`engine-native`, `gateway-enforced`, `hybrid`)

### Dry-Run Report (DR)

The Dry-Run Report is the universal dependency explainer.

It answers:
- Is this user allowed to execute this analysis?
- What permissions/scopes/capabilities are missing?
- What operations, procedures, or inference steps are blocked?
- Why?

This is the portable replacement for vendor-specific permissions troubleshooting.

### Execution Receipt (ER)

The Execution Receipt proves what actually happened.

It includes:
- engine name/version/config digest
- AB digest
- SP digest
- program digest
- inputs digest
- effective policy after resolution
- result digest
- counts/warnings/violations
- optional signatures/attestations

The ER is the proof object that FogMesh can commit to an evidence log.

## Two mandatory safety invariants

### 1. Projection enforcement is mandatory

Even if an engine claims property-level security, CairnShare adapters must enforce projection at the gateway/adapter layer.

Reason: graph engines differ; a portable share protocol cannot trust engine-specific property security semantics.

### 2. Bounded execution is mandatory

Adapters must enforce:
- timeout
- frontier cap
- max results
- depth cap
- dedupe rules

Reason: graph traversal and hypergraph inference can escape intended scope or cause resource exhaustion.

## AtomSpace-first design

AtomSpace is the first target because it is a semantic hypergraph with inference, truth values, attention values, and rich atom structures.

Primary risks:
- unbounded traversal
- inference expanding scope
- leakage through TruthValue / AttentionValue / custom Values
- predicate/atom-type overexposure

AtomSpace adapter defaults:
- seeded expansion only
- inference OFF by default
- atom type allowlist/denylist
- predicate allowlist/denylist
- projection whitelist
- depth/frontier/time/timeouts
- gateway-enforced projection

## Neo4j later

Neo4j is the next likely adapter.

Primary risks:
- unsafe Cypher clauses
- APOC/procedure abuse
- property leakage
- rel-type/label expansion beyond intended scope

Neo4j adapter defaults:
- allowlisted Cypher subset
- procedure deny-by-default
- projection enforcement at adapter
- label/relationship-type scope controls
- result envelope normalization

## FogMesh mapping

FogMesh grammar:

Offer → Request → Execute → Prove → Commit → Replay

CairnShare mapping:
- Offer: adapter publishes `capabilities()`
- Request: user submits AB + SP
- Execute: adapter runs bounded sandbox
- Prove: ER is produced
- Commit: ER is appended to the FogMesh evidence/event log
- Replay: another node verifies digests and re-runs against declared snapshot refs

## Normative digest and canonicalization rules

The v0.1 spec requires canonical JSON semantics similar to RFC 8785 / JCS:
- UTF-8
- sorted object keys
- no insignificant whitespace
- arrays preserve order
- JSON string escaping
- minimal number encoding
- `sha256:<hex>` digest format in v0.1

Production implementation must use a strict JCS-compatible canonicalizer. The included `tools/digest.py` is scaffolding and not complete numeric-normalization compliance.

## Adapter contract

Every adapter must implement:

1. `capabilities()`
   - supported languages
   - enforceable scope primitives
   - enforceable projection primitives
   - dangerous ops/procedures
   - inference support

2. `compile_policy(SP)`
   - translates SP into native/gateway/hybrid enforcement plan

3. `dry_run(AB, SP, identity)`
   - emits DR
   - explains missing permissions and blocked operations

4. `execute(AB, SP, identity)`
   - executes in sandbox
   - projection-enforces results
   - emits ER

5. `explain(AB, SP)`
   - human-readable operational explanation

## Current upstream integration state

This work is being integrated into:

https://github.com/SocioProphet/cairnpath-mesh

The integration branch created for this work is:

`feat/cairnshare-fogmesh-v0-1`

The initial upstream payload should live under:

`cairnshare/`

## What exists in the v2 payload

The v2 payload contains:
- `README.md`
- `LICENSE`
- `spec/analysis-bundle.schema.json`
- `spec/share-policy.schema.json`
- `spec/execution-receipt.schema.json`
- `spec/dryrun-report.schema.json`
- `spec/NORMATIVE.md`
- `spec/examples/analysis-bundle.example.json`
- `spec/examples/share-policy.example.json`
- `spec/vectors/canonicalization_vector_1.json`
- `adapters/ADAPTER_CONTRACT.md`
- `adapters/atomspace/README.md`
- `cli/README.md`
- `argo/workflows/workflowtemplate.yaml`
- `argo/workflows/run.yaml`
- `argo/workflows/cron.yaml`
- `docs/fogmesh-mapping.md`
- `docs/threat-model.md`
- `docs/HISTORY.md`
- `docs/TEACHING_NOTES.md`
- `docs/STATUS.md`
- `tools/digest.py`
- `tests/README.md`
- `tests/run_conformance.sh`
- `tests/fixtures/identities.json`

## Current gaps

The repo is not yet a complete executable product.

Missing:
1. AtomSpace adapter v0 implementation
2. strict RFC 8785/JCS canonicalization implementation
3. result-envelope schema
4. FogMesh commit-envelope schema
5. adapter conformance harness that actually executes containers
6. Neo4j adapter stub and mapping docs
7. replay verifier

## Recommended next work

1. Add result-envelope schema and vectors.
2. Add FogMesh commit-envelope schema and example.
3. Implement strict canonicalization.
4. Implement AtomSpace adapter v0.
5. Add conformance tests.
6. Add Neo4j adapter stubs.
7. Wire ER commit into FogMesh evidence log.

## Teaching summary

CairnShare teaches that graph analysis sharing should not mean graph access. It should mean bounded, projected, policy-backed, replayable analysis.

The system’s essential story is:

> We share the path, not the territory.
