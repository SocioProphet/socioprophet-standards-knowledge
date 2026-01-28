# docs/standards/

This directory contains **normative** specifications for the SocioProphet **Knowledge Context** standards package.

These documents use RFC-style language:
- **MUST** / **MUST NOT** = mandatory for compliance
- **SHOULD** / **SHOULD NOT** = strongly recommended (exceptions must be justified)
- **MAY** = optional

## What lives here

### Core normative specs
- `000-knowledge-platform-standards.md`  
  Scope, principles, and what “Knowledge Context” covers.

- `001-upstream-dependencies.md`  
  Upstream authority pins (platform governance + TriTRPC transport authority).

- `020-meriotopographics.md`  
  Predicate registry + invariants for meriotopographic relations (part/whole, placement, derivation, epistemic, governance).

- `030-tritrpc-binding.md`  
  TriTRPC v1 binding for Knowledge Context (envelope ordering, AEAD/AAD boundary, SERVICE/METHOD conventions, AUX semantics).

- `031-schema-context-id-registry.md`  
  Frozen **label → ID → path** registry for SCHEMA_ID/CONTEXT_ID (prevents silent drift).

- `032-tritrpc-knowledge-fixtures.md`  
  Fixture semantics, regeneration rules, and change control for byte-level compliance vectors.

## How docs relate to enforceable compliance

This repo treats standards as **executable**:
- **Schemas** define shapes (`schemas/`)
- **Fixtures** define bytes (`fixtures/`)
- **Verifiers** prove compliance (`tools/`)
- **Roundtrip** proves semantic correctness (`make roundtrip`)

Any doc change that affects:
- envelope framing / AEAD rules,
- schema/context labels or IDs,
- method naming,
- payload semantics,

MUST be accompanied by updates to:
- fixtures (hex vectors + nonces),
- verifiers,
- and any affected round-trip checks.

## Editing rules

- Prefer **precise** requirements over prose.
- Avoid ambiguity in anything that influences bytes or determinism.
- Keep “transport” (TriTRPC) separate from “semantics” (meriotopographics + artifact meaning).
- When adding new requirements, update fixtures/tests in the same PR or clearly mark the doc as `draft`.

## Running the gates

From repo root:

- `make hygiene` (cleans `.DS_Store` + runs validate)
- `make verify` (TriTRPC fixture verification)
- `make roundtrip` (Avro semantic round-trip verification)

## Upstream references

- TriTRPC authority: `SocioProphet/tritrpc` (TriTRPC; aliases: triRPC/trirpc/triunerpc)
- Platform governance index: `SocioProphet/socioprophet-standards-storage`
