# schemas/

This directory contains all **data contracts** for the Knowledge Context standards package.

These schemas are not “nice-to-have.” They are part of the enforceable compatibility surface:
- Avro defines **Path-A RPC payload bytes** and **event-stream payloads**
- JSON-LD defines the **semantic overlay** (linked data meaning)
- JSON Schema defines the **canonical structural shapes** for artifacts and relations

## Subdirectories

- `schemas/avro/`  
  Avro contracts:
  - `knowledge.store.v0/` — Path-A RPC payload protocol (`.avpr`)
  - `events.v1/` — lifecycle event contracts (topic payloads)

- `schemas/jsonld/`  
  JSON-LD contexts (semantic overlay):
  - `contexts/knowledge/context.jsonld` is the canonical context for Knowledge Context

- `schemas/jsonschema/`  
  Canonical structural schemas (tooling + documentation):
  - `common/` shared references
  - `core/` Note/Claim/Annotation/Provenance + Anchor/Selector
  - `relations/` MeriotopographicEdge + relation primitives

## Authority and change control

### TriTRPC binding
TriTRPC framing and method naming are defined in:
- `docs/standards/030-tritrpc-binding.md`

### Schema/Context IDs are frozen
The following labels and derived IDs are frozen and MUST NOT be renamed:
- `KNOWLEDGE_AVRO_v0` (SCHEMA_ID)
- `KNOWLEDGE_JSONLD_v0` (CONTEXT_ID)

See:
- `docs/standards/031-schema-context-id-registry.md`

If a breaking change is required:
- create a new label (e.g., `KNOWLEDGE_AVRO_v1`)
- update bindings + fixtures + verifiers in the same PR

## Enforceable gates

From repo root:
- `make verify` checks TriTRPC fixtures (AEAD/AAD boundary, IDs, SERVICE/METHOD, AUX).
- `make roundtrip` checks Avro semantic round-trip decoding for Path-A payloads.

If you change a schema, you are expected to update fixtures/verifiers/roundtrip as needed.
