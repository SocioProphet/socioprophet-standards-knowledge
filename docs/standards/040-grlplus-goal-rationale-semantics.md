# 040 — GRLPlus Goal/Rationale Semantics Standard v0.1

## Status

Draft canonical standard.

## Purpose

GRLPlus standardizes computable goal/rationale models for SocioProphet knowledge governance. It extends GRL-style goal modeling with RationalGRL-style argumentation, evidence, semantic linting, and exportable governance worklists.

The standard exists to make goal models auditable and executable rather than diagram-only.

## Scope

GRLPlus owns the canonical shape for:

- actors and ownership boundaries;
- intentional elements: goal, softgoal, task, resource, belief;
- contribution and dependency edges;
- decomposition groups with `and`, `ior`, and `xor` operators;
- argument nodes and support/attack links;
- trace links binding arguments to elements, edges, and decomposition groups;
- evidence references;
- lint report shape;
- metrics report shape;
- semantic action/worklist handoff obligations.

## Non-goals

GRLPlus does not directly own repo-specific export bindings. Repo-bound GitHub issue and ops-queue export adapters may live in integration repositories such as `SocioProphet/socioprophet`, but those adapters must treat this repository as the canonical source for the generic GRLPlus model, lint, and metrics semantics.

GRLPlus also does not define a full formal decision calculus in v0.1. The initial semantic layer is a bounded scaffold: argument confidence, scalar satisfaction signal, interval satisfaction signal, semantic divergence, critical-path action posture, and worklist generation.

## Canonical artifacts

The initial canonical artifacts are:

- `schemas/jsonschema/grlplus/model.schema.json`
- `schemas/jsonschema/grlplus/lint-report.schema.json`
- `schemas/jsonschema/grlplus/metrics-report.schema.json`

Integration adapters should import these schemas or pin a versioned copy with explicit provenance.

## Model invariants

A valid GRLPlus model MUST satisfy:

1. globally unique IDs across actors, elements, edges, decomposition groups, arguments, argument links, trace links, and evidence;
2. no dangling references;
3. no self-loop for contribution, dependency, support, or attack;
4. decomposition groups must not duplicate children;
5. task and resource elements must have an owner actor;
6. accepted arguments should trace to at least one modeled target;
7. top-level goals should have at least one inbound contribution or decomposition group;
8. evidence IDs referenced by arguments or edges should exist in the evidence collection.

## Semantic surfaces

GRLPlus metrics SHOULD distinguish:

- `element_confidence`: argument-trace posture, not propagated satisfaction;
- `satisfaction_scaffold`: scalar propagated support/drag;
- `satisfaction_interval_scaffold`: low/high interval posture;
- `semantic_diff`: divergence between argument confidence and propagated structure;
- `critical_path`: critical elements only;
- `semantic_action_report`: intervention categories and reason codes;
- `semantic_worklist`: export-ready governance tasks.

## Reason-code discipline

Semantic worklists SHOULD use stable reason codes rather than prose-only findings.

Initial reason-code families include:

- `RC_DIRECT_ARGUMENT_COVERAGE_MISSING`
- `RC_CONFIDENCE_SCALAR_GAP`
- `RC_CONFIDENCE_INTERVAL_GAP`
- `RC_WIDE_INTERVAL`
- `RC_CROSS_ACTOR_DEPENDENCY_UNCERTAINTY`
- `RC_CONTRADICTORY_TRADEOFF`
- `RC_SCALAR_INTERVAL_DIRECTION_OPPOSED`

## Integration with SocioProphet/socioprophet

`SocioProphet/socioprophet` may own repo-specific adapters for public/docs/integration surfaces. Its GRLPlus export contracts should be treated as adapter bindings over this canonical standard, not as the canonical source of GRLPlus semantics.

The integration adapter may define:

- GitHub issue bundle schema;
- ops-queue bundle schema;
- repo-specific GitHub binding presets;
- domain action policy defaults;
- CI helpers that validate generated worklists against strict export schemas.

## Evolution

Changes to the canonical model, lint, or metrics schema MUST update:

- the corresponding JSON Schema;
- this standard document when semantics change;
- fixtures and validators once executable fixture harnesses are introduced.

Versioned breaking changes SHOULD use a new schema version rather than mutating v0.1 behavior silently.
