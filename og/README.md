# Ontogenesis Canonical Index

This repository now carries the initial **Ontogenesis core registry** for the SocioProphet platform.

## Canonical base IRI

`https://socioprophet.github.io/ontogenesis/`

## Canonical module paths

- `og/ontologies/parent.ttl`
- `prophet/ontologies/prophet_cli_ontology.ttl`
- `Lower/ontologies/bindings.ttl`
- `ontologies/human.ttl`
- `ontologies/socioprophet.ttl`
- `policy/shapes/master.shacl.ttl`
- `policy/tools/validate_all.py`

## Canonical prefixes

- `og` — parent / registry surface
- `prop` — Prophet CLI ontology
- `bind` — atomic on-device bindings
- `human` — privacy-first human / phenotype surface
- `sp` — SocioProphet runners / experiments / metrics

## Naming freeze

- `Genesys` is the canonical **platform-plane** term.
- `G0` is the first adoption gate and may retain the human-facing label **"Genesis OK"**.
- `G1` is the second adoption gate and may retain the human-facing label **"Inception Stable"**.
- `ontologies/prophet.ttl` is a **deprecated shim only**. New imports MUST target `prophet/ontologies/prophet_cli_ontology.ttl`.

## Scope of the core registry

The core parent registry currently normalizes only four modules:

1. Prophet CLI
2. Atomic Bindings
3. Human
4. SocioProphet

K8s, ITSM, Linux, and GitHub remain explicit add-in modules to fold into the registry later.
