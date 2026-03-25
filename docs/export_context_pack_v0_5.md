# CairnPath Mesh — Export Context Pack v0.5 (Canonical)

**Status:** export-ready canonical context  
**Date:** 2026-02-07  
**Scope:** Citizen-fog storage+compute mesh, protocol-society event grammar, proof-carrying execution, versioned knowledge substrate, and CairnPath bounded traversal.

---

## 0) One-line thesis

We’re building a **local-first, open mesh** composed of interchangeable **organs** (compute, knowledge, social, education, dev-experience) snapped together by a shared **spine**:

> **TriRPC + AUM packaging + Policy + Evidence + Append-only replay**

Everything—whether volunteer compute, a graph DB, an IDE workspace, peer review, or gossip—speaks a small set of **verbs** and produces **proof-carrying events**.

---

## 1) Naming: CairnPath

We name the overall progressive traversal approach **CairnPath**:

- A **cairn** is a human-made trail marker: editable, intentional, and persistent even when terrain is chaotic.
- Each step is a **CairnStep** (not “breadcrumb”): typed operation + args + constraints + audit footprint.
- The visible history of steps is the **CairnLine**.
- The runtime working set is the **Frontier**, with enforced **Frontier Cap** + **Dedup** every hop.

This vocabulary is simultaneously:
- graph-theory legible (frontier, bounded expansion),
- investigator legible (cairns, line),
- database legible (bounded intermediate sets).

---

## 2) Design goals (non-negotiable)

### 2.1 Citizen-fog reality
- Machines are heterogeneous and ephemeral; churn is normal.
- We standardize **interfaces**, not hardware.

### 2.2 Local-first performance with distributed correctness
- Local reads/writes should be fast.
- Distributed correctness emerges from **append-only logs + replication policies**, not centralized authorities.

### 2.3 Open systems, composable plumbing
- Prefer open/auditable components and stable interfaces.
- Avoid monolithic platforms that embed a single vendor worldview.

### 2.4 Safety and user dignity
- Explicit consent; reversible participation; clear resource caps.
- Tokenization is optional and never the root of legitimacy; **proof is**.

---

## 3) The mesh is not “a system,” it’s a grammar

We treat the mesh as a **protocol society**. Coherence comes from forcing diverse components to speak the same verbs:

- **Offer**: capabilities + constraints  
- **Request**: job / query / review assignment / workspace  
- **Execute**: inside explicit, inspectable sandbox  
- **Prove**: outputs + environment digest + policy ref + signature  
- **Commit**: append-only record; branchable; diffable  
- **Reward**: optional; downstream of proof, never upstream of legitimacy  

This is the core integration trick: upstream diversity, downstream invariants.

---

## 4) The spine: TriRPC + AUM + proof-carrying events

### 4.1 TriRPC (edge transport + control plane)
- QUIC primary
- UDS local fast-path
- optional WebRTC/TURN fallback for hostile NATs

### 4.2 AUM packaging (unit of distributable capability)
AUM is the unit of distribution:
- job packages
- schema bundles
- adapter bundles
All are content-addressed and policy-bound.

### 4.3 Proof objects are first-class
Every meaningful action yields a signed artifact containing:
- input refs (digests)
- output refs (digests)
- environment digest (runtime/image/SBOM/platform)
- policy reference (decision context)
- signatures

This keeps the mesh honest: we can replay, audit, dispute, and compare outcomes.

---

## 5) Storage substrate: local-first bytes

### 5.1 TopoLVM everywhere (for Kubernetes nodes)
TopoLVM provides local PV provisioning using LVM and supports capacity-aware placement via Kubernetes storage capacity tracking.

We treat TopoLVM as:
- fast local bytes
- predictable allocation
- churn-friendly storage substrate

**TopoLVM is not distributed storage.** Durability lives above it.

### 5.2 Workstations mirror the contract
Workstations use LVM thin volumes directly but expose the same directory/mount contract.

### 5.3 Canonical filesystem contract (host)
- `/srv/fog/projects`
- `/srv/fog/models`
- `/srv/fog/datasets`
- `/srv/fog/topics`
- `/srv/fog/vector`
- `/srv/fog/cache`
- `/srv/fog/logs`
- `/srv/fog/secrets` (sealed; RO in containers)
- `/srv/fog/tmp` (disposable)

### 5.4 Canonical container-visible mounts
- `/mnt/fog/projects`
- `/mnt/fog/models`
- `/mnt/fog/datasets`
- `/mnt/fog/topics`
- `/mnt/fog/vector`
- `/mnt/fog/cache`
- `/mnt/fog/logs`
- `/mnt/fog/secrets` (RO)
- `/mnt/fog/tmp`

Result: dev == fog == prod-ish at the filesystem contract layer.

---

## 6) Distributed meaning: append-only topics (Merkle-log channels)

We anchor semantics, replication, and auditability in append-only, verifiable log topics (Hypercore-style Merkle-log topics).

A topic is a log whose entries are:
- schema/versioned envelopes
- encrypted (topic keys; rotating epochs)
- verifiable (Merkle proofs / signatures)
- replicated by topic policy (replicas, acks, retention, compaction)

