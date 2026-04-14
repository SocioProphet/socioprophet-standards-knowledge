# 051 — Masonmark Drive Activity Reporting Pilot Standard

## Status
Draft v0.1 for Evidence / Investigation Reporting live-bind track.

## Purpose
This standard defines the second Masonmark pilot family for **Drive Activity / Investigation Reporting**. It packages a bounded, schema-first, replayable intent-to-contract flow for one curated schema:
- `EV-DRV-001` — Drive activity reporting

The pilot uses a stable logical view name before live governed-view binding:
- `gv.ev.drive_activity_reporting.v1`

## Normative requirements
1. Masonmark MUST compile into a schema-grounded program path, not free-form execution.
2. Every promoted result MUST be represented by a proof-bearing `Stele` envelope linked to a `Proofpack`.
3. Commonsense sources MAY assist lexical normalization and plausibility ranking, but MUST be tagged as defeasible and non-authoritative.
4. Internal event, role, and time IDs MUST be present.
5. The first live bind SHOULD prioritize non-PII columns; sensitive columns (e.g., IP address) MUST remain denylisted until policy and redaction are shipped.

## Alignment hooks
- KAIROS: treat each row as an event instance with participants and temporal anchoring; support schema learning from event sequences.
- CHRONOS: represent before/after/during constraints and detect temporal inconsistencies.
- CSKG: use as a defeasible lexical and plausibility prior only.

## Internal ID blocks
- Event types: `mm.evt.ev.*`
- Roles: `mm.role.ev.*`
- Time anchors: `mm.time.ev.*`

## Acceptance gate
The pilot fixture corpus MUST include at least:
- 3 positive paths
- 3 abstention paths
- 3 robustness paths

The first live bind MUST target exactly one approved logical view and MUST emit at least one live proofpack before broader rollout.

## Files introduced by this standard
- `fixtures/masonmark/drive_activity_reporting.*.json`
- `data/drive_activity_reporting_demo.csv`
- `tools/masonmark_run_drive_activity_fixtures.py`

## Deferred items
- production policy bundle for PII exports
- warehouse-specific DDL and access controls
- explicit external ontology crosswalks
- learned schema extraction; v0.1 remains fixture-driven
