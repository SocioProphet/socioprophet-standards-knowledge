# 040. Knowledge State Lifecycle (v0.1)

## Status

Proposed baseline for implementation.

## Purpose

This standard defines the minimum state machine for knowledge assets in the SocioProphet Knowledge Context.

It exists to make one distinction explicit:

- not all observed or authored material is canonical,
- promotion into canonical status is a governed transition,
- canonical status can later be superseded, restricted, or rejected.

This standard binds the object taxonomy, promotion rules, and content-space model into one explicit lifecycle.

## Scope

This standard applies to structural knowledge assets represented in the Knowledge Context package, especially:

- `ConversationAsset`
- `DocumentAsset`
- `RunbookAsset`
- `CodeAsset`
- `EvidenceArtifact`
- `PublishedKnowledgeUnit`

This standard does **not** redefine transport framing, execution receipts, or raw evidence custody.

## Canonical lifecycle states

The canonical lifecycle states SHALL be:

1. `ObservedLocal`
2. `Structured`
3. `PromotionCandidate`
4. `Validated`
5. `PublishedCanonical`
6. `Superseded`
7. `Rejected`
8. `SensitiveRestricted`

## State meanings

### `ObservedLocal`
Material exists locally, privately, or provisionally, but is not yet normalized into canonical structural form.

Examples:
- chat transcript
- local note
- raw support conversation
- scratch operational draft

### `Structured`
Material has been normalized into a structural object class and has a durable identifier, but is not yet proposed for canon.

### `PromotionCandidate`
Material has been explicitly proposed for promotion and is awaiting governed review, duplicate checks, scope checks, or policy checks.

### `Validated`
The candidate has passed the required validation gates for its policy scope, but has not yet completed publication into canonical status.

### `PublishedCanonical`
The object has been published into a valid content space and is intended for durable retrieval and reuse.

### `Superseded`
A previously canonical object remains historically relevant but has been replaced by a newer stewarded object.

### `Rejected`
The candidate failed promotion or validation and SHALL NOT be treated as canonical.

### `SensitiveRestricted`
The object exists and may be valid, but its publication or exposure is restricted by policy, privacy, sensitivity, or governance constraints.

## Required transition rules

### Required structural transition
An object SHALL NOT transition from `ObservedLocal` directly to `PublishedCanonical`.

At minimum, the following transitions SHALL be traversed:

`ObservedLocal` -> `Structured` -> `PromotionCandidate` -> `Validated` -> `PublishedCanonical`

### Promotion requirement
A transition into `PublishedCanonical` MUST NOT complete unless:

- provenance is present,
- target content space is valid,
- duplicate or near-duplicate review is complete,
- required policy review is complete,
- the resulting asset class is explicit,
- publication evidence is emitted.

### Supersession rule
A canonical object SHOULD transition to `Superseded` rather than be deleted when a newer stewarded object replaces it.

### Restriction rule
Any object MAY transition to `SensitiveRestricted` when policy permits existence but limits exposure or publication.

### Rejection rule
Any candidate MAY transition to `Rejected` when validation, policy, duplication, contradiction, or sensitivity checks fail.

## Required references

A lifecycle record MUST carry:

- `subjectRef`
- `objectType`
- `state`
- `issuedTimeUtc`
- `scopeRef`
- `provenanceRootRef`

When applicable, it SHOULD carry:

- `contentSpaceRef`
- `validationReceiptId`
- `promotionReceiptId`
- `publicationReceiptId`
- contradiction references

## Content-space binding

A transition into `PublishedCanonical` MUST reference a valid content space.

Assets without a valid target content space MUST NOT be promoted into canonical status.

## Relationship to other standards

- object classes remain defined by the object taxonomy
- promotion gates remain defined by the promotion rules
- content-space governance remains defined by the content-space model
- raw evidence custody remains defined in the storage/evidence standards package
- receipts and execution evidence remain defined outside this repo

## Compliance note

This standard becomes enforceable only when accompanied by:

- `KnowledgeStateLifecycle` structural schema
- `PromotionDecision` structural schema
- any required fixture or roundtrip updates for downstream consumers
