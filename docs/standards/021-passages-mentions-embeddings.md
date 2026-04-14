# Passages, Mentions, and Embeddings (Normative)

This document defines the minimal interoperable contract for text-node segmentation, mention anchoring, and vector references in the Knowledge Context.

## 1) Scope
The Knowledge Context MUST treat extracted text spans as first-class artifacts when they participate in retrieval, provenance, or graph expansion.

The canonical artifacts introduced here are:
- `Passage`
- `Mention`
- `EmbeddingRef`
- `VectorIndexRef`

## 2) Passage rules
- A `Passage` MUST anchor back to source content via `Anchor`.
- A `Passage` MUST carry the extracted text used for retrieval and replay.
- A `Passage` SHOULD be segmented at paragraph granularity by default unless a workload requires sentence, windowed, or semantic chunking.
- A `Passage` MAY reference one or more embedding identifiers.

## 3) Mention rules
- A `Mention` MUST bind a surface form in a passage to an `Entity` candidate.
- A `Mention` MUST include a confidence score.
- A `Mention` SHOULD preserve a selector where span coordinates are available.

## 4) Embedding rules
- Embeddings MUST be referenced via `EmbeddingRef`; raw float vectors MUST NOT be embedded into the canonical Knowledge Context JSON-LD or graph contracts.
- `EmbeddingRef` MUST identify the target node, embedding model, and vector index reference.
- `VectorIndexRef` MUST identify the backend and similarity metric.

## 5) Privacy and governance
- Masking and redaction controls MUST execute before embedding or publishing.
- Embedding generation MUST be traceable via `ProvenanceRecord` with `activity_type = embed`.

## 6) Retrieval posture
Hybrid retrieval SHOULD proceed as:
1. lexical and/or vector retrieval over passages;
2. mapping top-k passage hits back to canonical node identifiers;
3. graph expansion over entities, claims, annotations, and meriotopographic edges;
4. provenance-backed answer assembly.
