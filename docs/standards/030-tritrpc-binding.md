# TriTRPC v1 Binding for Knowledge Context (Normative)

## 0. Authority
The canonical transport/envelope/encoding spec is **TriTRPC v1**:
- Repo: SocioProphet/tritrpc
- Pinned commit: 025907e49edfbb8c43f23e98d2f71a93a65cab6e

Aliases used interchangeably in conversation: triRPC, trirpc, triunerpc. In documents we write **TriTRPC**.

## 1. Envelope field order (Path-A)
A TriTRPC v1 frame is a concatenation of length-prefixed fields:

Each field is encoded as:
- `TLEB3(len(field_bytes)) || field_bytes`

Field sequence (canonical):
1. `MAGIC_B2` = bytes `F3 2A` (2 bytes), length-prefixed
2. `VER` = `TritPack243([1])`, length-prefixed
3. `MODE` = `TritPack243([0])` (B2 mode), length-prefixed
4. `FLAGS` = `TritPack243([aead, compress, 0])`, length-prefixed
   - `aead` trit: 2=true, 0=false
   - `compress` trit: 2=true, 0=false
5. `SCHEMA_ID` (32 bytes), length-prefixed
6. `CONTEXT_ID` (32 bytes), length-prefixed
7. `SERVICE` UTF-8 bytes, length-prefixed
8. `METHOD` UTF-8 bytes, length-prefixed
9. `PAYLOAD` bytes, length-prefixed
10. Optional `AUX` bytes, length-prefixed
11. Optional `AEAD_TAG` bytes (16 bytes), length-prefixed

## 2. AEAD rule (normative)
When AEAD is enabled:
- Suite: XChaCha20-Poly1305
- Nonce: 24 bytes
- Plaintext: empty (`b""`)
- **AAD** = exact envelope bytes **up to (but not including)** the length prefix of the final tag field.

## 3. Schema + Context IDs (normative for Knowledge Context)
We derive 32-byte IDs deterministically:
- `SCHEMA_ID = SHA3-256("KNOWLEDGE_AVRO_v0")`
  - hex: `a95570c2921b16ac12a9c0306e97399c669d9debf68d442c2ccaadcad8b6a092`
- `CONTEXT_ID = SHA3-256("KNOWLEDGE_JSONLD_v0")`
  - hex: `4aa071d983aed812efa04171781ac976562f88239e09aa17ad4769d3dfad1c69`

Bindings:
- Avro payload schemas: `schemas/avro/` (next)
- JSON-LD contexts: `schemas/jsonld/contexts/knowledge/context.jsonld`

## 4. SERVICE / METHOD naming (normative)
- SERVICE: `knowledge.store.v0`
- METHOD (requests): `<MethodName>_a.REQ`
- METHOD (responses): `<MethodName>_a.RESP`
Where `_a` denotes Path-A (Avro binary payload).

## 5. Determinism constraints (payload-level)
To preserve cross-language byte equality:
- Avoid Avro `map` types unless keys are sorted lexicographically before encoding.
- Prefer arrays of `{key,value}` records (sorted by key) for semantic maps.
- Any “free-form object” MUST be canonicalized using RFC 8785 (JCS) and stored as bytes.

## 6. Compliance checklist (v0.1)
Compliant implementations:
- Produce envelopes matching the field order and length-prefix rules above.
- Compute AEAD tags using the AAD rule above.
- Use the derived schema/context IDs exactly as specified.
- Use the SERVICE/METHOD naming conventions above.
