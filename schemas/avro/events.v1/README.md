# Knowledge Context — Lifecycle Events (Avro, v1)

These schemas define event-stream contracts (topic payloads), separate from TriTRPC Path-A RPC payloads.

## Topics (recommended)
- socioprophet.knowledge.note.changed.v1
- socioprophet.knowledge.claim.proposed.v1
- socioprophet.knowledge.claim.validated.v1

## Notes
- Event schemas are intentionally minimal and stable.
- Detailed state lives in the Knowledge Store (queried via TriTRPC RPC).
