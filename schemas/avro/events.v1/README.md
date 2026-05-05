# Knowledge Context — Lifecycle Events (Avro, v1)

These schemas define event-stream contracts (topic payloads), separate from TriTRPC Path-A RPC payloads.

## Topics (recommended)
- socioprophet.knowledge.note.changed.v1
- socioprophet.knowledge.claim.proposed.v1
- socioprophet.knowledge.claim.validated.v1
- socioprophet.knowledge.passage.indexed.v1
- socioprophet.knowledge.embedding.attached.v1
- socioprophet.knowledge.entity.resolved.v1
- socioprophet.knowledge.provenance.recorded.v1

## Notes
- Event schemas are intentionally minimal and stable.
- Detailed state lives in the Knowledge Store (queried via TriTRPC RPC).
- Passage, embedding, entity-resolution, and provenance events are emitted as lifecycle hooks around the expanded `knowledge.store.v1` surface.
