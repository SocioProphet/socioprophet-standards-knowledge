# 046 — Cross-Lane Field Alias Matrix

## Status

**Draft.** This matrix defines semantic aliases across SocioProphet runtime, knowledge, entity, capability, platform, and product evidence surfaces.

This document is normative for semantic mapping and non-breaking for existing schemas.

Companion standard: `045-cross-lane-artifact-canon.md`.

## Purpose

Different lanes use different serialization names for overlapping concepts. This matrix prevents semantic drift while preserving released schema compatibility.

It maps lane-specific field names to shared semantic slots used by `DecisionArtifact`, `ProofPack`, `TemporalProfile`, `TrustProfile`, identifier taxonomy, and bridge reference rules.

## Field alias matrix

| Semantic canon | Meaning | Runtime / AgentPlane examples | Knowledge Context examples | Entity / legal-entity examples | Capability Fabric examples | Platform / UI examples | Notes |
|---|---|---|---|---|---|---|---|
| `artifact_kind` | Artifact or object kind | `kind` | schema title / object family | proof artifact kind, designation event kind | receipt type, realization kind | manifest kind, catalog item kind | Runtime uses explicit `kind`; knowledge often uses schema class. |
| `object_id` | Stable object identifier | bundle-local IDs, artifact-local IDs | `note_id`, `claim_id`, `annotation_id`, `edge_id`, `prov_id` | `entity_id`, `source_record_id`, `designation_event_id`, `evidence_id` | function ID, realization ID, receipt ID | `layer_id`, fixture IDs, workbench IDs | Keep object-specific names but map semantics. |
| `artifact_ref` | Reference to an artifact | `runArtifactRef`, `replayArtifactRef`, `promotedObjectRef`, stdout/stderr refs | `ArtifactRef` | `storage_uri`, evidence refs, source refs | payload digest / artifact receipt refs | fixture digest, source receipt ref, manifest ref | Prefer typed refs over unclassified strings. |
| `provenance_ref` | Reference to provenance / lineage | upstream artifact refs, run refs | `ProvenanceRef` | source lineage refs, `source_record_id` | receipt lineage refs | source receipt refs, provenance blocks | Should resolve to inspectable lineage. |
| `actor_ref` | Human, agent, service, authority, or issuer | executor, reviewer, service account, bridge actor | `ActorRef`, `asserted_by`, `created_by`, provenance `actor` | reviewer, analyst, source authority, issuer | realization owner / authority | operator, workbench actor, catalog publisher | Runtime should expose actor refs more consistently over time. |
| `subject_ref` | Primary decision subject | bundle, chosen executor, mounted path, provider route | claim subject, edge subject | entity, source record, relationship statement | function / capability / realization | layer, feed item, content card, route | For two-sided decisions pair with `object_ref`. |
| `object_ref` | Decision target or related object | executor, output artifact, route target | edge object, artifact target | related entity, designation target | realization target | tile manifest, destination, source | Optional for unary decisions. |
| `captured_time` | When artifact was captured or emitted | `capturedAt` | sometimes `created_at` if capture-like | capture time for evidence/proof objects | receipt timestamp | generated-at / emitted-at | Capture is not necessarily occurrence. |
| `created_time` | When object was created | bundle metadata `createdAt` | `created_at` | object creation time | function/profile creation metadata | content/item creation time | Keep separate from capture. |
| `updated_time` | When object was updated | state update time | `updated_at` | update/review time | profile update metadata | last updated | Optional. |
| `occurred_time` | When underlying activity occurred | run start/end or event time when present | provenance `occurred_at` | event occurrence time | invocation timestamp | observed event time | Strongest audit time when available. |
| `asserted_time` | When claim/relation was asserted | n/a | `asserted_at` | statement assertion time | policy assertion time if modeled | governance assertion time | Knowledge-native. |
| `validated_time` | When claim/relation was validated | validation artifact capture/check time | `validated_at` | review/adjudication time | validation receipt time | readiness validation time | Optional. |
| `observed_time` | When fact was observed | adapter observation time | provenance observation when modeled | `observed_at` | telemetry observation time | catalog/API observation time | Entity and platform surfaces use this often. |
| `retrieval_time` | When source material was retrieved | artifact fetch time | import provenance time | `retrieval_time` | dependency/source retrieval time | catalog loaded time | Important for freshness. |
| `effective_start` | Start of validity/effectivity | bundle/version validity start if modeled | n/a | `effective_from`, `valid_from` | capability/profile validity start | layer/status validity start | Entity-native but broadly useful. |
| `effective_end` | End of validity/effectivity | bundle/version validity end if modeled | n/a | `effective_to`, `valid_to` | capability/profile validity end | layer/status validity end | Entity-native but broadly useful. |
| `status` | Lifecycle/result state | `status`, `valid`, check outcomes | validation `status` | review state, designation status | outcome / receipt status | safety status, production-ready state | Do not collapse status with admissibility. |
| `result` | Decision result | success/failure, chosen/rejected | validated/rejected/contested | allowed/review/blocked/reversed | outcome | live/fallback, safe/unsafe, placeholder/non-production | Prefer explicit decision result for high-consequence artifacts. |
| `checks` | Structured validation checks | `checks` in `ValidationArtifact` | validators / validation notes | screening/review checks | gate checks | readiness checks, smoke tests | Preserve structured details. |
| `confidence` | Probabilistic or analyst confidence | not central for most runtime artifacts | `assertion.confidence` | statement or relation confidence | proof-strength-adjacent but distinct | score/confidence labels | Confidence is not permission. |
| `validation_state` | Proposed/validated/rejected state | `valid`, checks, lifecycle state | validation `status` | `review_state`, designation caution state | validation receipt class | readiness state | Semantic alias, not forced rename. |
| `review_state` | Human or governance review posture | `reviewSessionRef`, session status | validators / notes | analyst review state | human-attested or review-required proof profile | trust-center review labels | Useful cross-lane addition. |
| `admissibility_state` | Whether action/link/export is allowed | placement allowed/rejected, side-effect allowed/blocked | validation/gate status when modeled | allow/review/block policy gate | controllability and policy gates | production-ready / placeholder / disabled | Separate from evidence strength. |
| `rights_profile` | Publication, retention, redistribution, or license constraints | license policy, artifact policy refs | artifact policy or provenance refs | `RightsProfile`, license refs | capability policy refs | attribution, license refs | Key for public outputs and catalogs. |
| `freshness_profile` | Freshness/staleness expectation | run recency, replay freshness | import/provenance recency | source-family freshness expectations | realization freshness | `freshness`, generated-at status | Promote from local metadata to trust capsule. |
| `receipt_semantics` | Receipt obligation / receipt kind | receipt refs, run/replay/promotion receipts | provenance/signature records | proof/export receipts | `ReceiptSemantics`, `PROOF_ARTIFACT` | source receipt refs | Capability Fabric authority. |
| `controllability` | Degree of trusted execution control | executor/backend posture, side-effect flags | n/a unless capability-backed | local/private/protected execution posture | `ExecutionControllabilityProfile` | production-ready / fallback / fixture-only | Bounds proof claims. |
| `proof_strength` | Allowed strength of proof claim | evidence artifact strength | validation/provenance strength | proof artifact strength | `ProofStrengthProfile` | public-safe proof label | Must not exceed controllability. |
| `evidence_refs` | Supporting or contradicting evidence | stdout/stderr refs, upstream artifacts, evidence schema refs | `evidence`, anchors, `ArtifactRef` | `EvidenceObject`, source record refs | receipt payload digest / evidence refs | fixture digest, source receipt refs | Evidence may support or contradict. |
| `policy_ref` | Policy, gate, rule, or policy-pack reference | `policyPackRef`, policy refs, side-effect gates | validation/governance refs | blocking policy, policy version, rights policy | policy hook refs | safety policy label | Consequential decisions should cite this. |
| `receipt_ref` | Durable receipt / decision record ref | `receiptRef`, `promotionReceiptRef`, `sourcePromotionReceiptRef` | `ArtifactRef` or provenance-generated artifact | proof/export receipt refs | receipt identifier | source receipt ref | Distinct from generic URI. |
| `session_ref` | Session lifecycle reference | `sessionRef`, `reviewSessionRef` | n/a | review session, operator session | invocation/session ref | workbench session | Runtime-native today. |
| `replay_ref` | Replay artifact or replay hook | `ReplayArtifact`, `replayArtifactRef`, replay inputs | provenance `run_id` may contribute | proof replay hooks | replay control profile | reproducibility fixture refs | Cross-lane bridge point. |
| `signature_refs` | Signatures or attestations | receipt signatures when present | provenance `signatures` | proof signatures / attestation refs | signature refs in receipts | signed release/status refs | Strongest proof support when present. |
| `witness_refs` | Human/system witnesses | reviewer, audit refs | validators | analyst/reviewer/witness | human-attested proof | trust-center witness refs | Distinct from signatures. |
| `uri` | Locator | path refs, `sshRef`, artifact directory | `ArtifactRef.uri`, `ProvenanceRef.uri` | `source_url`, `storage_uri` | endpoint/profile URI | catalog URL, source URL | URI is not identity. |
| `safe_summary` | Public-safe explanation | artifact summary / redaction summary | validation notes | proof explanation | receipt summary | UI explanation panel | Must not expose restricted internals. |
| `counterexample_refs` | Contradiction, failure, or blocking evidence | rejected executors, failed checks | contradiction evidence / contested claim | blocked edge, non-escape violation, sanctions caution | failed receipt/gate refs | placeholder/safety advisory refs | Do not average away protected contradictions. |
| `safe_alternative_refs` | Approved bounded alternative | fallback executor, record-only mode | alternative claim/note refs | coarsened export, bounded cohort | lower-controllability realization | demo fallback, placeholder-safe UI | Required when blocking should still preserve usefulness. |

