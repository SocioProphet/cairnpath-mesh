# CairnShare Adapter Contract (v0.1)

Every engine adapter MUST implement these surfaces:

## 1) capabilities()
Return a structured description of:
- supported query languages
- enforceable scope primitives (labels/rel-types, atom types/predicates, namespaces)
- enforceable projection primitives (engine-native vs gateway only)
- dangerous ops/procedures list (deny by default)
- inference support (off by default; sandboxed)

## 2) compile_policy(SP)
Translate Share Policy into an engine enforcement plan:
- native grants/roles (if available)
- gateway enforcement rules (projection filtering, clause allowlist)
- hybrid strategy

## 3) dry_run(AB, SP, identity)
Return a Dry-Run Report:
- allowed true/false
- missing actions/scopes/capabilities
- blocked ops/procedures/inference
- human-readable explain[]

## 4) execute(AB, SP, identity)
Run analysis inside sandbox, returning:
- filtered results (projection-enforced)
- Execution Receipt (ER)

## 5) explain(AB, SP)
Human readable “what will happen” for UI and audit.

Security rule: **projection enforcement is mandatory** even if the engine claims property-level security.
