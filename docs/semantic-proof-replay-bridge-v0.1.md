# Semantic-proof replay bridge v0.1

## Purpose

This note defines the narrow replay/materialize bridge between the semantic-proof / replay interoperability work and `cairnpath-mesh`.

`cairnpath-mesh` is the correct home for the replay/materialize-facing semantics of the pack, not for the entire standards or transport surface.

## Why this belongs here

The repository already presents itself as the home for:
- CairnPath schemas
- `Context` / `Step` / `Line` / `Result` / `Materialize`
- policy bounds (`CairnLimits`)
- fixtures and validator logic

That makes it the right replay/materialize lane for the semantic-proof work.

## What this bridge adds conceptually

### 1. Replay handle binding
A replayable semantic-proof artifact should be able to bind to a Cairn/materialize handle without redefining CairnPath itself.

### 2. Proof-bearing materialization
Materialization results should be able to expose:
- replay handle or cairn reference
- worldview or semantic surface root where applicable
- verifier status or proof references

### 3. Boundary discipline
`cairnpath-mesh` should not become the canonical home for the shared proof schemas or transport methods.
It should consume those as external references and bind them into replay/materialize fixtures and validator expectations.

## Deliberate exclusions

This bridge note does not add:
- canonical proof schemas
- shared vocabulary canon
- transport method definitions
- runtime receipt ownership
- policy/rule lowering semantics

## Follow-on

1. keep one worked replay/materialize fixture in-repo
2. add validator expectations for replay-bearing semantic proof refs later
3. bind the shared proof identifiers only after the standards-side schema family widens beyond the first seed
