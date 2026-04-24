# 044 — Capability Fabric Package Index (v0.1 draft)

## Status

**Draft.** This document is an index for the Capability Fabric package.

## Purpose

The Capability Fabric package defines the protocol-independent semantic core and realization-profile standards for capability-oriented execution, delivery, controllability, proof strength, and protocol/runtime binding.

This index exists to make the package discoverable as a coherent unit.

## Package contents

### Normative documents

- `040-capability-fabric-core.md`
  - Canonical semantic core objects
  - Function identity, capability signature, effect context, interaction mode
  - Delivery, receipts, controllability, proof strength, realization metadata

- `041-capability-fabric-realization-profiles.md`
  - Protocol-specific and boundary-specific realization profiles
  - MCP, A2A, ACP compatibility, sphere bridges, externalized adapters, provisional Morloc

- `042-capability-fabric-delivery-and-receipts.md`
  - Delivery guarantees
  - Side-effect classes
  - Streaming and cancellation semantics
  - Receipt obligations and consistency rules

- `043-capability-fabric-controllability-and-proof-strength.md`
  - Controllability grading (`C0..C3`)
  - Proof-strength classes
  - Replayability classes
  - Mixed-chain downgrade rules

### Machine-readable companions

- `schemas/jsonschema/capability-fabric/core.v0.schema.json`
- `schemas/jsonschema/capability-fabric/realization-profiles.v0.schema.json`
- `schemas/jsonschema/capability-fabric/README.md`

### Examples

- `examples/capability-fabric/v0.1/minimal-capability-example.yaml`

## Intended follow-on standards

Likely next documents in this package include:
- protocol-specific operational notes
- worked mixed-chain examples
- conformance vectors and verifiers
- dictionary / ontology alignment notes

## Source-of-truth rule

The canonical source of truth for the Capability Fabric semantic package is this repository.
Downstream repositories MAY consume, align, or implement these standards, but MUST NOT redefine the semantic core.
