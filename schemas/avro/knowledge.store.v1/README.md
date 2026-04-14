# knowledge.store.v1

This directory is reserved for the first non-placeholder Avro Path-A protocol for the Knowledge Context store.

Planned canonical artifact coverage:
- Note
- Annotation
- Claim
- MeriotopographicEdge
- ProvenanceRecord
- Entity
- Passage
- Mention
- EmbeddingRef
- EntityResolutionRecord

Activation requirements before this protocol is treated as authoritative:
1. add `knowledge.store.v1.avpr`;
2. freeze `KNOWLEDGE_AVRO_v1` in `docs/standards/031-schema-context-id-registry.md`;
3. add `KNOWLEDGE_JSONLD_v1` and the matching context file;
4. extend fixture and round-trip tooling.
