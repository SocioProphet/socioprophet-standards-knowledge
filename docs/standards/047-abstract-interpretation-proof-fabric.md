# 047 — Abstract Interpretation Proof Fabric

## Status

**Draft.** Semantic-only standard. This document does **not** change TriTRPC transport bytes, schema/context IDs, Avro payload bytes, JSON-LD context IDs, or released runtime schemas.

This standard defines the verification calculus behind cross-lane proof artifacts. It extends the Cross-Lane Artifact Canon by specifying how Event-IR, ProofArtifact, DecisionArtifact, ProofPack, TemporalProfile, and TrustProfile relate to abstract interpretation, proof domains, widening, precision, and replay.

## Purpose

SocioProphet has many proof-bearing lanes: knowledge, identity, capability, agent execution, runtime governance, entity analytics, security, platform evaluation, and public-safe explanation. These lanes must not drift into unrelated proof vocabularies.

This standard states the common rule:

> Security verification and knowledge commons governance are both reachability-under-policy problems over typed event streams.

## Non-goals

This standard does **not**:

- replace Event-IR;
- replace ProofArtifact, DecisionArtifact, ProofPack, TrustProfile, or TemporalProfile semantics;
- define TriTRPC framing;
- define a new artifact family;
- require fixture regeneration;
- mandate one solver or one abstract domain implementation.

## Core model

A lane is compliant when it can describe its high-consequence checks as:

\[
\mathrm{Reach}(S_0,T_E) \subseteq P
\]

where:

- \(S_0\) is the initial state set;
- \(T_E\) is the transition relation induced by Event-IR or equivalent typed event inputs;
- \(P\) is the safe/admissible policy region.

The lane MAY implement this with simple deterministic rules, static validators, abstract interpretation, SMT, graph search, proof-carrying receipts, or a mixed method. If it claims abstract-interpretation proof semantics, it MUST expose the abstract domains and precision posture in the resulting ProofArtifact or DecisionArtifact mapping.

## Abstract interpretation contract

A proof-producing analyzer SHOULD be described by:

