# 045 — Cross-Lane Artifact Canon

## Status

**Draft.** This document defines the semantic canon for artifacts, evidence, decisions, receipts, proof bundles, and cross-lane metadata across SocioProphet runtime, knowledge, entity, capability, platform, and product surfaces.

This document is normative for semantic alignment. It does **not** alter TriTRPC framing, byte fixtures, schema/context IDs, Avro payload bytes, JSON-LD context IDs, or released runtime schemas.

## Purpose

SocioProphet now has multiple evidence-producing lanes:

- Knowledge Context artifacts and provenance records.
- Capability Fabric functions, realization profiles, receipts, controllability, and proof strength.
- AgentPlane execution artifacts and domain-specific evidence records.
- Entity Analytics proof artifacts, governed links, merge/export decisions, and safe-output proofs.
- Platform and UI surfaces that expose provenance, receipt refs, fixture digests, safety status, and production-readiness metadata.

This standard prevents those lanes from drifting into separate proof vocabularies. It defines shared semantic nouns and minimum mapping rules while allowing each lane to preserve its own serialization surface.

## Non-goals

This standard does **not**:

- rename released fields in place;
- replace TriTRPC transport semantics;
- replace Capability Fabric semantics;
- replace AgentPlane schemas;
- replace Entity Analytics doctrine;
- freeze a full public `ProofPack` JSON Schema;
- require fixture regeneration.

Schema and transport changes remain separate versioned work.

## Upstream semantic authorities

- TriTRPC owns deterministic transport, envelope framing, AEAD/AAD boundaries, and byte fixtures.
- Knowledge Context owns canonical knowledge artifacts, relation semantics, provenance records, Avro/JSON-LD overlays, and knowledge-store payload contracts.
- Capability Fabric owns protocol-independent capability semantics, realization metadata, receipt semantics, controllability, and proof-strength classes.
- AgentPlane owns bounded execution artifacts, evidence records, replay records, promotion/reversal records, and domain-specific execution evidence schemas.
- Entity Analytics owns governed identity, scoped events, links, merge/unmerge/export decisions, and public-safe proof explanations.

This standard bridges those authorities. It does not supersede them.

## Shared semantic primitives

### Event

An `Event` is a typed observation, workflow transition, execution step, lifecycle transition, or entity-state transition.

Examples include claim lifecycle events, bundle validation, placement, run, replay, promotion, reversal, entity graph transitions, capability invocations, and UI-visible evidence or readiness transitions.

### Claim

A `Claim` is a knowledge assertion, candidate proposition, decision statement, requirement, risk, plan, or fact-like statement that may carry evidence, assertion metadata, validation state, and provenance.

Knowledge Context `Claim` remains the canonical knowledge assertion primitive.

### Entity

An `Entity` is a governed identity, object, actor, institution, artifact subject, legal entity, runtime target, capability realization, or scoped subject whose state can be asserted, linked, reviewed, merged, exported, blocked, or proven.

Entity Analytics remains the authority for scoped identity, identity-prime structure, governed links, and merge/export discipline.

### Relationship

A `Relationship` is a typed governed edge between subjects, objects, artifacts, claims, entities, or scopes.

Knowledge Context `MeriotopographicEdge` remains the canonical knowledge relation primitive. Entity Analytics and legal-entity relationship statements specialize this pattern for governed identity and institutional reference data.

### DecisionArtifact

A `DecisionArtifact` is a proof-bearing artifact that records a consequential decision, transition, validation outcome, execution outcome, promotion, reversal, merge, unmerge, export, suppression, screening decision, placement, routing decision, or review outcome.

Examples include:

- AgentPlane `ValidationArtifact`, `PlacementDecision`, `RunArtifact`, `ReplayArtifact`, `SessionArtifact`, `PromotionArtifact`, and `ReversalArtifact`;
- AgentPlane domain evidence records such as Agent Machine mount, Office artifact, Network Door, external model-provider routing, and Native Assistant bridge evidence;
- Capability Fabric receipt/proof artifacts;
- Entity Analytics merge, export, suppression, review, and proof artifacts;
- GAIA or product-surface catalog evidence when it carries provenance, source receipt refs, fixture digests, readiness state, or safety status.

A `DecisionArtifact` SHOULD expose, semantically:

- artifact kind;
- stable artifact identifier or artifact ref;
- subject/object refs where applicable;
- actor or authority refs where applicable;
- captured or occurred time;
- status/result;
- policy/gate refs where applicable;
- evidence refs;
- provenance refs;
- replay refs or hooks where applicable;
- receipt refs where applicable;
- signature or witness refs where applicable.

### ProofPack

A `ProofPack` is a public-safe packaging profile for review, replay, audit, disclosure, or regulated handoff.

`ProofPack` MUST NOT be treated as a competing proof model. It is a packaging profile over existing proof and receipt authorities, including:

- Capability Fabric `ReceiptSemantics` and `PROOF_ARTIFACT` receipt class;
- AgentPlane evidence and lifecycle artifacts;
- Knowledge Context claims, relations, artifact refs, and provenance records;
- Entity Analytics proof artifacts and safe-output explanations;
- platform release or product-surface evidence where applicable.

