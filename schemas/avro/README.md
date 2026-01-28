# schemas/avro/

This directory contains **Avro contracts** for the Knowledge Context.

Avro is used in two distinct roles:

1) **TriTRPC Path-A RPC payload bytes**  
   The TriTRPC envelope carries Avro binary payloads for Knowledge Context RPC calls. These payloads are defined by an Avro protocol (`.avpr`).

2) **Event stream payloads**  
   Lifecycle events (note changed, claim proposed/validated) are defined as independent Avro record schemas (`.avsc`) intended for topic payloads.

## Subdirectories

- `schemas/avro/knowledge.store.v0/`  
  **Path-A RPC payload protocol** for `knowledge.store.v0`.
  - `knowledge.store.v0.avpr` defines types + messages for REQ/RESP.
  - This is the authoritative payload contract for TriTRPC Path-A.

- `schemas/avro/events.v1/`  
  **Lifecycle event schemas** for the Knowledge Context event stream.

## Determinism rules (important)

Avro encoding must be deterministic across implementations.

- Avoid Avro `map` types unless the implementation sorts keys lexicographically before encoding.
- Prefer arrays of `{key,value}` records (sorted by key) for deterministic “maps.”
- For free-form JSON blobs, store canonicalized bytes:
  - JCS (RFC 8785) is recommended for canonical JSON bytes fields.

## Binding to TriTRPC

TriTRPC framing and method naming are governed by:
- `docs/standards/030-tritrpc-binding.md`

Schema IDs are frozen by label in:
- `docs/standards/031-schema-context-id-registry.md`

The fixture suite verifies that:
- TriTRPC envelopes embed Avro payload bytes consistently
- AEAD/AAD boundaries are correct
- SCHEMA_ID/CONTEXT_ID and SERVICE/METHOD match the spec

## Related tooling

- `tools/avro_path_a_payloads.py`  
  Deterministic Avro payload generation for fixtures.
- `tools/verify_avro_path_a_roundtrip.py`  
  Round-trip semantic decode verification for Path-A payloads.

## Gates

From repo root:
- `make verify`
- `make roundtrip`

If Avro schemas change, fixtures and roundtrip checks must be updated accordingly.
