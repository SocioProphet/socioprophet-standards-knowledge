# 044 — Capability Plane Registry

## Status

**Draft.** This document records the current capability-plane registry for capability descriptors.

This document is normative for the standards and validation surface.

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

This closes the prior contradiction where visualization and chart bundles were exported as capability artifacts with `plane: viz` while the capability-plane type system rejected `viz`.

## Scope

This decision affects standards and validation surfaces first. Runtime and CI consumers must update their validators to use the same enum.

## Renumbering note

This document is replayed onto the current `main` line after the Capability Fabric package occupied `040` through `043`, so the registry is renumbered here to avoid numbering collisions with already-landed standards.
