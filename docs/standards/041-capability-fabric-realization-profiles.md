# 041 — Capability Fabric Realization Profiles (v0.1 draft)

## Status

**Draft.** This document defines protocol-specific and boundary-specific realization profiles for the Capability Fabric.

This document is normative. It uses RFC-style language:
- **MUST / MUST NOT** = mandatory for compliance
- **SHOULD / SHOULD NOT** = strongly recommended
- **MAY** = optional

## Purpose

A realization profile binds a protocol, runtime, or boundary model onto the protocol-independent semantic core defined in `040-capability-fabric-core.md`.

Realization profiles define:
- how a capability is delivered
- what receipts are natural or mandatory
- what controllability is typical
- what proof claims are appropriate
- what security and interoperability constraints apply

Realization profiles MUST NOT redefine capability meaning.

## Supported profiles in this draft

- `MCPRealizationProfile`
- `A2ARealizationProfile`
- `ACPCompatibilityProfile`
- `SphereBridgeProfile`
- `ExternalizedCapabilityAdapter`
- `MorlocRealizationProfile` (provisional)

## Shared rules

1. Every realization profile MUST reference an existing `FunctionIdentity` through `RealizationMetadata`.
2. Every realization profile MUST declare a single `InteractionMode`.
3. Every realization profile MUST declare `DeliverySemantics`, `ReceiptSemantics`, `ExecutionControllabilityProfile`, and `ProofStrengthProfile`.
4. Realization profiles MAY add protocol-specific metadata, but MUST NOT alter the canonical meaning of the capability.

## MCPRealizationProfile

### Purpose

Defines capability realizations delivered through the Model Context Protocol (MCP).

### Required fields

An `MCPRealizationProfile` MUST include:
- `server_ref`
- `host_mediated` (boolean; MUST be true in this profile)
- `session_scope`
- `auth_scope`
- `exposure_kinds`
- `local_execution_risk`

### Normative rules

- MCP realizations MUST use `InteractionMode = MCP`.
- MCP realizations SHOULD default to `REQUEST_RECEIPT` at minimum.
- Side-effecting MCP realizations SHOULD emit `ARTIFACT_RECEIPT` when durable output or external side effects exist.
- Audience-bound authorization and no-token-passthrough constraints SHOULD be documented in the security profile reference.

## A2ARealizationProfile

### Purpose

Defines capability realizations delivered through agent-to-agent task interaction.

### Required fields

An `A2ARealizationProfile` MUST include:
- `agent_card_ref`
- `task_lifecycle`
- `update_modes`
- `input_modes`
- `output_modes`
- optional `extension_uris`

### Normative rules

- A2A realizations MUST use `InteractionMode = A2A`.
- A2A realizations SHOULD default to `TASK_RECEIPT`.
- A2A realizations with durable terminal outputs SHOULD emit `ARTIFACT_RECEIPT`.
- A2A realizations SHOULD represent updates as append-only task observations.

## ACPCompatibilityProfile

### Purpose

Defines compatibility mapping for HTTP-native async agent interaction patterns historically associated with ACP.

### Required fields

An `ACPCompatibilityProfile` MUST include:
- `endpoint_ref`
- `async_default`
- `discovery_mode`
- `migration_target`

### Normative rules

- ACP compatibility realizations MUST use `InteractionMode = ACP`.
- ACP compatibility realizations SHOULD default to `TASK_RECEIPT` or equivalent durable job receipt.
- ACP compatibility realizations SHOULD document how they map onto A2A-equivalent task semantics where feasible.

## SphereBridgeProfile

### Purpose

Defines cross-domain / cross-sphere boundary traversal where admissibility, policy, or evidence requirements change.

### Required fields

A `SphereBridgeProfile` MUST include:
- `source_domain`
- `target_domain`
- `admissibility_transition`
- `required_cover_refs`
- `bridge_policy_ref`

### Normative rules

- Sphere bridges MUST use `InteractionMode = SPHERE_BRIDGE`.
- Sphere bridges MUST declare downgrade or upgrade requirements for proof strength when crossing domains.
- Sphere bridges MUST reference the evidence-cover requirements needed for admissible traversal.

## ExternalizedCapabilityAdapter

### Purpose

Defines weakly controlled or uncontrolled realizations such as browser automation, prompt programs, vendor APIs, or human-mediated wrappers.

### Required fields

An `ExternalizedCapabilityAdapter` MUST include:
- `adapter_id`
- `canonical_capability_id`
- `native_mode`
- `transcript_schema_ref`
- `evidence_emission_contract_ref`
- `downgrade_rules_ref`

### Normative rules

- Externalized adapters MUST use either `InteractionMode = EXTERNAL_ADAPTER` or `InteractionMode = HUMAN`.
- Externalized adapters MUST NOT claim stronger proof strength than their controllability permits.
- Externalized adapters SHOULD emit transcript-backed evidence receipts.

## MorlocRealizationProfile (provisional)

### Purpose

Defines a provisional mapping for Morloc-like polyglot function-fabric realizations.

### Required fields

A `MorlocRealizationProfile` MUST include:
- `status` (MUST be `PROVISIONAL` in this draft)
- `general_type_ref`
- `realization_set_ref`
- `nexus_manifest_ref`
- `pool_requirements_ref`
- `determinism_grade`

### Normative rules

- Morloc realizations MUST NOT be treated as canonical or required by the Capability Fabric core until conformance and determinism criteria are satisfied.
- Morloc realizations MUST be represented as realizations, not as canonical capability definitions.

## Machine-readable companions

The canonical JSON Schema companion for this draft is:

- `schemas/jsonschema/capability-fabric/realization-profiles.v0.schema.json`

## Change control

Changes that alter:
- profile names
- required fields
- enum values
- protocol mapping semantics

MUST update the machine-readable companion in the same PR.

Breaking changes MUST advance the schema version.
