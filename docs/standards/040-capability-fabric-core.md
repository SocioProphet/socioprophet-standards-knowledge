# 040 — Capability Fabric Core (v0.1 draft)

## Status

**Draft.** This document defines the protocol-independent semantic core for the SocioProphet Capability Fabric.

This document is normative. It uses RFC-style language:
- **MUST / MUST NOT** = mandatory for compliance
- **SHOULD / SHOULD NOT** = strongly recommended
- **MAY** = optional

## Purpose

The Capability Fabric standard defines the canonical semantic objects used to represent capabilities, their contracts, execution effects, interaction modes, delivery guarantees, receipts, controllability, proof strength, and realization metadata.

The Capability Fabric core exists to separate:
- **transport** from **semantics**
- **capability meaning** from **runtime realization**
- **delivery guarantees** from **proof claims**
- **controlled execution** from **externalized / weakly controlled execution**

## Scope

This document standardizes the following protocol-independent objects:

- `FunctionIdentity`
- `CapabilitySignature`
- `EffectContext`
- `InteractionMode`
- `DeliverySemantics`
- `ReceiptSemantics`
- `ExecutionControllabilityProfile`
- `ProofStrengthProfile`
- `RealizationMetadata`

These objects are independent of MCP, A2A, ACP, Morloc, Ray, Kubernetes, or any particular runtime.

## Non-goals

This document does **not** define:
- TriTRPC envelope framing
- protocol-specific message formats
- policy sets or admissibility registries
- runtime placement algorithms
- proof artifact schemas

These belong to separate standards packages.

## Relationship to upstream authorities

- Transport authority remains `SocioProphet/TriTRPC`.
- Platform governance / index remains `SocioProphet/socioprophet-standards-storage`.
- This document defines semantic objects that MAY be carried by TriTRPC, but MUST NOT alter TriTRPC transport semantics.

## Core objects

### 1. FunctionIdentity

`FunctionIdentity` is the canonical identity of a capability independent of language, protocol, runtime, or deployment substrate.

A `FunctionIdentity` MUST include:
- stable identifier
- namespace
- human-readable name
- version
- canonical input type reference
- canonical output type reference
- semantic hash
- purity hint
- determinism hint

A `FunctionIdentity` MUST NOT mention a specific runtime, protocol, or implementation language.

### 2. CapabilitySignature

`CapabilitySignature` is the typed callable contract for a capability.

A `CapabilitySignature` MUST bind:
- one `FunctionIdentity`
- optional precondition reference
- optional postcondition reference
- one `EffectContext`
- zero or more policy hook references
- optional evidence requirement reference

### 3. EffectContext

`EffectContext` defines execution-relevant effect classes.

An `EffectContext` MUST specify:
- transport effect
- state effect
- placement effect
- authorization effect
- observation effect

### 4. InteractionMode

`InteractionMode` defines how a capability node is delivered or mediated.

The standard modes are:
- `LOCAL`
- `MCP`
- `A2A`
- `ACP`
- `SPHERE_BRIDGE`
- `EXTERNAL_ADAPTER`
- `HUMAN`

Every realization MUST declare exactly one `InteractionMode`.

### 5. DeliverySemantics

`DeliverySemantics` defines:
- delivery class
- side-effect class
- streaming class
- cancellation class

The standard delivery classes are:
- `AT_MOST_ONCE`
- `AT_LEAST_ONCE`
- `DEDUPED_AT_LEAST_ONCE`
- `TASK_EXACTLY_ONCE_INTENT`

The standard side-effect classes are:
- `PURE`
- `IDEMPOTENT_EFFECT`
- `NON_IDEMPOTENT_EFFECT`
- `COMPENSATABLE_EFFECT`

### 6. ReceiptSemantics

`ReceiptSemantics` defines the minimum receipt obligations for a realization.

The standard receipt types are:
- `NONE`
- `REQUEST_RECEIPT`
- `TASK_RECEIPT`
- `ARTIFACT_RECEIPT`
- `PROOF_ARTIFACT`

Every non-pure capability invocation SHOULD emit at least one receipt.
Every receipt MUST carry:
- receipt identifier
- correlation identifier
- capability identifier
- realization identifier
- timestamp
- outcome
- payload digest
- signature or signature reference

### 7. ExecutionControllabilityProfile

`ExecutionControllabilityProfile` grades how much of the execution chain is under trusted control.

It MUST score:
- type control
- realization control
- placement control
- state control
- policy control
- telemetry control
- replay control
- attestation control

It MUST classify the node into one of:
- `C3` fully controlled
- `C2` mostly controlled
- `C1` weakly controlled
- `C0` uncontrolled / external

### 8. ProofStrengthProfile

`ProofStrengthProfile` defines what proof claims are legitimate for a node.

The standard proof-strength classes are:
- `INTRINSIC`
- `ATTESTED_OBSERVATIONAL`
- `TRANSCRIPT_OBSERVATIONAL`
- `HUMAN_ATTESTED`
- `EXTERNAL_UNVERIFIABLE`

A node MUST NOT claim a proof strength stronger than its controllability class permits.

### 9. RealizationMetadata

`RealizationMetadata` binds a canonical capability to a runtime/protocol realization.

It MUST include:
- realization identifier
- function identifier
- interaction mode
- delivery semantics reference
- receipt semantics reference
- controllability profile reference
- proof-strength profile reference
- runtime kind

Runtime kind MAY include implementations such as:
- local function
- MCP server
- A2A agent
- ACP endpoint
- Kubernetes worker
- Ray task
- Ray actor
- external adapter
- human step

## Cross-object rules

1. `FunctionIdentity` is canonical and protocol-independent.
2. `InteractionMode` and `RealizationMetadata` MAY vary across realizations of the same capability.
3. `DeliverySemantics`, `ReceiptSemantics`, `ExecutionControllabilityProfile`, and `ProofStrengthProfile` MUST be explicit for every realization.
4. External or weakly controlled steps MUST be represented honestly as `EXTERNAL_ADAPTER`, `HUMAN`, or lower-controllability realizations.
5. Capability meaning MUST remain stable even when realization, runtime, placement, or protocol changes.

## Machine-readable companions

The canonical JSON Schema companion for this draft is:

- `schemas/jsonschema/capability-fabric/core.v0.schema.json`

## Change control

Changes that alter:
- identifiers
- enum values
- required fields
- canonical meaning

MUST update the machine-readable companion schema in the same PR.

Breaking changes MUST advance the schema version.

## Editorial guidance

This document defines the semantic core only.
Protocol-specific mappings (MCP, A2A, ACP, sphere bridges, Morloc) belong in separate realization-profile documents.
