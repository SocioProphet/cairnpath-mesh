# CairnPath Conformance Rules v0

Conformance defines what it means for two CairnPath executions to be semantically equivalent.

## Normalization first

Backend-native objects are not conformance artifacts. Neo4j nodes, Cypher rows, APOC paths, AtomSpace Atoms, Atomese groundings, and backend handles MUST be normalized to CairnPath EntityRefs before comparison.

## Frontier comparison

A frontier is an ordered list of EntityRefs.

By default, conformance requires exact ordered equality of EntityRef `canonical` values.

Order-insensitive comparison is allowed only when a fixture explicitly declares `rank_policy_id = none` and the step is not capped by TopK.

## Digest comparison

Frontier digests MUST be computed from canonical ordered frontier content using the declared FrontierDigest schema. If a digest includes scores or snapshot refs, those inclusions MUST be declared in the digest object.

## Optional attachments

If optional attachments are replay-critical, conformance MUST compare attachment digests. If not replay-critical, attachments are compared only as materialized evidence and not as frontier semantics.

## Ranking

Rank policies MUST be versioned. If two executions use different rank policy versions, their traces are not equivalent.

Ties MUST be broken by EntityRef `canonical` lexicographic ordering unless the fixture declares a stricter rule.

## Backend variance

Backend variance is allowed only before normalization. After normalization, StepTrace comparison is exact unless the fixture explicitly declares a tolerance.

Allowed tolerance fields may include:

- elapsed time,
- backend db hits,
- cache hits,
- backend query fingerprint differences across adapter versions.

Not tolerated by default:

- different frontier canonical ordering,
- different frontier digest,
- different cap-hit status,
- different optional miss semantics,
- different materialization target set.

## Golden traces

A golden trace SHOULD include:

- input Context,
- CairnLine,
- per-step StepTrace,
- final Result,
- expected FrontierDigest values,
- policy reference,
- backend adapter version.

## Exhaustive versus bounded mode

Bounded mode is default. Exhaustive mode is allowed only when explicitly declared by policy and MUST be marked unsafe for large or unconstrained graphs.
