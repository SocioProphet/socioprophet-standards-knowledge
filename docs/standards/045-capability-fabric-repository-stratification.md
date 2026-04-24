# 045 — Capability Fabric Repository Stratification (v0.1 draft)

## Status

**Draft.** This document records the canonical repository split for the Capability Fabric package.

## Purpose

The Capability Fabric spans transport, semantics, ontology alignment, platform adoption, and runtime implementation. This document defines where each responsibility MUST live so that repositories do not silently fork or re-specify the semantic core.

## Canonical source of truth

The protocol-independent Capability Fabric standards live in:

- `SocioProphet/socioprophet-standards-knowledge`

This repository is the canonical home for:
- semantic core objects
- realization profiles
- delivery and receipt semantics
- controllability and proof-strength semantics
- machine-readable companion schemas
- worked examples and future conformance vectors

## Transport authority

The transport authority remains:

- `SocioProphet/TriTRPC`

`TriTRPC` MAY carry capability-fabric objects as typed blobs, digests, signatures, references, or attestations.

`TriTRPC` MUST NOT redefine the canonical semantics of the Capability Fabric core.

## Ontology alignment authority

Ontology and dictionary alignment belongs in:

- `SocioProphet/ontogenesis`

`ontogenesis` MAY define namespace mappings, controlled vocabulary bindings, SHACL or JSON-LD overlays, and dictionary governance for capability-fabric concepts.

`ontogenesis` MUST NOT redefine the semantic core.

## Platform adoption authority

Platform-facing integration and adoption guidance belongs in:

- `SocioProphet/prophet-platform-standards`

This repository MAY define:
- deployment and runtime integration guidance
- planner/operator/runtime adoption notes
- platform-facing examples

It MUST consume the canonical source rather than restate the semantic core.

## Runtime and hardening implementations

Runtime adapters, protocol gateways, and hardening surfaces MAY live in implementation repositories such as:
- `SocioProphet/mcp-a2a-zero-trust`
- other planner, operator, or execution repos

These repositories MUST implement or consume the standards, not redefine them.

## Core rule

A repository MAY extend or consume the Capability Fabric package only if it does not redefine the canonical meaning of:
- `FunctionIdentity`
- `CapabilitySignature`
- `EffectContext`
- `InteractionMode`
- `DeliverySemantics`
- `ReceiptSemantics`
- `ExecutionControllabilityProfile`
- `ProofStrengthProfile`
- `RealizationMetadata`

## Review posture

When changes touch multiple repositories, review SHOULD proceed in this order:
1. canonical semantic source (`socioprophet-standards-knowledge`)
2. transport pointers (`TriTRPC`)
3. ontology alignment (`ontogenesis`)
4. platform adoption (`prophet-platform-standards`)
5. runtime/hardening implementations

This ordering preserves semantic authority and minimizes drift.
