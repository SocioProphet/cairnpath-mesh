# CairnShare (FogMesh Edition)
**Verifiable sharing of graph analyses across AtomSpace, Neo4j, and other graph engines — without granting raw graph access.**

CairnShare packages a shareable “analysis link” as three portable, cryptographic artifacts:
- **Analysis Bundle (AB)**: the analysis program, parameters, scope hints, and projection rules.
- **Share Policy (SP)**: who can run it, what they may access/see, and what actions are allowed.
- **Execution Receipt (ER)**: what actually ran, on what dataset snapshot, under what effective policy, producing what results.

In FogMesh terms: CairnShare is a **Cairn** — a signed, replayable trail marker through a graph/hypergraph.

## Why this exists
Graph systems typically force a false choice:
1) Share raw access (too broad, unsafe), or
2) Export static results (non-reproducible, non-interactive).

CairnShare shares *live analyses* inside a sandbox with explicit scope and projection enforcement, and produces auditable receipts.

## Repo layout
- `spec/` – normative schemas + examples (AB/SP/ER + DryRun report)
- `adapters/` – engine adapter contract + stubs (AtomSpace first)
- `cli/` – reference CLI surface (validate/dry-run/execute/explain)
- `argo/` – Argo Workflows templates (engine-agnostic) + Cron
- `argocd/` – Argo CD Application (GitOps)
- `kustomize/` – deploy base + secret templates
- `monitoring/` – Prometheus rule examples + dashboard stubs
- `docs/` – threat model, FogMesh mapping, engine notes

## Quick start (Argo)
1) Apply template: `kubectl -n cairnshare apply -f argo/workflows/workflowtemplate.yaml`
2) Submit a run: `argo -n cairnshare submit argo/workflows/run.yaml -p engine=atomspace -p repo_url=... -p revision=... -p adapter_image=...`

## Status
This is a **DataWalk-purged, open-source-first** remediation of earlier scaffolding. Next implementation step is the AtomSpace adapter.

## Spec
- Normative rules: `spec/NORMATIVE.md`
- Schemas: `spec/*.schema.json`
- Test vectors: `spec/vectors/`
- Teaching notes: `docs/TEACHING_NOTES.md`
- History: `docs/HISTORY.md`
