# Triune Agent Mesh Schemas

This directory is the schema landing zone for the Triune Agent Mesh framework.

## Scope

Machine-readable artifacts for:
- agent lifecycle, promotion, rollback, and evidence trails
- model cards, model profiles, behavioral profiles, patch bundles
- learning manifests, birth records, umbilical plans, reward manifests
- telemetry atoms, window shards, vector space specs, shard manifests
- distribution packs, semantic tombstones, drift and MoM check reports
- cohort specs, cohort window stats, experience index, fractal profiles
- model templates, distill manifests, promotion gate packs
- semantic fingerprints, fingerprint registries, sample plans, k-fold plans

## Intended layout

- `schemas/triune/avro/`
- `schemas/triune/jsonschema/`
- `schemas/triune/jsonld/`

## Contract relationship

- normative prose: `SocioProphet/socioprophet-standards-storage`
- ontology classes and semantic graph: `SocioProphet/ontogenesis`
- implementation-facing typed contracts: `SourceOS-Linux/sourceos-spec`
- runtime/controller integration: `SocioProphet/sociosphere`

This file is the initial anchor commit for the schema layer.
