# schemas/jsonschema/

This directory contains **canonical JSON Schemas** for Knowledge Context artifacts and relations.

These schemas serve three purposes:
1) Human-readable canonical shapes for artifacts (documentation + tooling)
2) Validation for non-Avro tooling integrations (e.g., JSON-based adapters)
3) A stable reference model for mapping between Avro payloads and JSON-LD semantic overlays

**Important:** TriTRPC Path-A wire payload bytes are Avro (see `schemas/avro/`). JSON Schema here is the canonical structural model.

## Structure

- `schemas/jsonschema/common/`  
  Shared references used across schemas (ActorRef, ArtifactRef, ProvenanceRef, etc.).

- `schemas/jsonschema/core/`  
  Core artifacts:
  - Note
  - Claim
  - Annotation
  - ProvenanceRecord
  - Anchor/Selector primitives

- `schemas/jsonschema/relations/`  
  Relationship artifacts:
  - MeriotopographicEdge

## Relationship to normative semantics

JSON Schema defines structure, not meaning.

Semantic meaning and invariants live in:
- `docs/standards/020-meriotopographics.md`

For example:
- JSON Schema can say an edge has `predicate: string`
- The normative doc defines which predicates exist and what constraints apply (acyclicity, anchor requirements, ordering, etc.)

## Change control

If you change JSON Schema in a way that impacts:
- Avro payload mapping,
- fixture generation/verifiers,
- JSON-LD predicate interpretation,

then you MUST update the corresponding:
- Avro protocol or payload tooling (if applicable)
- fixtures/verifiers
- roundtrip checks (if it affects Avro semantics)

## Gates

From repo root:
- `make hygiene`
- `make verify`
- `make roundtrip`

These are the compatibility gates. Schema changes that break these must not merge.
