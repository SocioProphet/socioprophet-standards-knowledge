# Registri Schema + Context ID Registry (Normative Draft)

This registry freezes the string labels used to derive the 32-byte TriTRPC `SCHEMA_ID` and `CONTEXT_ID`
for the first Entity Registri / Proof Fabric package.

Derivation rule (normative):
- ID = SHA3-256(label) (32 bytes)

## 1) Avro Path-A payload schema label
- Label: `REGISTRI_AVRO_v0`
- SCHEMA_ID (hex): `c6a09192f2d917badfa53415d8499f3edc67068c5974bf9a7be367306f7eb340`
- Canonical path(s):
  - `schemas/avro/registri.store.v0/registri.store.v0.avpr`

## 2) JSON-LD context label
- Label: `REGISTRI_JSONLD_v0`
- CONTEXT_ID (hex): `d9edf86e9b97bfeb5bbb4d8972e1c74b6e0de0bd1c172bc1c4093d11e61e0358`
- Canonical path(s):
  - `schemas/jsonld/contexts/registri/context.jsonld`

## 3) Change control
- Labels MUST NOT be renamed.
- If a breaking change is required, create a new label (for example `REGISTRI_AVRO_v1`) and bind it in a new package version.
- Package index entries MUST resolve to the same canonical paths declared here.
