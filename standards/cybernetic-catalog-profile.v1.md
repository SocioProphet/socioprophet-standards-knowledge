# Cybernetic Catalog Profile v1

## Purpose

The Cybernetic Catalog Profile defines the knowledge objects required for a catalog that teaches the platform across mathematics, physics, systems, and bio-evolutionary design.

This profile extends the existing Knowledge Context posture of explicit artifacts, claims, annotations, meriotopographic edges, and provenance records. It does not replace those atoms. It adds a scientific/cybernetic layer for model-bearing knowledge.

## Scope

The profile standardizes records for:
- model families
- equations
- variables
- unit bindings
- regimes
- assumptions
- evidence anchors
- contradictions
- benchmark tasks
- simulation runs
- operators
- cross-domain mappings

## Core principle

The catalog is not a document dump. It is a feedback-bearing semantic system.

Every catalog object SHOULD be able to answer:
- what claim, model, equation, or operator is represented
- what evidence supports it
- what assumptions and regimes bound it
- which units and variables are used
- what contradicts it
- what benchmark or simulation would test it
- how it projects into query lanes such as document, annotation, ontology, graph, and search

## Canonical record fields

A cybernetic catalog record MUST include:
- `id`
- `kind`
- `labels`
- `provenance`

A record SHOULD include:
- `domainTags`
- `relations`
- `evidence`
- `regimes`
- `assumptions`
- `validation`

## Record kinds

### ModelFamily
A family of models, not one fitted instance.

Examples:
- reaction-diffusion model family
- phase-field model family
- population-balance crystallization model family

### Equation
A formal equation or equation template.

Equation records SHOULD include:
- expression text
- variables
- dimensional constraints where known
- valid regimes
- derivation or evidence anchors

### Variable
A named mathematical or scientific variable.

Variable records SHOULD include:
- symbol
- quantity kind
- unit binding where known
- admissible range where known

### UnitBinding
A machine-checkable unit or dimensional constraint.

### Regime
A validity envelope for a claim, equation, model, operator, or mapping.

### Assumption
A declared condition required by a claim or model.

### EvidenceAnchor
A provenance-bearing pointer to a source span, artifact, dataset, simulation, benchmark, or fixture.

### Contradiction
A structured conflict between claims, models, mappings, evidence, or regimes.

### BenchmarkTask
A task that tests whether a catalog object is usable, valid, reproducible, or appropriately bounded.

### SimulationRun
A generated or executed run used as evidence.

### Operator
A reusable cybernetic/scientific operator such as diffusion, feedback, selection, inhibition, nucleation, growth, aggregation, control, or adaptation.

### CrossDomainMapping
A typed bridge between domains. The mapping MUST distinguish exact equivalence, reduction, approximation, analogy, and metaphorical relation.

## Relation discipline

Cross-domain links MUST be typed. A system MUST NOT silently collapse analogy, reduction, and equivalence.

Recommended relation types:
- `uses_operator`
- `has_variable`
- `has_unit_binding`
- `valid_in_regime`
- `assumes`
- `supported_by`
- `contradicted_by`
- `tested_by`
- `derived_from`
- `projects_to_lattice_lane`

## Lattice projection posture

The catalog SHOULD project into the platform Lattice query plane rather than inventing an independent retrieval plane.

Recommended projection lanes:
- document query
- annotation query
- ontology/SPARQL query
- property graph/Cypher query
- hypergraph/Atomese query
- Sherlock or Lampstand search records

## Validation posture

Implementations SHOULD provide fixtures and round-trip checks for:
- JSON structural validation
- JSON-LD expansion where applicable
- relation typing
- evidence anchor integrity
- unit/regime consistency where machine-checkable

## Non-goals

This profile does not standardize storage backend selection. Storage backend selection is governed by the storage-fabric standards and benchmark methodology.

This profile does not define runtime deployment topology. Runtime adoption belongs in platform implementation repositories.
