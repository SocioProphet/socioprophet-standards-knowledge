# schemas/jsonld/

This directory contains **JSON-LD contexts** that provide a semantic overlay for Knowledge Context artifacts.

JSON-LD here is **not** the wire payload format for TriTRPC Path-A. Wire payloads are Avro bytes. JSON-LD is used to:
- express linked-data meaning (IRIs, vocab expansion),
- enable RDF/graph-store interoperability,
- provide a stable semantic interpretation of predicates and fields.

## Structure

- `schemas/jsonld/contexts/knowledge/`
  - `context.jsonld` — canonical JSON-LD context for the `v0` Knowledge Context
  - `README.md` — mapping notes and predicate expansion rules

- `schemas/jsonld/contexts/knowledge.v1/`
  - `context.jsonld` — draft JSON-LD context for the expanded `v1` Knowledge Context
  - `README.md` — v1 coverage notes for provenance records, entities, passages, mentions, embedding references, vector index references, and entity resolution records

## Canonical binding and ID freeze

The frozen JSON-LD context labels are:
- `KNOWLEDGE_JSONLD_v0`
- `KNOWLEDGE_JSONLD_v1`

The derived `CONTEXT_ID` values are SHA3-256(label) and are frozen in:
- `docs/standards/031-schema-context-id-registry.md`

If a breaking change is required:
- create a new label (e.g., `KNOWLEDGE_JSONLD_v2`)
- update the registry, TriTRPC binding, fixtures, and verifiers in the same PR

## Predicate semantics

Meriotopographic predicates are defined normatively in:
- `docs/standards/020-meriotopographics.md`

In the JSON-LD context, predicate values expand under `@vocab` to:
- `https://socioprophet.org/ns/knowledge#<predicate>`

## Relation to TriTRPC

TriTRPC’s `CONTEXT_ID` field is how a receiver identifies which semantic overlay is intended.
The TriTRPC binding for Knowledge Context is specified in:
- `docs/standards/030-tritrpc-binding.md`

## Gates and change control

If JSON-LD contexts change in ways that affect IDs or predicate interpretation:
- update `031-schema-context-id-registry.md`
- update TriTRPC fixtures/verifiers as needed

From repo root:
- `make verify` (ensures IDs remain consistent via fixture checks)
