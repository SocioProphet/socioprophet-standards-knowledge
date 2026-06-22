# SocioProphet/socioprophet GRLPlus export adapter

`SocioProphet/socioprophet` hosts a repo-bound integration adapter for GRLPlus semantic worklists.

That adapter may own:

- GitHub issue export bundle schema;
- ops-queue export bundle schema;
- repo-specific GitHub binding presets;
- domain action policy defaults used by the public/integration surface;
- CI helpers that validate generated worklists against strict export schemas.

This repository owns the canonical GRLPlus model, lint, and metrics semantics. The adapter should therefore treat these files as the upstream semantic source:

- `docs/standards/040-grlplus-goal-rationale-semantics.md`
- `schemas/jsonschema/grlplus/model.schema.json`
- `schemas/jsonschema/grlplus/lint-report.schema.json`
- `schemas/jsonschema/grlplus/metrics-report.schema.json`

## Current adapter status

The `socioprophet` adapter includes strict export contracts and validation helpers for:

- generic input fixture export;
- report-shape example fixture export;
- generated contradictory semantic report export;
- generated positive semantic report export;
- output invariant snapshot checks.

## Versioning rule

When the canonical GRLPlus schema changes here, adapter repos should update their pinned import/copy explicitly and record the source commit or release. Adapter repos should not silently fork model, lint, or metrics semantics.
