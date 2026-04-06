# 050 — Masonmark Grant Stewardship Pilot Standard

## Status
Draft v0.1 for Knowledge Context pilot packaging.

## Purpose
This standard defines the first Masonmark pilot family for **Grant Stewardship**. It packages a bounded, schema-first, replayable intent-to-contract flow for three curated schemas:
- `GS-AWD-001` — award reporting
- `GS-AMD-002` — amendment governance
- `GS-CLO-003` — closeout compliance

The pilot uses stable logical view names before live governed-view binding:
- `gv.gs.award_reporting.v1`
- `gv.gs.amendment_delta.v1`
- `gv.gs.closeout_compliance.v1`

## Normative requirements
1. Masonmark MUST compile into a schema-grounded program path, not free-form execution.
2. Every promoted result MUST be represented by a proof-bearing `Stele` envelope linked to a `Proofpack`.
3. Commonsense sources MAY assist lexical normalization and plausibility ranking, but MUST be tagged as defeasible and non-authoritative.
4. External ontology alignment MAY remain null in v0.1, but internal event, role, and time IDs MUST be present.
5. Live physical bindings are explicitly out of scope for this draft; demo bindings are used only to freeze interfaces and fixture expectations.

## Internal ID blocks
- Event types: `mm.evt.gs.*`
- Roles: `mm.role.gs.*`
- Time anchors: `mm.time.gs.*`

## Acceptance gate
The pilot fixture corpus MUST include at least:
- 3 positive paths
- 3 abstention paths
- 3 robustness paths

The first live bind MUST target exactly one approved governed view and MUST emit at least one live proofpack before broader rollout.

## Files introduced by this standard
- `schemas/masonmark/*.schema.json`
- `fixtures/masonmark/grant_stewardship.*.json`

## Deferred items
- named human owners and approvers
- warehouse-specific DDL and access controls
- external ontology crosswalks
- learned proposal model; v0.1 remains fixture-driven
