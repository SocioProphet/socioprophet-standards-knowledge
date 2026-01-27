# Upstream Dependencies

This repo is governed by platform-wide invariants defined in:
- Repo: SocioProphet/socioprophet-standards-storage
- Pinned commit: 7844457feb9863f7ea037348364962604f39fdab

MUST comply with (in the upstream repo):
- docs/standards/020-data-formats.md
- docs/standards/030-service-interfaces-tritrpc.md
- docs/standards/070-graph-rdf-hypergraph.md

Compatibility statement:
- Knowledge Context v0.1 targets Storage Standards v0.1+ at the pinned commit above.

## RPC Transport Authority (TriTRPC)
This repo uses **TriTRPC v1** as the canonical transport/envelope/encoding standard (aliases: triRPC, trirpc, triunerpc).

- Repo: SocioProphet/tritrpc
- Pinned commit (HEAD at time of update): 025907e49edfbb8c43f23e98d2f71a93a65cab6e

MUST comply with TriTRPC v1 envelope framing, deterministic encoding, and fixtures as defined in that repo.
