# schemas/jsonld/

This directory contains **JSON-LD contexts** that provide a semantic overlay for Knowledge Context artifacts.

JSON-LD here is **not** the wire payload format for TriTRPC Path-A. Wire payloads are Avro bytes. JSON-LD is used to:
- express linked-data meaning (IRIs, vocab expansion),
- enable RDF/graph-store interoperability,
- provide a stable semantic interpretation of predicates and fields.

## Structure

- `schemas/jsonld/contexts/knowledge/`
  - `context.jsonld` — canonical JSON-LD context for the Knowledge Context
  - `README.md` — mapping notes and predicate expansion rules

## Canonical binding and ID freeze

The canonical JSON-LD context is bound to a frozen label:
- `KNOWLEDGE_JSONLD_v0`

The derived `CONTEXT_ID` is SHA3-256(label) and is frozen in:
- `docs/standards/031-schema-context-id-registry.md`

If a breaking change is required:
- create a new label (e.g., `KNOWLEDGE_JSONLD_v1`)
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