- a concrete state space \(S\);
- an abstract domain \((A,\sqsubseteq)\);
- abstraction and concretization maps \(\alpha,\gamma\);
- sound abstract transformers \(F^\#\);
- optional widening \(\nabla\) and narrowing operators;
- a precision/budget profile.

Soundness expectation:

\[
F(X) \subseteq \gamma(F^\#(\alpha(X))).
\]

A result MUST NOT imply that all concrete behavior was enumerated unless the analyzer actually performed complete concrete enumeration. Approximate proofs MUST declare approximation and precision metadata.

## Required proof-domain classes

When applicable, proof artifacts SHOULD classify domains using the following vocabulary:

| Domain class | Use |
|---|---|
| `interval` | scalar numeric bounds |
| `sign` | sign-only numeric reasoning |
| `octagon` | weak relational constraints such as \(x-y\le c\) |
| `polyhedra` | linear constraints \(Ax\le b\) |
| `nnc_polyhedra` | linear constraints with strict inequalities / open facets |
| `congruence` | modular counters, nonces, sequence numbers, epochs |
| `grid` | multi-dimensional congruence domains |
| `sharing` | alias / may-share / identity ambiguity |
| `linearity` | exactly-once resource use |
| `affinity` | at-most-once resource use |
| `escape` | non-escape / containment proofs |
| `lattice` | policy, authority, clearance, trust, or admissibility ordering |
| `hypergraph` | n-ary governed relation reachability |
| `smt_backstop` | countermodel search or bit-vector backstop |

Lanes MAY add domain classes, but SHOULD map them into this vocabulary when crossing lane boundaries.

## ProofArtifact binding

A ProofArtifact that uses this standard SHOULD include:

- `claim`;
- `status` in `PROVED`, `VIOLATION`, `INCONCLUSIVE`;
- `inputs` with stable hashes and policy/version refs;
- `domains` using the domain-class vocabulary above;
- `diagnostics` with iteration, widening, duration, and budget data where available;
- `precision` for approximation, downgrade, loss, or uncertainty posture;
- `schedule` for widening/checkpoint behavior where applicable;
- `witnesses` when proved;
- `counterexample` and/or `violations` when violated;
- replay refs or hooks when available.

If a lane emits DecisionArtifact or ProofPack rather than a raw ProofArtifact, it SHOULD map these fields into the cross-lane canon.

## Widening and schedule semantics

Analyzers that use widening MUST expose enough metadata for replay and review:

- widening operator name or profile;
- iteration count;
- widening count;
- checkpoint schedule;
- precision effect or downgrade where available.

A base-e schedule MAY be used for long-running or streaming checks:

\[
n_k = \lceil e^k \rceil.
\]

A lane that uses a different schedule SHOULD identify it by profile name and parameters.

## Congruence and bounded modular evidence

Lanes that analyze nonces, handles, sequence numbers, counters, replay epochs, or namespace-reserved identifiers SHOULD use congruence or grid semantics when equality or range reasoning is insufficient.

A bounded stream check may use:

\[
x \equiv n_0 + k\delta \pmod m
\]

with explicit bound \(k\le K\). The bound MUST be recorded when it materially affects the result.

## Linearity, affinity, and escape

Secrets, votes, grants, delegations, handles, and export rights MAY be modeled as linear or affine capabilities.

If a result depends on non-duplication or non-escape, the proof artifact SHOULD identify:

- the protected resource or authority;
- the declared scope;
- the boundary or jurisdiction;
- the witness or absence of forbidden crossing;
- any allowed witnessed transfer.

Security reading: a key or handle must not escape its HSM or runtime scope.  
Governance reading: authority, quorum, consent, or publication right must not escape its declared scope.

## Topos and sheaf interpretation

This standard permits a topos-level interpretation for cross-lane locality and admissibility.

- Observation stages form a category \(\mathcal{C}\).
- Local knowledge/security state is a presheaf \(K:\mathcal{C}^{op}\to\mathbf{Set}\).
- Policies are subobjects \(P\hookrightarrow K\).
- Evidence sufficiency is represented by a coverage discipline, optionally a Grothendieck topology.
- Admissibility closure MAY be represented by a Lawvere--Tierney topology \(j:\Omega\to\Omega\).
- A proof artifact is a compatible family of local witnesses or a global witness section.

Lanes are not required to implement topos machinery. The topos reading is the formal semantic interpretation for why local evidence, gluing, export, and public-safe proof packaging must remain explicit.

## Hypergraph interpretation

High-consequence decisions SHOULD be represented as n-ary relations when binary edges lose essential context.

A decision hyperedge may bind:

- actor;
- claim/action;
- policy;
- scope;
- evidence refs;
- temporal profile;
- trust profile;
- artifact refs;
- replay refs;
- result/status.

This aligns the proof fabric with boundary-centric hypergraph, MeshRush, Entity Analytics, and graph-native operational surfaces.

## Compliance rules

A lane or artifact family is compliant with this draft when it:

1. reuses Event-IR / ProofArtifact / DecisionArtifact / ProofPack / TrustProfile vocabulary rather than creating a shadow proof family;
2. identifies the policy region or invariant being checked;
3. identifies the domain classes used for any abstract-interpretation-style result;
4. records precision, budget, widening, or downgrade metadata where relevant;
5. emits witnesses for proved claims and counterexamples or violation traces for failed claims where available;
6. treats security containment and governance admissibility as the same class of state-transition proof problem;
7. preserves replay hooks or stable input hashes when the artifact crosses a trust boundary.

## Change-control note

Because this standard is semantic-only, adding it does not require fixture regeneration. Any future schema, Avro, JSON-LD, or transport binding that changes bytes MUST update fixtures, verifiers, and round-trip checks in the same PR or clearly mark the change as draft and non-enforceable.
