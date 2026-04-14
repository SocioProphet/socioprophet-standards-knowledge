# Capability Plane Registry

This document records the current capability-plane registry for capability descriptors.

## Current plane enum

- `cloud`
- `ai`
- `serve`
- `msg`
- `svc`
- `pkg`
- `r`
- `fs`
- `graph`
- `gib`
- `twin`
- `agents`
- `viz`

## Decision

`viz` is admitted as a first-class capability plane.

This closes the prior contradiction where visualization/chart bundles were exported as capability artifacts with `plane: viz` while the capability-plane type system rejected `viz`.

## Scope

This decision affects standards and validation surfaces first. Runtime and CI consumers must update their validators to use the same enum.
