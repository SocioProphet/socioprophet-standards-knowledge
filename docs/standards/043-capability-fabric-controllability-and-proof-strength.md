# 043 — Capability Fabric Controllability and Proof Strength (v0.1 draft)

## Status

**Draft.** This document defines controllability grading and proof-strength rules for Capability Fabric realizations.

This document is normative. It uses RFC-style language:
- **MUST / MUST NOT** = mandatory for compliance
- **SHOULD / SHOULD NOT** = strongly recommended
- **MAY** = optional

## Purpose

This document standardizes how the Capability Fabric represents:
- how much of an execution step is under trusted control
- how strong a proof claim is legitimate for that step
- how mixed chains must degrade honestly when they traverse weakly controlled or externalized boundaries

The intent is to prevent realizations from claiming stronger guarantees than their actual execution boundary permits.

## ExecutionControllabilityProfile

An `ExecutionControllabilityProfile` MUST score:
- `type_control`
- `realization_control`
- `placement_control`
- `state_control`
- `policy_control`
- `telemetry_control`
- `replay_control`
- `attestation_control`

Each score MUST be an integer in `[0,3]`.

### Score interpretation

- `0` = absent or not trusted
- `1` = weak
- `2` = substantial
- `3` = strong

### Overall controllability classes

Every realization MUST be classified into exactly one of:
- `C3` — fully controlled
- `C2` — mostly controlled
- `C1` — weakly controlled
- `C0` — uncontrolled / external

### Recommended interpretation

- `C3` realizations are suitable for strong replay and intrinsic proof claims.
- `C2` realizations are suitable for attested or bounded observational claims.
- `C1` realizations are suitable only for weak observational claims unless corroborated.
- `C0` realizations MUST be treated as external observations or human/external adapter boundaries.

## ProofStrengthProfile

A `ProofStrengthProfile` MUST define:
- `strength_class`
- `replayability`
- `admissibility_floor`
- `required_corrob_count`

### Standard strength classes

- `INTRINSIC`
- `ATTESTED_OBSERVATIONAL`
- `TRANSCRIPT_OBSERVATIONAL`
- `HUMAN_ATTESTED`
- `EXTERNAL_UNVERIFIABLE`

### Standard replayability classes

- `FULL`
- `BOUNDED`
- `TRANSCRIPT_ONLY`
- `NONE`

### Standard admissibility floors

- `PUBLIC`
- `OPERATOR`
- `AUDITOR`

## Cross-object rules

1. A realization MUST NOT claim `INTRINSIC` proof strength unless its controllability is sufficient for the claim.
2. A realization with `overall_class = C0` MUST NOT claim `INTRINSIC` or `ATTESTED_OBSERVATIONAL` without explicit corroboration and a higher-level bridge or policy exception.
3. A realization with replayability `NONE` MUST NOT present itself as replay-stable.
4. A realization with replayability `TRANSCRIPT_ONLY` MUST provide transcript-backed evidence or equivalent observational traces.
5. A higher `required_corrob_count` indicates that the realization requires more corroborating evidence items before stronger claims are admissible.

## Mixed-chain rule

A capability chain MAY include mixed controllability classes. In such a chain:

1. Every node MUST declare its own controllability and proof-strength profiles.
2. The chain MUST degrade honestly when traversing from stronger to weaker nodes.
3. A weaker node MUST NOT silently inherit the proof strength of a stronger upstream node.
4. Stronger downstream nodes MAY re-establish stronger guarantees only through explicit attestation, corroboration, or policy-defined admissibility repair.

## Informative defaults

The following defaults are informative and MAY be refined by later standards:

- Internal local realization: typically `C3`
- Internal MCP realization: typically `C3` or `C2`
- External MCP realization: typically `C2` or `C1`
- Trusted A2A peer: typically `C2`
- Public or weakly controlled A2A/ACP peer: typically `C1`
- Externalized adapter: typically `C0` or `C1`
- Human approval: typically `C0` or `C1`

## Machine-readable companions

The canonical JSON Schema companion for this draft is:

- `schemas/jsonschema/capability-fabric/core.v0.schema.json`

## Change control

Changes that alter:
- controllability scoring
- class meanings
- proof-strength classes
- replayability classes
- admissibility floors

MUST update the machine-readable companion in the same PR.

Breaking changes MUST advance the schema version.
