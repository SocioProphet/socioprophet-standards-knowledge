# SocioProphet Standards — Knowledge Context

We define the **Knowledge Context** standards package for SocioProphet: canonical knowledge artifacts (Note/Claim/Annotation/Edge), meriotopographic semantics (part/whole + placement + derivation + governance), and a **provable** transport/payload contract using **TriTRPC v1** + **Avro Path-A** + **byte fixtures**.

This repo is not “docs-only.” We treat standards as executable: schemas define shapes, fixtures define bytes, verifiers prove compliance, and round-trip checks prove semantic correctness.

## Authority chain

- **Platform governance / context index:** `SocioProphet/socioprophet-standards-storage`
- **Canonical transport / envelope / AEAD / framing:** `SocioProphet/tritrpc` (TriTRPC; we may say triRPC/trirpc/triunerpc interchangeably)

## Quickstart (single paste)

Run from the repo root:

`python3 -m venv .venv && ./.venv/bin/python -m pip install -U pip && ./.venv/bin/python -m pip install -r requirements-dev.txt && make hygiene && make verify && make roundtrip`

### Gates (must stay green)

- `make hygiene`  
  Removes `.DS_Store` races (macOS Finder) and runs `make validate`.
- `make validate`  
  Repo sanity checks (no `.DS_Store`, schema/workload parsing where applicable).
- `make verify`  
  TriTRPC fixture verification: AEAD/AAD boundary, schema/context IDs, SERVICE/METHOD decode, AUX coverage.
- `make roundtrip`  
  Avro Path-A semantic round-trip: encoded bytes decode back to deterministic sample objects.

### Versioned v1 gates

The default gates remain v0-compatible. The expanded v1 store surface uses explicit targets so v1 can be promoted without silently changing the frozen v0 fixture path:

- `make fixtures-v1`  
  Generates v1 TriTRPC fixture vectors and nonces using `rpc/knowledge.store.v1.yaml` and `schemas/avro/knowledge.store.v1/knowledge.store.v1.avpr`.
- `make verify-v1`  
  Verifies v1 fixture AEAD/AAD boundaries, schema/context IDs, SERVICE/METHOD decode, and AUX coverage.
- `make roundtrip-v1`  
  Verifies v1 Avro Path-A request/response payload decoding over the expanded store surface.

## What we standardize here

### 1) Canonical artifacts (knowledge atoms)
We standardize knowledge as explicit artifacts with provenance and validation fields:
- `Note`
- `Claim` (assertion + optional evidence + validation state)
- `Annotation` (anchored spans)
- `MeriotopographicEdge` (relations + governance)
- `ProvenanceRecord` (traceability spine)

Canonical structure is documented via JSON Schemas under `schemas/jsonschema/`.

### 2) Meriotopographics (meaning, not just links)
We define a predicate registry and invariants for:
- part/whole (e.g., `part_of`, `has_part`)
- placement/anchors (e.g., `located_in`, `anchors_to`, `overlaps`)
- derivation/provenance (e.g., `derives_from`)
- epistemic relations (e.g., `supports`, `contradicts`)
- governance/privacy (e.g., `validated_by`, `masked_by`, `redacted_by`)

See: `docs/standards/020-meriotopographics.md`

### 3) TriTRPC binding (transport is a contract)
We bind Knowledge Context RPC calls onto TriTRPC v1:
- envelope field ordering
- AEAD rule (AAD = bytes before tag field)
- schema/context IDs derived from frozen labels
- method naming conventions
- AUX behavior (when present, included in AAD)

See: `docs/standards/030-tritrpc-binding.md`  
Label/ID freeze: `docs/standards/031-schema-context-id-registry.md`

### 4) Avro Path-A payload contracts
TriTRPC Path-A uses Avro binary payload bytes. We define protocols for:
- `knowledge.store.v0` requests/responses (REQ/RESP methods); `v0` remains the initial placeholder store surface
- `knowledge.store.v1` expansion for `Annotation`, `ProvenanceRecord`, `Entity`, `Passage`, `Mention`, `EmbeddingRef`, and `EntityResolutionRecord`
- deterministic constraints (no nondeterministic maps; prefer arrays or canonicalized bytes)

See:
- `schemas/avro/knowledge.store.v0/knowledge.store.v0.avpr`
- `schemas/avro/knowledge.store.v1/knowledge.store.v1.avpr`

### 5) JSON-LD semantic overlay
We provide JSON-LD contexts for semantic expansion without changing wire payloads:
- canonical `v0` context: `schemas/jsonld/contexts/knowledge/context.jsonld`
- draft `v1` context: `schemas/jsonld/contexts/knowledge.v1/context.jsonld`

### 6) Lifecycle events (event-stream contracts)
We define minimal Avro event schemas (separate from RPC payloads):
- note changed
- claim proposed
- claim validated

See: `schemas/avro/events.v1/`

## Repo map (where to find things)

- `docs/standards/`  
  Normative documents (MUST/SHOULD language), registries, binding rules.
- `schemas/`  
  - `schemas/avro/` — Avro contracts (RPC payload protocol + lifecycle events)  
  - `schemas/jsonld/` — JSON-LD contexts  
  - `schemas/jsonschema/` — canonical structural schemas
- `rpc/`  
  Service surfaces and TriTRPC wire mapping metadata (e.g., `rpc/knowledge.store.v0.yaml`, `rpc/knowledge.store.v1.yaml`).
- `fixtures/`  
  Hex fixture vectors + nonces (TriTRPC compliance), including AUX coverage.
- `tools/`  
  Generators/verifiers and Avro payload helpers:
  - TriTRPC fixture generator + verifier
  - Avro payload byte builder (Path-A)
  - Avro round-trip verifier
- `benchmarks/`  
  Workload definitions and early benchmark tooling (report-first).

## Change control (how we evolve the standard)

This repo is a compatibility surface. When we change it, we change it carefully.

- If we change **envelope rules**, we update:
  - `docs/standards/030-tritrpc-binding.md`
  - fixtures in `fixtures/`
  - verifier in `tools/`
- If we change schema/context labels or IDs, we:
  - do **not** rename labels
  - add new labels (e.g., `KNOWLEDGE_AVRO_v1`)
  - update the registry `docs/standards/031-schema-context-id-registry.md`
- If we extend the store surface, we prefer adding a new versioned contract rather than mutating a frozen label in place.
- If we change payload schema semantics, we update:
  - Avro protocol (`.avpr`)
  - fixture generator (payload bytes)
  - JSON-LD contexts when semantic coverage changes
  - `make roundtrip` expectations

## Contributor workflow (house style)

- Work in `~/dev/` clones.
- Use `gh` CLI for PR operations.
- Keep changes small and mainline via PR merges.
- Always run:
  - `make hygiene && make verify && make roundtrip`
  before pushing a PR.
- For v1-specific validation, also run:
  - `make fixtures-v1 && make verify-v1 && make roundtrip-v1`
  before promoting v1 fixture files or verification status.

_Last updated: update via PR when this README changes_
