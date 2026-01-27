# TriTRPC Knowledge Context Fixtures (Normative)

This repo includes a minimal fixture suite proving TriTRPC envelope compliance for Knowledge Context.

## Files
- `fixtures/knowledge_vectors_hex_pathA.txt`
- `fixtures/knowledge_vectors_hex_pathA.txt.nonces`

## What is verified
- AEAD tag correctness: XChaCha20-Poly1305, **key = 0x00 * 32**, nonce from `.nonces`, plaintext empty, AAD = envelope bytes prior to tag field.
- SCHEMA_ID / CONTEXT_ID match labels frozen in `docs/standards/031-schema-context-id-registry.md`.
- SERVICE and METHOD decode match fixture names.

## Regeneration
Run:
- `python3 tools/generate_knowledge_tritrpc_fixtures.py`
Then verify:
- `python3 tools/verify_knowledge_tritrpc_fixtures.py`

Fixtures MUST only change when labels or envelope rules change (both are governed by change control).
