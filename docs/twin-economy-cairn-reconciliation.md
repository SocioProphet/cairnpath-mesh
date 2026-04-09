# Twin economy Cairn reconciliation contract (v0.1)

This note defines how the previously proposed standalone `cairn.schema.json` for twin-economy work must be reconciled into the existing CairnPath bundle.

It is intentionally a **reconciliation contract**, not a replacement schema. The goal is to preserve CairnPath as the canonical replay/materialization spine while giving the twin-economy work a safe landing path.

## Why this exists

The twin-economy slice needs replayable decision checkpoints, bounded execution traces, policy-aware materialization, and settlement artifacts.

`cairnpath-mesh` already owns the following concepts:
- TriTRPC frame envelope schema
- CairnPath schemas for `Context`, `Step`, `Line`, `Result`, and `Materialize`
- policy schema `CairnLimits`
- fixtures and validator logic

A new standalone Cairn schema outside this repository would duplicate and likely drift from the existing replay/materialization model.

## Decision

Twin-economy replay artifacts must be expressed as a constrained composition of existing CairnPath concepts.

### Required mapping

#### 1. Decision checkpoint -> `Context`
A twin-economy decision checkpoint must map to `Context`.

Minimum semantic fields to preserve:
- twin scope / domain pack identifier
- time bounds (valid time + transaction time where applicable)
- objective profile identifier
- policy / approval profile identifier
- upstream evidence bundle references
- transport / request correlation identifiers where present

#### 2. Candidate actions and execution trace -> `Step` + `Line`
The selection and execution path for candidate actions must be expressed through `Step` and `Line` rather than a bespoke action-trace structure.

Minimum semantic fields to preserve:
- candidate action identifier
- plan rank / dominance ordering
- preconditions evaluated
- approvals observed
- selected / rejected / deferred disposition
- rollback hook identifiers

#### 3. Outcome / settlement -> `Result`
Observed or derived outcomes after a committed action must map to `Result`.

Minimum semantic fields to preserve:
- expected vs realized effect
- settlement status
- variance / drift summary
- error taxonomy or exception class if failed
- downstream artifact references

#### 4. State projection / durable publish -> `Materialize`
Any durable publish, export, or projection of replay state must map to `Materialize`.

Minimum semantic fields to preserve:
- target storage or publication surface
- projection format
- retention / replay policy reference
- reproducibility bundle references

#### 5. Bounded policy -> `CairnLimits`
Twin-economy execution bounds must be encoded using `CairnLimits` rather than a new limits object.

Minimum semantic fields to preserve:
- frontier / breadth caps
- replay depth caps
- materialization caps
- approval escalation thresholds
- side-effect class restrictions

## What should not be done

- Do not keep a standalone `cairn.schema.json` outside this repo.
- Do not encode twin-economy replay as an ad hoc JSON blob without `Context` / `Step` / `Line` / `Result` / `Materialize` mapping.
- Do not move Cairn semantics into `TriTRPC`; only transport mapping belongs there.
- Do not place replay authority in domain-pack repos.

## Planned follow-on artifacts

1. A worked example fixture for one contested-logistics decision cycle.
2. A field-by-field mapping table from the discarded standalone Cairn draft into CairnPath concepts.
3. Validator cases for bounded replay and materialization under twin-economy rules.
4. A transport note showing how TriTRPC correlation IDs bind to CairnPath `Context`.

## Cross-repo dependencies

- Storage/twin state contracts are defined in `socioprophet-standards-storage`.
- Claim/evidence semantics are defined in `socioprophet-standards-knowledge`.
- Action/approval semantics are defined in `socioprophet-standards-agents` (planned sibling repo).
- Domain-pack semantics are defined in `prophet-domain-twin-economy` (planned domain repo).
- Runtime services consume the reconciled CairnPath model from `prophet-platform`.

## Immediate next step

The next concrete change in this repository should be a worked replay fixture for the contested-logistics slice rather than a large speculative schema rewrite.
