# Neo4j/APOC Example: Sequence Expansion and Bounded Frontier

This example demonstrates the difference between backend-native sequence expansion and CairnPath bounded-frontier semantics.

## Toy graph

```cypher
MATCH (n:Seq) DETACH DELETE n;

CREATE (u:Seq:User {name:"alice"})
CREATE (d:Seq:Device {id:"dev1"})
CREATE (p:Seq:Process {name:"procA"})
CREATE (f:Seq:File {path:"/tmp/x"})
CREATE (pkg:Seq:Package {name:"pkg1"})
CREATE (s:Seq:Signer {id:"sig1"})

MERGE (u)-[:LOGGED_IN_TO]->(d)
MERGE (d)-[:RAN]->(p)
MERGE (p)-[:OPENED]->(f)
MERGE (f)-[:IN_PACKAGE]->(pkg)
MERGE (pkg)-[:SIGNED_BY]->(s);
```

## APOC sequence expansion

```cypher
MATCH (u:User {name:"alice"})
CALL apoc.path.expandConfig(u, {
  sequence: "LOGGED_IN_TO>,Device|RAN>,Process|OPENED>,File|IN_PACKAGE>,Package|SIGNED_BY>,Signer",
  beginSequenceAtStart: true,
  bfs: true,
  uniqueness: "NODE_GLOBAL",
  maxLevel: 6,
  limit: 1000,
  optional: false
}) YIELD path
RETURN path;
```

## CairnPath interpretation

The same operation should be represented as a CairnLine with explicit steps:

```text
START(User{name=alice})
SEQUENCE_EXPAND([
  LOGGED_IN_TO -> Device,
  RAN -> Process,
  OPENED -> File,
  IN_PACKAGE -> Package,
  SIGNED_BY -> Signer
])
DEDUP(identity)
RANK(rank_policy_id=lexicographic_entity_ref)
TOPK(k=1000)
MATERIALIZE(mode=metadata_only)
```

## Important distinction

APOC `limit` limits the returned expansion result according to APOC traversal behavior. CairnPath `cap_k` is a framework-level per-hop or per-substep frontier invariant.

A compliant CairnPath Neo4j adapter may compile simple sequence expansions to APOC, but it must still emit StepTrace evidence showing:

- input frontier count,
- raw expanded count,
- deduplicated count,
- final frontier count,
- whether the cap was hit,
- backend query fingerprint.

## Bounded frontier pattern

When per-hop TopK semantics are required, the adapter should use explicit hop-by-hop expansion or an equivalent controlled executor rather than relying on final result `LIMIT`.

```cypher
:param K => 20;

MATCH (u:User {name:"alice"})
WITH [u] AS frontier0, [] AS visited0

CALL {
  WITH frontier0, visited0
  UNWIND frontier0 AS x
  MATCH (x)-[:LOGGED_IN_TO]->(y:Device)
  WHERE NOT elementId(y) IN visited0
  WITH DISTINCT y
  ORDER BY elementId(y)
  LIMIT $K
  RETURN collect(y) AS frontier1, visited0 + [z IN collect(y) | elementId(z)] AS visited1
}

CALL {
  WITH frontier1, visited1
  UNWIND frontier1 AS x
  MATCH (x)-[:RAN]->(y:Process)
  WHERE NOT elementId(y) IN visited1
  WITH DISTINCT y
  ORDER BY elementId(y)
  LIMIT $K
  RETURN collect(y) AS frontier2, visited1 + [z IN collect(y) | elementId(z)] AS visited2
}

RETURN size(frontier0) AS f0, size(frontier1) AS f1, size(frontier2) AS f2;
```

This is intentionally verbose. CairnPath exists so users do not have to hand-author this structure for every investigation.
