# CairnPath + Hill Proof Fabric

**Status:** v0.1 integration narrative  
**Purpose:** explain CairnPath as bounded traversal, Hill as proof closure, and the shared artifact chain that connects exploration, evidence, and replayable proof.

## 1. Why CairnPath exists

When people wanted a statement to survive conscious memory, they carved it into stone. A cairn is a smaller version of that instinct: a deliberate marker placed where terrain is ambiguous and where the path matters.

CairnPath uses that metaphor literally. A traversal is not a throwaway query string. It is a line of durable markers: each step records what we asked, what it generated, how it was bounded, and why the next step followed. The goal is to preserve the path of reasoning after the immediate human context disappears.

In modern graph and agentic systems, most reasoning evaporates. Queries get rewritten. Logs rotate. Dashboards change. Agents wander and leave only opaque outputs. CairnPath turns exploration into a durable, replayable artifact.

## 2. The mathematical origin: bloom, factorial, exponential

The framework is grounded in the difference between growth with reuse and growth without reuse.

With replacement:

```math
W(N,t)=N^t
```

Without replacement:

```math
U(N,t)=N^{\underline{t}}=N(N-1)\cdots(N-t+1)=\frac{N!}{(N-t)!}
```

The bridge is:

```math
\frac{U(N,t)}{W(N,t)}=\prod_{i=0}^{t-1}\left(1-\frac{i}{N}\right)
```

This is the suppression factor between naive exponential bloom and uniqueness-aware traversal. A log expansion gives the useful approximation:

```math
\prod_{i=0}^{t-1}\left(1-\frac{i}{N}\right)\approx \exp\left(-\frac{t(t-1)}{2N}\right)
```

The approximate crossover occurs at:

```math
t^*\approx \sqrt{2N}
```

Before this point, uniqueness does not reduce much. After it, repeated discoveries dominate. In real graphs the effective pool size is contextual, not global, so collisions often arrive earlier than the clean model predicts.

## 3. Runtime measurements

At hop `t`, CairnPath measures:

- `f_t`: frontier size entering the hop
- `g_{t+1}`: generated candidates before dedup
- `u_{t+1}`: unique candidates after dedup
- `r_{t+1}`: retained candidates after ranking and TopK

Derived metrics:

```math
b_eff(t)=\frac{g_{t+1}}{\max(1,f_t)}
```

```math
eta(t)=\frac{u_{t+1}}{\max(1,g_{t+1})}
```

```math
mu(t)\approx\frac{g_{t+1}}{\max(1,u_{t+1})}
```

`mu` is the path-multiplicity / duplication factor. It exposes the hidden failure mode where many paths or match contributions collapse onto the same few nodes. High `mu` means path materialization is dangerous even if unique nodes remain bounded.

## 4. CairnPath execution model

CairnPath runs a sequence of `CairnStep`s over a bounded `Frontier`.

The invariant after every hop is:

```text
candidates = EXPAND(frontier, step.args)
candidates = DEDUP(candidates)
candidates = RANK(candidates)
frontier  = TOPK(candidates, K)
```

This makes deep traversal a budgeted process. The framework does not claim that graph growth stops being combinatorial. It refuses to pay the combinatorial bill by default.

Core controls:

- `K`: frontier cap / beam width
- `B_ops`: candidate-operation budget
- `S_max`: execution-state budget for optional branching
- `mu_max`: path-multiplicity ceiling
- novelty threshold: stop or pivot when discovery collapses
- fanout spike detector: shrink `K` when `b_eff` shocks the run

## 5. Why this matters for AI and agent graphs

Agents do not know the final query at step zero. They probe, revise, branch, and backtrack. Without explicit bounds, they can wander into infinite neighborhoods, hub regions, optional-state blowups, and high-path-multiplicity regions.

CairnPath gives an agent three things:

1. **A plan it can edit:** the `CairnLine`.
2. **A trace it can observe:** the `StepTrace`.
3. **Policies it cannot silently bypass:** caps, budgets, stop reasons, and action registries.

A planner agent can read StepTrace and propose patches:

- high `mu`: force node-only evidence, increase duplicate penalty, reduce `K`
- fanout spike: tighten relation selector, push down filters, shrink `K`
- novelty plateau: pivot relation class, add diversity gate, change ranking weights
- budget pressure: project stop, ask for batch profile, or narrow scope

## 6. Hill Proof Fabric integration

CairnPath explores and selects evidence. Hill closes the proof.

Hill turns Event-IR into constraints, runs abstract-interpretation domains, and emits replayable proof artifacts or minimal counterexamples. CairnPath supplies the bounded evidence trail that feeds Hill.

The bridge objects are:

- `EvidenceSlice`: the selected event/subgraph subset, content-addressed and linked to the CairnPath run
- `ClaimSpec`: the formal claim, assumptions, preferred domains, budgets, and witness/counterexample contract
- `ProofArtifact`: the Hill output, linked back to StepTrace and EvidenceSlice hashes

Together:

```text
Event-IR -> Evidence graph overlay -> CairnLine traversal -> StepTrace -> EvidenceSlice -> ClaimSpec -> Hill proof -> ProofArtifact
```

This creates a chain of custody from exploration to proof.

## 7. Platform role

Within the SocioProphet platform, `cairnpath-mesh` owns the bounded traversal and proof-orchestration semantics:

- CairnLine / CairnStep runtime semantics
- StepTrace schema and validator rules
- EvidenceSlice generation
- ClaimSpec bridge to Hill proof claims
- backend adapters such as Neo4j and AtomSpace

Neighboring repos keep their existing responsibilities:

- TriTRPC: deterministic transport and envelopes
- agentplane: execution lifecycle, governance, evidence, replay
- standards repos: canonical schemas and conformance profiles
- sociosphere: workspace and multi-repo orchestration

## 8. What is world-class here

The distinctive contribution is not simply traversal. The contribution is **bounded progressive traversal with proof-carrying traces**.

CairnPath makes these first-class:

- bounded frontier semantics
- path-multiplicity (`mu`) as an operational hazard metric
- optional branching as an explicit state-budgeted algebra
- deterministic ranking and replay
- trace-first cross-backend comparability
- bridge from exploration to formal proof through EvidenceSlice and ClaimSpec

Most systems offer traversal, alerts, or proof in isolation. CairnPath + Hill integrates exploration and proof into one artifact chain.

## 9. Current spec surface

Locked or newly introduced in this branch:

- `StepTrace v0.2`: per-hop audit/evidence record
- `EvidenceSlice v0.1`: bridge object from traversal to proof
- `ClaimSpec v0.1`: formal claim object for Hill analysis

Next spec surfaces to lock:

- `actions.v1`
- `stop_reasons.v1`
- `policy_profiles.v1`
- `trace_validator.v1`

## 10. Minimal narrative positioning

CairnPath is a stone-path for machine reasoning: each step is durable, bounded, and replayable. Hill is the proof engine that takes those stones and closes claims. Together they let humans and agents explore complex evidence spaces without losing the path, and then prove what happened under explicit assumptions.
