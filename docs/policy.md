# CairnPath Policy Semantics v0

CairnPath traversal is policy-gated. Bounded frontier traversal reduces risk, but it does not remove the need for hard execution and materialization controls.

## Policy caps

A CairnLimits policy SHOULD bound:

- default and maximum frontier cap,
- maximum hops,
- allowed opcodes,
- maximum materialization bytes,
- maximum elapsed time,
- allowed relations,
- allowed predicates,
- allowed uniqueness modes.

## Unsafe traversal

The following are unsafe by default:

- expansion-like steps without cap policy,
- unbounded variable-length path enumeration,
- uniqueness mode `NONE`,
- exhaustive traversal over unknown or high-degree graphs,
- materialization without max bytes,
- backend-local ids as the sole conformance identity.

Unsafe behavior MAY be permitted only if policy explicitly allows it and StepTrace records the unsafe decision.

## Policy decision trace

A StepTrace SHOULD record:

- policy id,
- decision id when available,
- allowed/denied status,
- reason for denial or warning,
- cap applied,
- materialization budget applied.

## Privacy and exfiltration guardrails

Traversal can reveal sensitive relationships even when properties are not materialized. Policy SHOULD therefore apply to navigation predicates as well as materialized fields.

A compliant executor MUST be able to deny traversal over disallowed relations, predicates, or namespaces before expansion occurs.
