# TriTRPC v1 Binding for Entity Registri / Proof Fabric (Normative Draft)

## 0. Authority

The canonical transport / envelope / framing spec remains **TriTRPC v1**.
This document binds the Registri / Proof Fabric package onto that transport without changing the
upstream TriTRPC standard.

## 1. Scope

This binding covers the first package surface for:

- `Entity`
- `ArtifactManifest`
- `HyperedgeRecord`
- `CheckpointManifest`

It does **not** define a rival graph query protocol. RDF / property graph / hypergraph interrogation
continues to ride `graph.store.v0` from the upstream platform standards.

## 2. SERVICE / METHOD naming

- SERVICE: `registri.store.v0`
- METHOD (requests): `<MethodName>_a.REQ`
- METHOD (responses): `<MethodName>_a.RESP`
- `_a` denotes Path-A (Avro binary payload)

## 3. Path-A payload authority

The canonical Path-A payload contract for this package is:

- `schemas/avro/registri.store.v0/registri.store.v0.avpr`

## 4. Schema + Context labels

- `REGISTRI_AVRO_v0`
- `REGISTRI_JSONLD_v0`

See the ID registry for the frozen SHA3-256 derivations.

## 5. Determinism constraints

To preserve cross-language byte equality:

- Avoid Avro maps unless keys are sorted lexicographically before encoding.
- Prefer arrays of `{key, value_jcs}` records for semantic maps.
- Any free-form object MUST be canonicalized with RFC 8785 (JCS) and stored as bytes.
- `HyperedgeRecord.participants` MUST preserve declared order.
- `HyperedgeRecord.support_refs` and `rebuttal_refs` SHOULD be stable-sorted when generated mechanically.

## 6. Package split

This binding assumes the following coordinated package split:

- Avro = Path-A payload contract
- JSON-LD = semantic overlay
- JSON Schema = authoring / editor validation surface
- Fixtures = transport compliance evidence
- Bundle manifest / package index = schema lookup and downstream import entrypoints