Folders and views are projections; logs are truth.

---

## 7) Compute substrate: Volunteer Compute Mesh + attestation lane

### 7.1 Baseline execution lane (Volunteer Compute Mesh)
- WASM-first for determinism and capability control
- rootless containers as escape hatch
- replication + canaries as default correctness strategy
- outputs are **JobProofs** (digests + env digest + policy + signature)

### 7.2 Attestation lane (TEE)
Trusted execution frameworks (e.g., iExec TCF-style) provide optional TEE proofs:
- enclave measurement/quote
- TCB status
- output digest binding

This complements replication-based verification; it does not replace it.

### 7.3 Compute marketplace bridges (optional)
Adapters can map internal FogCompute artifacts to external systems (iExec-like, Akash, Golem), but settlement is not foundational.

---

## 8) Knowledge organ: versioned knowledge with time travel

We treat knowledge as versioned, branchable, diffable objects (TerminusDB-like semantics):
- branch-per-case / branch-per-course conventions
- merge approvals as governance artifacts
- schemas/ontologies versioned in the KB itself

The KB is behind TriRPC: it is an organ, not the edge API.

---

## 9) Social + governance organs

### 9.1 Gossip organ (SSB-like feeds)
Social streams can replicate via signed, append-only feeds and ingest into the KB via adapters.

### 9.2 Education/peer review organ (Expertiza-like workflows)
Assignments, rubrics, reviews, and scores become events:
- `Edu.Assignment.Upsert`
- `Edu.Review.Upsert`
- `Edu.Score.Upsert`

These are governance evidence, not mere UI states.

### 9.3 Incentives (optional)
Rewards/credits can be layered later, but **proof + consent** remain the root of legitimacy.

---

## 10) FogCompute internal protocol (artifact model)

We define a canonical “always works” protocol that adapters map onto external systems:

### 10.1 Entities
- Provider
- Requestor
- Broker (optional)
- Verifier (optional)

### 10.2 Artifacts (append-only, content-addressable)
- **Offer**: resources, availability, pricing, constraints, attestation claims
- **WorkOrder**: image digest, inputs, outputs, verification policy
- **JobProof / UsageReceipt**: metering + env digest + output digests + signatures
- **VerificationDecision**: which proof(s) were accepted, why, and policy clauses
- **SettlementEvent**: optional mapping to credits/tokens

### 10.3 Metering contract
Linux-first metering via OS accounting (cgroups). The receipt is the canonical outcome.

---

## 11) Security and trust posture

### 11.1 Integrity
All critical artifacts are:
- content-addressed
- signed
- append-only committed

Tampering is detectable.

### 11.2 Confidentiality
- topic-level encryption with rotating epochs
- membership changes trigger epoch rotation (forward secrecy posture as feasible)

### 11.3 Verification (policy-selectable)
- TEE attestation where available
- replicated verification where not
- reputation/spot checks for cost control

### 11.4 User protection defaults
- opt-in participation
- explicit resource caps
- transparent manifests
- auditable receipts
- exit is always possible (no protocol captivity)

---

## 12) CairnPath: bounded progressive traversal framework (normative)

CairnPath turns unbounded path enumeration into bounded iterative deepening over a controlled frontier.

### 12.1 CairnPath invariant (non-negotiable)
After every hop, we compute:

1) `candidates = EXPAND(frontier, args)`  
2) `candidates = DEDUP(candidates)`  
3) `candidates = RANK(candidates)`  
4) `frontier  = CAP(candidates, K)`  

This prevents exponential blowups by enforcing a bounded intermediate set every hop.

### 12.2 Lazy evaluation
We compute with cheap metadata first (IDs, types, degrees, light stats) and only **materialize** deeper properties when later steps prove they’re needed.

### 12.3 Replay + audit
A CairnLine is replayable when:
- it references a stable dataset snapshot (`dataset_ref`)
- each step has inputs/outputs contexts
- steps/results are committed as signed frames

### 12.4 CairnStep opcodes (initial set)
- expand
- optional_expand
- sequence_expand
- filter
- rank
- dedup
- cap
- materialize
- commit_view

### 12.5 Policy.CairnLimits (safety + predictability)
Policy bounds:
- max hops
- max cap K
- allowed opcodes
- allowed predicates/relations/namespaces
- max materialize bytes
- max elapsed time

---

## 13) Neo4j adapter: mapping Cairn opcodes to Cypher/APOC (contract)

### 13.1 Core rule
Neo4j `LIMIT` is not frontier cap semantics. Frontier cap is enforced in the Cairn driver layer.

### 13.2 Identity and dedup
- default dedup identity: `elementId(node)` (engine-local)
- optional canonical equivalence: domain `uuid` field (cross-engine)

### 13.3 Expand mapping
Use `apoc.path.expandConfig` (or subgraph procs) to produce candidate neighbors with:
- relationshipFilter / labelFilter
- bfs
- uniqueness (NODE_RECENT recommended for huge traversals)
- terminators / endNodes
Then apply Cairn invariant in framework: dedup → rank → cap.

