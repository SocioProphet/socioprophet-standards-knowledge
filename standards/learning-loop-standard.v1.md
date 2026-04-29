# Learning Loop Knowledge Standard v1

Status: draft
Owner: SocioProphet standards knowledge
Scope: systems learning loops, public-sector innovation case studies, cybernetics, institutional learning, agent learning, MLOps learning loops, and platform governance.

## Purpose

This standard defines how SocioProphet represents learning loops as evidence-bound knowledge objects rather than informal narrative. It is intentionally broad enough to cover early internet learning, cybernetic feedback systems, public-sector innovation systems, MLOps feedback loops, SourceOS lifecycle loops, and agent learning loops.

The standard does not define a defense product. Public-sector and national-security innovation programs are modeled only as case studies in institutional learning, capability transition, evidence production, and feedback governance.

## Core principle

Every learning-loop record MUST preserve the chain:

```text
Need or signal -> challenge or objective -> intervention -> evidence -> feedback -> transition decision -> doctrine or system update
```

No learning-loop claim is accepted without provenance, confidence, and claim-status metadata.

## Required classes

Implementations SHOULD map these terms into RDF/Turtle, JSON Schema, or graph-native equivalents.

- `LearningLoop`: a bounded feedback system that learns from evidence and changes behavior, policy, model state, doctrine, software, or deployment state.
- `Institution`: an organization, alliance, agency, lab, program office, platform, project, or community operating a learning loop.
- `Program`: a named initiative under an institution.
- `Initiative`: a narrower scoped effort, call, challenge, workstream, experiment, or portfolio.
- `Challenge`: a demand signal transformed into a bounded problem statement.
- `FundingInstrument`: grants, contracts, prizes, accelerator capital, venture capital, procurement vehicles, or internal allocation.
- `Prototype`: an artifact built to test a hypothesis or capability.
- `TestEnvironment`: lab, test range, sandbox, simulation, battlefield feedback path, model evaluation suite, or staging environment.
- `OperationalUser`: the user, community, team, mission owner, developer, analyst, fleet, or agent that supplies feedback.
- `FeedbackSignal`: measurable result, qualitative signal, evaluation score, operational lesson, incident, bug report, telemetry, or review finding.
- `EvidenceArtifact`: source, citation, dataset, log, manifest, model card, run output, transcript, provenance record, attestation, or review record.
- `TransitionGate`: decision point for fielding, adoption, promotion, rollback, rejection, or further research.
- `DoctrineUpdate`: documented change to policy, architecture, agent behavior, platform primitive, model lifecycle, curriculum, or operational process.
- `Capability`: a reusable function, primitive, product capability, operational capability, model capability, or infrastructure capability.
- `TechnologyDomain`: AI, autonomy, cyber, networking, quantum, biotech, energy, geospatial, space, MLOps, OS lifecycle, platform governance, or other domain.
- `SourceRecord`: a structured record for all evidence sources backing a claim.
- `ConfidenceRating`: an explicit rating of how much trust to assign to a claim.

## Required fields for a LearningLoop record

```yaml
id: stable identifier
name: human readable name
loop_type: controlled vocabulary
summary: concise description
scope: local | project | organization | alliance | public-sector | platform | model | os-fleet | agent
actors: list of Institution or Agent references
input_signal: Need, Challenge, or FeedbackSignal reference
intervention: Prototype, Program, Model, Policy, or Software reference
evidence_artifacts: list of EvidenceArtifact references
feedback_signals: list of FeedbackSignal references
transition_gate: TransitionGate reference
doctrine_update: DoctrineUpdate reference, if any
technology_domains: list of TechnologyDomain values
source_records: list of SourceRecord references
confidence_rating: high | medium | low | contested | unknown
claim_status: established | inferred | speculative | deprecated | disputed
last_reviewed: ISO-8601 date
owner: repository or steward
```

## Loop taxonomy

The following loop types are canonical for v1:

- `ChallengeToPrototypeLoop`
- `PrototypeToFieldLoop`
- `OperationalFeedbackLoop`
- `FundingToFieldingLoop`
- `ProcurementTransitionLoop`
- `DoctrineUpdateLoop`
- `InstitutionalMemoryLoop`
- `ModelTrainingLoop`
- `ModelEvaluationLoop`
- `ModelDeploymentFeedbackLoop`
- `AgentLearningLoop`
- `OntologyUpdateLoop`
- `SourceTrustLoop`
- `OSBuildLoop`
- `OSBootInstallLoop`
- `OSRollbackLoop`
- `FleetComplianceLoop`
- `LocalFirstMeshLoop`
- `PlatformGovernanceLoop`

## Public-sector innovation case-study handling

Public-sector, defense, and national-security innovation programs MAY be represented when they provide useful evidence about institutional learning, high-risk technology development, challenge-driven R&D, capability transition, or governance feedback loops.

These records MUST be neutral, sourced, and bounded. They MUST NOT be presented as endorsement, tasking, operational guidance, or unsourced strategic analysis.

Required extra fields:

```yaml
jurisdiction: country, alliance, or public body
program_type: research_agency | accelerator | venture_fund | lab | procurement_bridge | industrial_policy | operational_feedback_platform | other
civil_military_status: civilian | defense | dual_use | public_sector | unknown
public_sources_only: true
```

## Agent-use boundary

Agents may use this standard to:

- classify institutions and learning loops;
- extract platform primitives;
- propose ontology updates;
- generate curriculum;
- improve MLOps lifecycle design;
- identify evidence gaps.

Agents MUST NOT transform case studies into unsupported operational claims, procurement advice, targeting advice, or hidden tasking.

## Integration requirements

A repository is integrated with this standard only if it contains:

1. a local alignment document;
2. a reference to this standard;
3. at least one schema, ontology, example, or adapter using the standard;
4. a validation or review path owned by Sociosphere, Delivery Excellence, or a standards repo.

## Relationship to model serving

For MLOps serving loops, Ray Serve and KubeRay are the preferred primary serving substrate. Clipper is legacy-reference only and MUST NOT be treated as the active default model-serving architecture.
