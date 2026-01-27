# Knowledge Context JSON-LD (v0)

This directory defines the canonical JSON-LD context for Knowledge Context artifacts.

## Canonical label and TriTRPC binding
- Context label: `KNOWLEDGE_JSONLD_v0`
- CONTEXT_ID (SHA3-256 label): `4aa071d983aed812efa04171781ac976562f88239e09aa17ad4769d3dfad1c69`

This label/ID pair is referenced by:
- `docs/standards/030-tritrpc-binding.md`
- `rpc/knowledge.store.v0.yaml` (`tritrpc_wire.context_*`)

## Scope
This context provides a semantic overlay for:
- Note / Claim / Annotation / MeriotopographicEdge

## Predicate values
`predicate` is typed as `@vocab`, so values such as `part_of` expand to:
- `https://socioprophet.org/ns/knowledge#part_of`
