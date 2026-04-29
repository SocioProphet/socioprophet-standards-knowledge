# Foundational Training Cycle Standard v1

Status: draft
Owner: SocioProphet standards knowledge
Depends on:
- `standards/learning-loop-standard.v1.md`
- `standards/model-serving-loop-standard.v1.md`
- SocioProphet/socioprophet-standards-storage: `standards/evidence-bundle-standard.v1.md`
- SocioProphet/sociosphere: `standards/angel-of-the-lord/README.md`

## Purpose

This standard defines how SocioProphet reinforces systems-learning programs with foundational training cycles. It connects institutional learning loops, MLOps, Alexandrian Academy curriculum, Michael-agent learning, Prophet Platform primitives, and SourceOS lifecycle work to repeatable training methods.

The standard encodes:

```text
Foundational principle -> worked example -> trial/experiment -> feedback -> reinforcement -> transfer -> evidence -> Angel epoch review -> curriculum/platform/model/ontology update
```

## Core doctrine

Every major program case study, ontology update, model lifecycle, OS lifecycle, or agent-learning artifact SHOULD be reinforced by a training cycle that teaches:

1. the underlying principle;
2. a minimal worked example;
3. a trial or experiment;
4. feedback/evaluation signals;
5. reinforcement or repetition path;
6. transfer path to adjacent domains;
7. evidence bundle and review state;
8. Angel of the Lord epoch grading;
9. update path into curriculum, platform, model, or ontology.

## Required object: FoundationalTrainingCycle

```yaml
id: stable identifier
name: human readable name
training_domain: cybernetics | institutional_learning | mlops | model_serving | ontology | sourceos_lifecycle | agent_learning | platform_governance | other
learning_loop_ref: LearningLoop reference
principles: list of foundational principles
techniques: list of techniques
worked_examples: list of example references
trial_protocol: TrialProtocol reference
feedback_signals: list of FeedbackSignal references
reinforcement_plan: ReinforcementPlan reference
transfer_plan: TransferPlan reference
evidence_bundle_ref: EvidenceBundle reference
angel_epoch_grade_ref: AngelEpochGrade reference
curriculum_refs: Alexandrian Academy module references
platform_refs: Prophet Platform or implementation references
assessment_refs: tests, exercises, evaluations, or review gates
status: draft | active | validated | deprecated
last_reviewed: ISO-8601 date
```

## Required object: TrialProtocol

```yaml
id: stable identifier
question: what is being tested or learned
hypothesis: expected learning or capability outcome
setup: environment, dataset, simulator, repo, notebook, pipeline, or OS lifecycle context
inputs: required inputs
procedure: stepwise procedure
success_criteria: measurable criteria
failure_modes: expected ways the trial can fail
safety_bounds: constraints, permissions, and exclusions
outputs: expected artifacts
evidence_required: EvidenceArtifact references or requirements
```

## Required object: ReinforcementPlan

```yaml
id: stable identifier
skill_or_principle: what is reinforced
repetition_schedule: one-shot | spaced | milestone | continuous | triggered_by_feedback
feedback_basis: metrics, tests, reviews, human feedback, operational telemetry, or agent critique
reward_signal: explicit or implicit reinforcement signal, if applicable
correction_path: what happens when performance degrades
retention_check: how durability of learning is evaluated
```

## Required object: TransferPlan

```yaml
id: stable identifier
source_context: where the principle is first learned
target_contexts: where the principle should transfer
invariants: what must remain true across contexts
adaptations: what may change across contexts
evaluation: how transfer is tested
evidence_required: EvidenceArtifact references or requirements
```

## Required object: AngelEpochGrade

Michael-agent and other education-bearing agents MUST be graded at each epoch using the Sociosphere Angel of the Lord Hardening Regime as the adversarial critique and evidence gate.

```yaml
id: stable identifier
agent_id: michael_agent | socioprophet_agent | prophet_platform_agent | sourceos_agent | atlas_agent | mlops_agent | other
epoch_id: stable epoch identifier
review_regime_ref: SocioProphet/sociosphere:standards/angel-of-the-lord/README.md
surfaces_reviewed: learning objectives, evidence bundles, code outputs, repo changes, model artifacts, ontology updates, curriculum claims, platform claims
angel_lanes: source_exposure | ci_permissions | repo_boundary | dependency_vulnerability | runtime_policy | telemetry_publication | release_mirror | adversarial_review
findings_by_severity:
  blocker: list
  high: list
  medium: list
  low: list
  info: list
evidence_accepted: list of EvidenceArtifact references
evidence_missing: list of missing evidence items
trust_boundaries_found: list
trust_boundaries_missing: list
publication_or_transition_decision: pass | pass_with_findings | remediation_required | blocked | restricted_handling
remediation_backlog: list of remediation records
review_state: draft | reviewed | accepted | rejected | blocked
reviewed_at: ISO-8601 datetime
```

## Angel epoch grading rule

A training cycle cannot be marked `validated` unless the corresponding epoch has an AngelEpochGrade with no unresolved `blocker` findings and no unresolved `high` findings that materially affect the claimed capability.

If Angel grading returns `remediation_required`, the learning objective remains incomplete until remediation evidence is produced and reviewed.

If Angel grading returns `blocked`, the learning objective, transition gate, publication, deployment, or claim MUST be blocked or restricted according to Sociosphere source-exposure and hardening policy.

## Technique taxonomy

Canonical technique terms for v1:

- `WorkedExampleLearning`
- `TrialBasedLearning`
- `ExperimentDrivenLearning`
- `ReinforcementLearning`
- `HumanFeedbackReinforcement`
- `AgentCritiqueReinforcement`
- `TransferLearning`
- `CurriculumLearning`
- `RetrievalAugmentedLearning`
- `CaseBasedReasoning`
- `OntologyGuidedLearning`
- `SimulationBasedLearning`
- `OperationalFeedbackLearning`
- `SpacedReview`
- `EvidenceBasedReview`
- `ModelEvaluationLoop`
- `PolicyEvaluationLoop`
- `AngelEpochReview`

## Program case-study reinforcement

Every public-sector innovation or institutional learning case study SHOULD include a training-cycle adapter that extracts transferable principles without making unsupported operational claims.

Example mapping:

```text
NATO DIANA -> challenge-driven innovation training cycle
BRAVE1 -> operational feedback and rapid transition training cycle
NATO Innovation Fund -> portfolio learning and venture signal training cycle
EDF/EUDIS/HEDI -> collaborative R&D governance training cycle
DIU/AFWERX/ASCA/iDEX/IDEaS -> commercial transition training cycle
MAFAT/DSO/ADD/ATLA -> lab-to-field transition training cycle
```

## MLOps reinforcement

MLOps repositories MUST map training cycles into:

```text
dataset -> experiment -> model -> evaluation -> deployment -> feedback -> retraining or rollback
```

For model serving, Ray Serve and KubeRay are the preferred primary serving substrates. Clipper-era lessons may be used only as historical training examples for prediction-serving concepts and must be marked `legacy_reference`.

## Alexandrian Academy integration

Alexandrian Academy SHOULD consume this standard to produce modules with:

1. principle explanation;
2. worked example;
3. trial exercise;
4. reinforcement exercise;
5. transfer exercise;
6. evidence and reflection artifact;
7. Angel epoch review;
8. assessment rubric.

## Non-hand-waving acceptance criteria

A training cycle is accepted only if it has:

1. explicit principles;
2. at least one worked example;
3. a trial protocol;
4. feedback signals;
5. reinforcement plan;
6. transfer plan;
7. evidence bundle;
8. AngelEpochGrade;
9. assessment or review gate.