A `ProofPack` SHOULD contain decision artifact refs, claim refs, bounded evidence refs, provenance refs, policy refs, replay refs, receipt refs, signature/witness refs, safe summaries, counterexample refs, and safe alternative refs where applicable.

### TemporalProfile

A `TemporalProfile` is the semantic capsule for time fields. It distinguishes captured time, created time, updated time, occurred time, asserted time, validated time, observed time, retrieval time, effective start, effective end, and replay ordering metadata.

### TrustProfile

A `TrustProfile` is the semantic capsule for validation state, checks, confidence, review state, admissibility state, rights, freshness, controllability, proof strength, receipt semantics, signatures, witnesses, and policy refs.

Capability Fabric `ExecutionControllabilityProfile`, `ProofStrengthProfile`, and `ReceiptSemantics` are authoritative inputs to `TrustProfile` for capability realizations.

## Mandatory bridge references

New cross-lane artifacts SHOULD reuse existing Knowledge Context bridge primitives unless a stronger domain-specific ref is justified:

- `ActorRef`;
- `ArtifactRef`;
- `ProvenanceRef`;
- `ProvenanceRecord`.

If a lane uses local identifiers such as receipt refs, session refs, bundle refs, source-record refs, or replay refs, it SHOULD document how those identifiers map into artifact or provenance references.

## Capability Fabric alignment

This standard MUST align to Capability Fabric rather than duplicate it.

| Cross-lane canon | Capability Fabric mapping |
|---|---|
| `DecisionArtifact` | receipt-bearing or proof-bearing decision output |
| `ProofPack` | public-safe packaging profile over `PROOF_ARTIFACT` and related receipts |
| `TrustProfile.receipt_semantics` | `ReceiptSemantics` |
| `TrustProfile.controllability` | `ExecutionControllabilityProfile` |
| `TrustProfile.proof_strength` | `ProofStrengthProfile` |
| runtime realization refs | `RealizationMetadata` |

A node MUST NOT claim proof stronger than its controllability and proof-strength profiles permit.

## AgentPlane evidence alignment

AgentPlane evidence records and lifecycle artifacts SHOULD map into `DecisionArtifact`.

The current known family includes `ValidationArtifact`, `PlacementDecision`, `RunArtifact`, `ReplayArtifact`, `SessionArtifact`, `PromotionArtifact`, `ReversalArtifact`, `BrokerExecutionBundle`, `AgentMachineMountEvidence`, `OfficeArtifactEvidence`, `NetworkDoorPlanEvidence`, `ExternalModelProviderRouteEvidence`, and `NativeAssistantBridgeEvidence`.

AgentPlane remains the execution/evidence authority for these schemas. This standard provides semantic aliases and cross-lane mapping only.

## Entity Analytics alignment

Entity Analytics proof, merge, link, unmerge, suppression, export, and safe-output decisions SHOULD map into `DecisionArtifact`.

A public-safe entity proof bundle SHOULD map into `ProofPack` when it needs to cross boundaries for review, disclosure, replay, or audit.

A high-confidence relation MUST NOT be treated as permission to merge or export unless the relevant policy/admissibility gate allows it.

## Product and UI evidence alignment

Product surfaces that expose governed provenance, safety state, production-readiness state, source receipt refs, fixture digests, attribution, freshness, or placeholder/non-production state SHOULD map those fields into the alias matrix.

This applies to catalog, map, feed, workbench, release, trust-center, and system-card surfaces where evidence is user-visible or operator-visible.

## Serialization policy

This standard is semantic-first and non-breaking.

Existing lanes MAY continue to use released field names such as `capturedAt`, `created_at`, `occurred_at`, `asserted_at`, `validated_at`, `effective_from`, `observed_at`, `receiptRef`, and `source_record_id`.

New schemas SHOULD either use the canonical semantic term directly or explicitly map their field names in the alias matrix.

Released schemas MUST NOT be renamed in place solely to satisfy this canon. Convergence requires normal versioning.

## Identifier taxonomy

This standard distinguishes object identifiers, artifact references, provenance references, source-record references, session references, receipt references, replay references, and URI locators.

A plain string ID is not automatically interchangeable with a receipt ref, session ref, provenance ref, or URI.

New schemas SHOULD name identifier classes explicitly.

## Compliance rules

A new cross-lane artifact is compliant when it:

1. maps consequential decisions to `DecisionArtifact` semantics;
2. maps exported/reviewable proof bundles to `ProofPack` semantics where applicable;
3. maps time fields into `TemporalProfile`;
4. maps validation/admissibility/proof/freshness/rights fields into `TrustProfile`;
5. reuses `ActorRef`, `ArtifactRef`, `ProvenanceRef`, or `ProvenanceRecord` where applicable;
6. documents any identifier class not already covered by this standard;
7. does not claim stronger proof than its controllability and proof-strength posture permits;
8. avoids breaking released field names without a versioned schema change.

## Change-control note

Because this standard does not change transport framing, schema/context IDs, Avro payload bytes, JSON-LD context IDs, or fixture bytes, it does not require TriTRPC fixture regeneration.

Any future schema or transport binding that changes bytes MUST update the relevant fixtures, verifiers, and round-trip checks in the same PR or clearly mark the work as draft and non-enforceable.