### 13.4 Optional expand
If expansion returns empty candidates, preserve context according to canonical behavior (recommended: preserve frontier + warning).

### 13.5 Sequence expand
Compile a Cairn sequence into APOC sequence constraints where possible; still enforce per-hop frontier discipline at hop boundaries.

### 13.6 Materialize
Hydrate properties/subgraph only after selection, under max-bytes/time policy.

---

## 14) AtomSpace adapter: MeetLink/QueryLink + bounded frontier (contract)

### 14.1 Core rule
AtomSpace’s pattern matcher can return huge matches. CairnPath bounds the intermediate set.

### 14.2 Canonical neighbor expansion
Model edges as an explicit predicate relation (e.g., `Evaluation(Predicate "edge", List(from,to))`), and expand:

- bind `$from` ∈ frontier via membership
- match relation
- return `$to` groundings

### 14.3 Extraction semantics
The adapter must define:
- how result containers (QueueValue/Set-like) are enumerated into AtomIDs
- identity rule for dedup
- supporting_refs that allow replay and audit

### 14.4 Ranking tiers
- metadata-only ranking pre-materialize
- richer ranking post-materialize
Rank policies may only reference available features.

---

## 15) Exported implementation artifacts in this pack

This export pack includes the actual machine-readable schemas and fixtures we generated:

### 15.1 Downloaded bundle
- `cairnpath_mesh_bundle_v0_4/` directory (schemas + fixtures + validator)
- This pack adds documentation that integrates the earlier storage/compute mesh spec with CairnPath.

### 15.2 Included schema files (v0.4)
Envelope:
- `schemas/envelope/frame.v0.jsonschema.json`

CairnPath:
- `schemas/cairn/context.v0.jsonschema.json`
- `schemas/cairn/step.v0.jsonschema.json`
- `schemas/cairn/line.v0.jsonschema.json`
- `schemas/cairn/result.v0.jsonschema.json`
- `schemas/cairn/materialize.v0.jsonschema.json`

Policy:
- `schemas/policy/cairn_limits.v0.jsonschema.json`

Docs/tools:
- `docs/cairnpath_v0.md`
- `tools/validate.py`
- `fixtures/*.frame.json`

---

## 16) Key lessons we should explicitly export (so we don’t forget)

### Lesson A — Frontier cap is not LIMIT
Database LIMIT controls returned rows/paths; Cairn cap controls the **intermediate working set** each hop. Confusing these recreates blow-ups in production.

### Lesson B — Exploration is a product object
A CairnLine is a signed, diffable program: we can edit step 7 without rewriting the whole expedition.

### Lesson C — Lazy materialization is a privacy + performance primitive
Compute cheap metadata first; only materialize deeper properties when required by later steps.

### Lesson D — Proof beats incentives
Reward can be layered later, but proof-carrying events are the root of legitimacy.

### Lesson E — Upstream diversity, downstream invariants
Adapters are thin; our invariants (TriRPC+AUM+Policy+Evidence+Append-only replay) are what create coherence.

---

## 17) Running backlog (prioritized, exportable)

### P0 — Lock the core contracts
1) AtomID URI scheme standard (`neo4j://…`, `atomspace://…`, `kb://…`) + canonical equivalence mapping hook  
2) Neo4j “golden queries” doc: exact APOC configs per opcode and returned column shapes  
3) AtomSpace extraction micro-spec: container→list enumeration method, identity rule, replay refs  
4) Rank policy schema: what features are legal pre/post materialize  
5) Conformance harness: run the same CairnLine over multiple engines and compare outputs + telemetry

### P1 — Operationalizing the mesh
6) Replication policy DSL formalization (replicas, acks, retention, compaction checkpoints)  
7) Key epoch + membership change rules formalization  
8) FogCompute receipt signing + verification decision rules (dispute workflow)  
9) GitOps module for TopoLVM + standard mount contract installer

### P2 — Product surfaces
10) CairnLine editor UI: step diff, rerun from step N, branch line, compare lines  
11) Audit viewer: show policy decisions + proofs + receipts + materialization triggers  
12) Education workflows: peer review trails as CairnLines + evidence objects

---

## 18) Self-critique (exported)

### Strong
- We unified mesh diversity under a small set of verbs and made proof-carrying events first-class.
- We introduced CairnPath to solve the real graph-product problem: bounded exploration with replayable step history.
- We produced machine-validated schemas + fixtures + validator tooling (not just prose).

### Weak
- The Neo4j and AtomSpace adapters are specified at contract level, but we have not yet published a fully runnable “golden query + expected output shape” suite for each opcode.
- We have not yet locked a single universal AtomID URI scheme and equivalence mapping policy, which is necessary for cross-engine replay comparability.

### Best remediation
- Publish the adapter golden suites and AtomID scheme first, then build conformance tests. That prevents drift across implementations.

---

## 19) Quick start: validate schemas/fixtures

From the extracted bundle directory:

```bash
python3 -m pip install jsonschema
python3 cairnpath_mesh_bundle_v0_4/tools/validate.py
```

---

**End of export context pack.**
