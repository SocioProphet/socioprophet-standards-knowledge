# schemas/jsonschema/capability-fabric/

This directory contains **canonical JSON Schemas** for the Capability Fabric semantic core.

These schemas define structure for protocol-independent objects such as:
- FunctionIdentity
- CapabilitySignature
- EffectContext
- InteractionMode
- DeliverySemantics
- ReceiptSemantics
- ExecutionControllabilityProfile
- ProofStrengthProfile
- RealizationMetadata

## Purpose

These schemas serve three purposes:
1. Human-readable canonical shapes for capability-fabric objects
2. Validation for adapters, planners, and SDKs that consume the semantic core
3. Stable references for mappings into protocol-specific realization profiles and proof/telemetry tooling

## Relationship to normative semantics

JSON Schema here defines **structure, required fields, enums, and references**.

Normative meaning lives in:
- `docs/standards/040-capability-fabric-core.md`

Protocol-specific meaning lives in later documents such as MCP/A2A/ACP realization profiles.

## Structure

- `core.v0.schema.json`
  Aggregate schema containing `$defs` for the draft core objects.

## Change control

If you change:
- required fields
- enum values
- object names
- identifier semantics

then you MUST update:
- `docs/standards/040-capability-fabric-core.md`
- this schema family
- any affected examples or conformance vectors

Breaking changes MUST advance the schema version.