## Identifier classes

The following identifier classes MUST NOT be treated as interchangeable solely because they are strings:

| Identifier class | Examples | Notes |
|---|---|---|
| Object ID | `claim_id`, `entity_id`, `layer_id` | Stable object identity within a domain. |
| Artifact ref | `ArtifactRef`, `runArtifactRef`, fixture digest refs | Points to an artifact object or record. |
| Provenance ref | `ProvenanceRef`, lineage refs | Points to lineage/provenance. |
| Source-record ref | `source_record_id`, source refs | Points to upstream source observation. |
| Session ref | `sessionRef`, `reviewSessionRef` | Runtime/review lifecycle identity. |
| Receipt ref | `receiptRef`, `promotionReceiptRef`, source receipt ref | Durable receipt/decision reference. |
| Replay ref | `replayArtifactRef`, replay hook | Reconstructability handle. |
| URI | `source_url`, `storage_uri`, `ArtifactRef.uri` | Locator, not necessarily identity. |

New schemas SHOULD name identifier classes explicitly.

## Required mapping rule

Any new artifact, evidence, receipt, proof, catalog, release, or UI evidence surface that crosses lane boundaries SHOULD include a short mapping note that states:

1. which fields map to `DecisionArtifact`;
2. which fields map to `ProofPack`, if export/review packaging is involved;
3. which time fields map to `TemporalProfile`;
4. which trust/admissibility/proof fields map to `TrustProfile`;
5. which identifiers are object IDs, artifact refs, provenance refs, source refs, session refs, receipt refs, replay refs, or URIs;
6. whether any proof claim is bounded by Capability Fabric controllability or proof-strength classes.

## Non-breaking rule

Released fields SHOULD NOT be renamed in place to satisfy this matrix.

If a lane wants to converge field names, it MUST do so through the lane's normal schema/versioning process.

## Transport note

This matrix does not change TriTRPC framing, Avro payload bytes, JSON-LD context IDs, schema/context IDs, AEAD/AAD semantics, or fixture vectors.

Any future byte-affecting binding MUST update fixtures, verifiers, and round-trip checks in the same PR or remain explicitly draft-only.
