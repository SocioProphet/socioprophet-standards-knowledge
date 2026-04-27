# 080 — Multi-Domain Geospatial Knowledge Context

Status: Draft v0.1
Authority: `SocioProphet/socioprophet-standards-knowledge`
Related: `SocioProphet/prophet-platform-standards/docs/standards/070-multidomain-geospatial-standards-alignment.md`

## Purpose

This standard defines the semantic and provenance context for multi-domain geospatial intelligence artifacts.

It covers ontology alignment, JSON-LD context placement, meriotopographic relations, provenance, claim/evidence semantics, redaction, masking, and entity-resolution obligations for Earth, space, air, maritime, land, smart-space, and public-safety domains.

## Canonical semantic families

The following semantic families are in scope:

- `GeoEntity`: any geospatially anchored entity.
- `Place`: a named or bounded location.
- `Feature`: a map or observed feature.
- `Asset`: a physical or logical asset with geospatial or operational presence.
- `SpaceAsset`: satellite, spacecraft, constellation, payload, ground station, or orbital object.
- `Vessel`: ship, boat, maritime asset, or vessel identity abstraction.
- `Aircraft`: aircraft, drone, airport vehicle, or air-domain asset.
- `Sensor`: physical, logical, remote-sensing, field, or platform sensor.
- `Observation`: evidence-bearing measurement or report.
- `Track`: time-ordered position/evidence chain.
- `Event`: operational, environmental, safety, infrastructure, or mission event.
- `DecisionCard`: advisory decision artifact with evidence and constraints.
- `SensitiveGeoPolicy`: masking, redaction, delay, access-control, or jurisdictional rule.

## Required relation families

The predicate registry MUST include relations for:

- containment and part/whole: `part_of`, `has_part`, `contained_by`, `contains`
- location and geometry: `located_at`, `located_in`, `intersects`, `overlaps`, `near`, `within_route_corridor`
- derivation and provenance: `derived_from`, `observed_by`, `reported_by`, `validated_by`, `fused_from`
- temporal ordering: `precedes`, `follows`, `during`, `valid_for`, `supersedes`
- evidentiary semantics: `supports`, `contradicts`, `qualifies`, `requires_review`
- operational semantics: `assigned_to`, `tasked_by`, `responds_to`, `affects_asset`, `affects_route`
- governance semantics: `masked_by`, `redacted_by`, `restricted_by`, `licensed_by`, `authorized_by`

## JSON-LD and ontology requirements

Multi-domain geospatial artifacts SHOULD have JSON-LD contexts that preserve:

- stable entity identifiers
- source identifiers
- geometry identifiers
- time semantics
- provenance references
- confidence and uncertainty
- license and attribution
- sensitive-location policy references
- runtime boundary and evidence references

## Provenance discipline

A semantic assertion MUST NOT be treated as authoritative unless its provenance is explicit.

Every derived feature, track, anomaly, or decision card SHOULD be traceable to source observations, source products, runtime boundary evidence, or human/organizational assertion records.

## Sensitive geospatial knowledge

Sensitive geospatial data must be modeled as policy-bound knowledge, not merely hidden fields. Redaction and masking SHOULD preserve the fact that a protected object exists when policy allows that meta-fact, while withholding exact details according to `SensitiveGeoPolicy`.

## Implementation rule

GAIA ontology repos and implementation repos may propose terms and fixtures, but stable multi-domain semantics must be promoted here or reference this draft standard before becoming canonical.
