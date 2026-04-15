# 042 — Capability Fabric Delivery and Receipts (v0.1 draft)

## Status

**Draft.** This document defines operational delivery guarantees, side-effect classes, streaming and cancellation semantics, and receipt obligations for Capability Fabric realizations.

This document is normative. It uses RFC-style language:
- **MUST / MUST NOT** = mandatory for compliance
- **SHOULD / SHOULD NOT** = strongly recommended
- **MAY** = optional

## Purpose

This document standardizes how a realization expresses:
- how delivery is attempted
- what side effects it may produce
- what streaming model it uses
- what cancellation guarantees it provides
- what receipts it MUST emit

Delivery and receipts are protocol-independent semantic objects. Protocol-specific defaults are defined through realization profiles, not by changing the meaning of the delivery model itself.

## DeliverySemantics

A `DeliverySemantics` object MUST define:
- `delivery_class`
- `side_effect_class`
- `streaming_class`
- `cancellation_class`

### Delivery classes

The standard delivery classes are:
- `AT_MOST_ONCE`
- `AT_LEAST_ONCE`
- `DEDUPED_AT_LEAST_ONCE`
- `TASK_EXACTLY_ONCE_INTENT`

#### Interpretation

- `AT_MOST_ONCE` means an invocation MAY be lost, but MUST NOT be retried automatically by the realization layer.
- `AT_LEAST_ONCE` means delivery MAY be retried and duplicate execution is possible.
- `DEDUPED_AT_LEAST_ONCE` means retries MAY occur, but duplicates MUST be detected or suppressed using an idempotency or task key.
- `TASK_EXACTLY_ONCE_INTENT` means exactly-once is claimed only at the durable task identity layer, not at the network transport layer.

### Side-effect classes

The standard side-effect classes are:
- `PURE`
- `IDEMPOTENT_EFFECT`
- `NON_IDEMPOTENT_EFFECT`
- `COMPENSATABLE_EFFECT`

#### Interpretation

- `PURE` means the realization has no externally visible side effects.
- `IDEMPOTENT_EFFECT` means repeated execution with the same key or input envelope yields the same externally visible state.
- `NON_IDEMPOTENT_EFFECT` means repeated execution MAY cause additional externally visible effects.
- `COMPENSATABLE_EFFECT` means a compensating operation exists that can reverse or offset the effect according to a declared compensation contract.

### Streaming classes

The standard streaming classes are:
- `NONE`
- `PROGRESS_STREAM`
- `EVENT_STREAM`
- `RESULT_STREAM`

### Cancellation classes

The standard cancellation classes are:
- `NOT_CANCELLABLE`
- `BEST_EFFORT_CANCEL`
- `GUARDED_CANCEL`
- `TRANSACTIONAL_CANCEL`

#### Interpretation

- `NOT_CANCELLABLE` means cancellation requests MUST be ignored or rejected.
- `BEST_EFFORT_CANCEL` means the runtime MAY attempt cancellation, but no rollback or completion guarantee is implied.
- `GUARDED_CANCEL` means cancellation MAY proceed only if guard conditions hold and receipt state is updated accordingly.
- `TRANSACTIONAL_CANCEL` means cancellation semantics are integrated with a compensating or transactional model and MUST emit a corresponding receipt.

## ReceiptSemantics

A `ReceiptSemantics` object MUST define:
- `receipt_type`
- `required_fields`

### Standard receipt types

- `NONE`
- `REQUEST_RECEIPT`
- `TASK_RECEIPT`
- `ARTIFACT_RECEIPT`
- `PROOF_ARTIFACT`

### Receipt obligations

Every receipt MUST carry at least the fields required by the profile. The standard field universe is:
- `receipt_id`
- `correlation_id`
- `capability_id`
- `realization_id`
- `interaction_mode`
- `timestamp`
- `actor_ref`
- `outcome`
- `payload_digest`
- `signature_ref`

### Core rules

1. Every realization that is not `PURE` SHOULD emit at least one receipt.
2. Every `NON_IDEMPOTENT_EFFECT` realization MUST emit either `ARTIFACT_RECEIPT` or `PROOF_ARTIFACT`, unless an exception is explicitly justified by a higher-level policy profile.
3. Every `TASK_EXACTLY_ONCE_INTENT` realization MUST emit `TASK_RECEIPT` and MUST use a stable task identity for dedupe and replay.
4. Every receipt MUST bind to the canonical `FunctionIdentity` through `capability_id`.
5. Every receipt MUST be content-addressable through `payload_digest`.
6. If a realization supports streaming, receipts MAY be append-only over the life of a task or stream, but the terminal state MUST be unambiguous.

## Cross-object consistency rules

1. `NON_IDEMPOTENT_EFFECT` MUST NOT be paired with `AT_LEAST_ONCE` unless a dedupe or compensation strategy is declared elsewhere in the realization metadata.
2. `COMPENSATABLE_EFFECT` SHOULD reference a compensation contract or workflow contract.
3. `TASK_EXACTLY_ONCE_INTENT` MUST NOT be interpreted as a transport-level guarantee.
4. `REQUEST_RECEIPT` is the minimum acceptable receipt for bounded request/response realizations.
5. `TASK_RECEIPT` is the minimum acceptable receipt for long-running task realizations.

## Protocol-specific defaults (informative)

- MCP realizations SHOULD default to `REQUEST_RECEIPT` at minimum.
- A2A realizations SHOULD default to `TASK_RECEIPT`.
- ACP compatibility realizations SHOULD default to `TASK_RECEIPT` or equivalent durable job receipts.
- Externalized adapters and human steps SHOULD emit transcript-backed evidence receipts where direct execution receipts are unavailable.

## Machine-readable companions

The canonical JSON Schema companion for this draft is:

- `schemas/jsonschema/capability-fabric/core.v0.schema.json`

## Change control

Changes that alter:
- delivery class semantics
- side-effect class semantics
- receipt obligations
- required receipt fields

MUST update the machine-readable companion in the same PR.

Breaking changes MUST advance the schema version.
