# Schema + Context ID Registry (Normative)

This registry freezes the string labels used to derive the 32-byte TriTRPC `SCHEMA_ID` and `CONTEXT_ID`.

Derivation rule (normative):
- ID = SHA3-256(label) (32 bytes)

## 1) Avro Path-A payload schema label
- Label: `KNOWLEDGE_AVRO_v0`
- SCHEMA_ID (hex): `a95570c2921b16ac12a9c0306e97399c669d9debf68d442c2ccaadcad8b6a092`
- Canonical path(s):
  - `schemas/avro/knowledge.store.v0/knowledge.store.v0.avpr`

## 2) JSON-LD context label
- Label: `KNOWLEDGE_JSONLD_v0`
- CONTEXT_ID (hex): `4aa071d983aed812efa04171781ac976562f88239e09aa17ad4769d3dfad1c69`
- Canonical path(s):
  - `schemas/jsonld/contexts/knowledge/context.jsonld`

## 3) Change control
- Labels MUST NOT be renamed.
- If a breaking change is required, create a new label (e.g., `KNOWLEDGE_AVRO_v1`) and update TriTRPC bindings accordingly.
