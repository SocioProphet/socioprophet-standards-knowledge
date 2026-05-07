# docs/standards/

This directory contains **normative** specifications for the SocioProphet **Knowledge Context** standards package and adjacent semantic standards used by the broader SocioProphet artifact, capability, and evidence fabric.

These documents use RFC-style language:
- **MUST** / **MUST NOT** = mandatory for compliance
- **SHOULD** / **SHOULD NOT** = strongly recommended (exceptions must be justified)
- **MAY** = optional

## What lives here

### Knowledge Context core specs
- `000-knowledge-platform-standards.md`  
  Scope, principles, and what “Knowledge Context” covers.

- `001-upstream-dependencies.md`  
  Upstream authority pins (platform governance + TriTRPC transport authority).

- `020-meriotopographics.md`  
  Predicate registry + invariants for meriotopographic relations (part/whole, placement, derivation, epistemic, governance).

- `030-tritrpc-binding.md`  
  TriTRPC v1 binding for Knowledge Context (envelope ordering, AEAD/AAD boundary, SERVICE/METHOD conventions, AUX semantics).

- `031-schema-context-id-registry.md`  
  Frozen **label → ID → path** registry for SCHEMA_ID/CONTEXT_ID (prevents silent drift).

- `032-tritrpc-knowledge-fixtures.md`  
  Fixture semantics, regeneration rules, and change control for byte-level compliance vectors.

### Capability Fabric specs
- `040-capability-fabric-core.md`  
  Protocol-independent semantic core for capability identity, signatures, effects, interaction modes, delivery, receipts, controllability, proof strength, and realization metadata.

- `041-capability-fabric-realization-profiles.md`  
  Protocol-specific and boundary-specific realization profiles for MCP, A2A, ACP compatibility, sphere bridges, external adapters, and provisional Morloc-style realizations.

- `042-capability-fabric-delivery-and-receipts.md`  
  Delivery guarantees, side-effect classes, streaming/cancellation classes, and receipt obligations, including `PROOF_ARTIFACT` receipt semantics.

- `043-capability-fabric-controllability-and-proof-strength.md`  
  Controllability grading, proof-strength classes, replayability classes, admissibility floors, and mixed-chain proof downgrade rules.

- `044-capability-plane-registry.md`  
  Capability-plane enum registry, including the `viz` plane admission.

### Cross-lane artifact and evidence specs
- `045-cross-lane-artifact-canon.md`  
  Semantic canon for runtime artifacts, knowledge artifacts, entity/proof artifacts, Capability Fabric receipts, AgentPlane evidence records, and UI/platform evidence surfaces.

- `046-field-alias-matrix.md`  
  Non-breaking alias matrix mapping lane-specific field names into shared semantic slots for `DecisionArtifact`, `ProofPack`, `TemporalProfile`, and `TrustProfile`.

- `081-operation-plane-memory-knowledge.md`  
  Draft standard for Operation Plane memory ingestion as `WorkspaceOperation`, evidence-linked memory metadata, lifecycle/admission/correction/deletion flow, and policy-governed agent visibility.

## How docs relate to enforceable compliance

This repo treats standards as **executable**:
- **Schemas** define shapes (`schemas/`)
- **Fixtures** define bytes (`fixtures/`)
- **Verifiers** prove compliance (`tools/`)
- **Roundtrip** proves semantic correctness (`make roundtrip`)

Any doc change that affects:
- envelope framing / AEAD rules,
- schema/context labels or IDs,
- method naming,
- payload semantics,
- fixture vector semantics,

MUST be accompanied by updates to:
- fixtures (hex vectors + nonces),
- verifiers,
- and any affected round-trip checks.

Semantic-only documents that do not change transport bytes, schema/context IDs, Avro payload bytes, JSON-LD context IDs, fixture vectors, or validation behavior MUST state that boundary explicitly.

## Editing rules

- Prefer **precise** requirements over prose.
- Avoid ambiguity in anything that influences bytes or determinism.
- Keep “transport” (TriTRPC) separate from “semantics” (meriotopographics + artifact meaning + capability meaning).
- When adding new requirements, update fixtures/tests in the same PR or clearly mark the doc as `draft`.
- When introducing a cross-lane semantic alias, prefer a non-breaking mapping before renaming released fields.

## Running the gates

From repo root:

- `make hygiene` (cleans `.DS_Store` + runs validate)
- `make verify` (TriTRPC fixture verification)
- `make roundtrip` (Avro semantic round-trip verification)

Additional optional gates may exist for semantic-core SHACL or domain-specific validation when those packages are present on a branch.

## Upstream references

- TriTRPC authority: `SocioProphet/tritrpc` (TriTRPC; aliases: triRPC/trirpc/triunerpc)
- Platform governance index: `SocioProphet/socioprophet-standards-storage`
- Runtime/evidence consumer: `SocioProphet/agentplane`
- Public architecture surface: `SocioProphet/socioprophet`
