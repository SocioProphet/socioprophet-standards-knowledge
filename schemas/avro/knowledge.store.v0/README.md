# knowledge.store.v0 — Avro Path-A Payload Contracts (v0)

This directory defines the Avro payload contracts used when TriTRPC `path: A` is selected (Avro binary payload).

## Mapping to TriTRPC envelope
- TriTRPC `SERVICE`: `knowledge.store.v0`
- TriTRPC `METHOD` strings (envelope) use dot suffixes per binding doc:
  - Request: `<MethodName>_a.REQ`
  - Response: `<MethodName>_a.RESP`

Avro protocol message names are stored with underscores for portability:
- `UpsertNote_a_REQ` maps to TriTRPC method `UpsertNote_a.REQ`
- `QueryNotes_a_REQ` maps to TriTRPC method `QueryNotes_a.REQ`
(and similarly for Claim/Edge)

See: `docs/standards/030-tritrpc-binding.md`

## Determinism
- No Avro `map` types are used.
- Any free-form payload is JCS-canonicalized and stored as bytes (`*_jcs`).
