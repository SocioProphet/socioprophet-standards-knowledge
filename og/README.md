# SocioProphet Ontogenesis Canonical Index (Wave 1)

This file is the normative naming and layout index for the Ontogenesis semantic core.

## Canonical base IRI

`https://socioprophet.github.io/ontogenesis/`

## Canonical prefixes

- `prop` — Prophet CLI ontology
- `bind` — Atomic bindings / Lower layer
- `human` — Human privacy-aware ontology
- `sp` — SocioProphet runners / experiments / reports
- `og` — Ontogenesis parent / core index

Deferred ecosystem modules to fold later:

- `k8s`
- `itsm`
- `lnx`
- `gh`

## Canonical module paths

- `og/ontologies/parent.ttl`
- `prophet/ontologies/prophet_cli_ontology.ttl`
- `prophet/contexts/prophet_cli.context.jsonld`
- `Lower/ontologies/bindings.ttl`
- `Lower/contexts/bindings.context.jsonld`
- `ontologies/human.ttl`
- `ontologies/socioprophet.ttl`
- `policy/shapes/master.shacl.ttl`
- `policy/tools/validate_all.py`

## Naming freeze

- `Genesys` is the canonical platform-plane term.
- `G0` may retain the human-readable label `Genesis OK`.
- `Genesis` must not be introduced as a platform-plane class IRI.

## Current canonical core registry

The core registry is intentionally limited to:

1. Prophet CLI
2. Atomic Bindings
3. Human
4. SocioProphet

K8s, ITSM, Linux, and GitHub remain deferred add-ins until the core is green in CI.

## Immediate deprecations

- `ontologies/prophet.ttl` is deprecated and should remain only as a temporary import shim.
- Active examples, dashboard imports, and CLI references must use `prophet/ontologies/prophet_cli_ontology.ttl`.

## Blocking type-system decision

Visualization bundles currently behave as first-class capability artifacts. Either:

1. add `viz` to the capability-plane enum and validator surface, or
2. stop representing chart bundles as CapDs.

No mixed state is allowed.
