# Evaluation Fabric Standard v1

Status: draft
Owner: SocioProphet standards knowledge
Depends on:
- `standards/learning-loop-standard.v1.md`
- `standards/foundational-training-cycle-standard.v1.md`
- `standards/agent-education-equivalence-standard.v1.md`
- `standards/model-serving-loop-standard.v1.md`
- SocioProphet/socioprophet-standards-storage: `standards/evidence-bundle-standard.v1.md`
- SocioProphet/socioprophet-standards-storage: `standards/open-courseware-corpus-standard.v1.md`
- SocioProphet/sociosphere: `standards/angel-of-the-lord/README.md`

## Purpose

This standard defines a common evaluation fabric for people, machines, agents, models, curricula, ontologies, SourceOS/SociOS lifecycle systems, Atlas orchestration, and Prophet Platform capabilities.

The evaluation fabric exists to prevent hand-wavy claims of learning, mastery, deployment readiness, model quality, platform readiness, curriculum completion, or operational correctness. It aligns human education assessment, machine evaluation, agent epoch grading, model evaluation, OS lifecycle proof, and platform transition gates under one evidence-bound framework.

## Core thesis

Evaluation is not a final test. Evaluation is a continuous fabric:

```text
objective -> task -> evidence -> metric/rubric -> adversarial review -> remediation -> transfer -> regression check -> certification of state
```

The same fabric must support:

- human learning and course-equivalent assessment;
- Michael-agent education epochs;
- agent capability growth and transfer;
- model training, evaluation, serving, feedback, and retraining;
- OS build, boot, install, update, rollback, and fleet compliance;
- ontology correctness and knowledge graph quality;
- platform capability transition and release readiness;
- curriculum quality in Alexandrian Academy;
- Sociosphere Angel of the Lord critique.

## Required object: EvaluationFabric

```yaml
id: stable identifier
name: human readable name
scope: human | agent | model | mlops | os_lifecycle | ontology | curriculum | platform | atlas | mixed
owner: repo, team, academy, agent, or governance owner
standards_refs: list of standards consumed
evaluation_tracks: list of EvaluationTrack references
evidence_requirements: list of EvidenceRequirement references
governance_gate_refs: Sociosphere, Delivery Excellence, standards, or human review gates
status: draft | active | validated | deprecated
last_reviewed: ISO-8601 date
```

## Required object: EvaluationTrack

```yaml
id: stable identifier
name: human readable name
evaluated_subject_type: human | agent | model | service | pipeline | os_release | boot_release | ontology | curriculum | platform_capability | atlas_bundle | other
evaluated_subject_ref: person, agent, model, repo, service, release, course, ontology, or capability reference
evaluation_level: diagnostic | formative | summative | adversarial | certification | regression | transfer | continuous
objectives: list of LearningObjective or CapabilityObjective references
tasks: list of EvaluationTask references
prior_required_tasks: tasks from previous accepted epochs that must remain non-regressed
rubrics: list of Rubric references
metrics: list of Metric references
monotonicity_policy: MonotonicProgressPolicy reference
evidence_bundle_ref: EvidenceBundle reference
angel_epoch_grade_ref: AngelEpochGrade reference, when applicable
result: pass | pass_with_findings | remediation_required | fail | blocked | restricted_handling | unknown
```

## Required object: EvaluationTask

```yaml
id: stable identifier
task_type: exam | test | quiz | problem_set | lab | project | code_review | oral_defense | benchmark | simulation | red_team | adversarial_review | model_eval | service_eval | ontology_eval | os_lifecycle_eval | transfer_task | regression_task | other
prompt_or_spec_ref: source, course material, benchmark, schema, issue, contract, or task specification
inputs: datasets, artifacts, repos, models, environments, course materials, or release refs
allowed_resources: open_book | closed_book_simulated | timed | tool_allowed | no_tool | sandboxed | restricted | custom
success_criteria: measurable or rubric criteria
failure_modes: expected or known failure classes
outputs_required: EvidenceArtifact types
review_required: human | agent | Angel | standards | Delivery Excellence | Sociosphere | CI | none
```

## Required object: Rubric

```yaml
id: stable identifier
name: human readable name
rubric_type: human_learning | agent_learning | model_quality | systems_reliability | security | ontology_quality | curriculum_quality | platform_readiness | os_lifecycle | other
criteria:
  - criterion_id: stable identifier
    description: what is judged
    scale: pass_fail | numeric | ordinal | severity | qualitative
    minimum_acceptance: threshold or rule
    evidence_required: EvidenceArtifact requirements
```

## Required object: Metric

```yaml
id: stable identifier
name: metric name
metric_type: accuracy | precision | recall | f1 | latency | throughput | cost | reliability | safety | security | coverage | reproducibility | calibration | drift | human_mastery | transfer_success | ontology_consistency | regression_delta | other
definition: precise definition
measurement_method: how it is measured
thresholds: pass, warning, fail, or severity thresholds
known_limitations: caveats
```

## Required object: MonotonicProgressPolicy

Every epoch-bearing subject must define a monotonic progress policy. This policy protects against hidden regression in stochastic systems, agents, models, curricula, and platform capabilities.

```yaml
id: stable identifier
subject_ref: evaluated subject
baseline_epoch_ref: previous accepted epoch
prior_exam_policy: rerun_all_prior | sampled_prior_suite | risk_weighted_prior_suite | waiver_required
minimum_grade_retention: same_grade | no_material_regression | custom_threshold
allowed_delta:
  numeric_absolute: optional maximum absolute drop
  numeric_relative: optional maximum relative drop
  rubric_band_drop: none | one_minor_band | custom
  stochastic_confidence: confidence interval or repeated-run policy
stochastic_repeats: number of repeated runs for stochastic models or agents
aggregation_method: mean | median | worst_case | confidence_bound | custom
block_on_regression: true
remediation_required_on_regression: true
waiver_policy: explicit standards or Sociosphere waiver only
```

## Required object: EpochRegressionCheck

```yaml
id: stable identifier
subject_ref: evaluated subject
current_epoch_ref: current epoch
baseline_epoch_ref: prior accepted epoch
prior_tasks_evaluated: list of prior EvaluationTask refs
current_results: EvaluationRecord refs
baseline_results: EvaluationRecord refs
deltas: metric and rubric deltas
stochastic_adjustment: repeated-run or confidence-bound notes
regressions_found: list
result: no_regression | within_allowed_delta | remediation_required | blocked
remediation_refs: RemediationRecord refs
```

## Required object: EvidenceRequirement

```yaml
id: stable identifier
artifact_type: source_record | assessment_attempt | model_eval | dataset_card | model_card | deployment_manifest | build_manifest | test_log | transcript | ontology_diff | review_report | angel_epoch_grade | epoch_regression_check | other
required_for: human | agent | model | os_lifecycle | ontology | curriculum | platform | atlas | mixed
minimum_fields: required fields or schema refs
retention_policy: ephemeral | retained | append_only | restricted | public_safe
```

## Monotonic epoch rule

For Michael-agent and other epoch-bearing agents, the agent must maintain the same accepted grade in all prior exams, tests, projects, rubrics, and transfer evaluations unless a standards-approved tolerance explicitly allows a small stochastic delta.

Forward progress is blocked when:

1. a prior accepted exam/test/project falls below its accepted grade outside the allowed delta;
2. a prior transfer task fails in the new epoch;
3. a stochastic model regresses beyond its confidence-bound tolerance;
4. an Angel grade identifies regression as material;
5. the epoch omits required prior-regression checks.

This rule applies to humans where appropriate, to agents by default, and to models/systems whenever regression can create false progress claims.

## Evaluation lanes

The v1 fabric defines these canonical lanes:

### Human education lane

For people or human-equivalent training tracks:

```text
course objective -> assignment/test/exam/lab/project -> rubric -> evidence -> review -> remediation or completion
```

### Michael-agent education lane

For Michael-agent degree-equivalent education:

```text
public courseware corpus -> published test/exam/project -> assessment attempt -> evidence bundle -> Angel epoch grade -> prior exam regression check -> transfer task -> accepted/remediated epoch
```

### Agent capability lane

For agents generally:

```text
capability objective -> task battery -> adversarial critique -> transfer evaluation -> memory/capability update -> regression check
```

### MLOps/model lane

For ML systems:

```text
dataset -> experiment -> model -> evaluation -> deployment -> observability -> feedback -> retraining/rollback -> regression check
```

Ray Serve and KubeRay are the primary serving default for new serving-loop work. Clipper is legacy-reference only.

### OS/fleet lifecycle lane

For SourceOS/SociOS:

```text
build -> boot -> install -> update -> rollback -> device/fleet fingerprint -> compliance evaluation -> regression check -> evidence -> Angel review
```

### Ontology/knowledge lane

For knowledge systems:

```text
source -> extraction -> entity/relationship proposal -> ontology diff -> SHACL/validation -> review -> graph update -> query regression
```

### Platform transition lane

For Prophet Platform and Atlas:

```text
learning-loop insight -> platform primitive -> contract -> implementation -> evidence -> transition gate -> regression check -> release or remediation
```

## Angel of the Lord integration

The Angel of the Lord is the adversarial review authority for high-consequence epochs. Any evaluation track involving agent education, platform transition, public-source case studies, model serving, OS lifecycle, source exposure, or release readiness MUST include an Angel grade or an explicit waiver.

An evaluation cannot be marked complete if the Angel grade has unresolved blocker findings or unresolved material high findings.

Angel grading must inspect whether prior accepted grades and capabilities are preserved. Material hidden regression is a high or blocker finding depending on impact.

## Machine and human parity

The fabric must treat humans and machines consistently where possible:

- humans and agents can both attempt tests, projects, labs, and transfer tasks;
- models can be evaluated by benchmarks, telemetry, and task-specific metrics;
- OS/fleet systems can be evaluated by lifecycle proofs and compliance records;
- ontologies can be evaluated by consistency, coverage, provenance, query behavior, and review;
- all claims require evidence bundles.

Human-only credentials and institutional statuses must remain human/institutional facts. Agent education may be degree-equivalent only when evidence supports equivalence; it must not claim enrollment, credit, degree, or institutional endorsement.

## Acceptance rule

A capability, epoch, course-equivalent module, model deployment, release, ontology update, or platform primitive is accepted only when:

1. objectives are explicit;
2. tasks are defined;
3. rubrics or metrics are defined;
4. evidence is stored;
5. review gate is identified;
6. remediation path exists;
7. transfer or regression is evaluated where relevant;
8. prior accepted exams, tests, projects, and transfer tasks remain non-regressed within the monotonic progress policy;
9. Angel grading is applied where required.

## Non-hand-waving rule

A repo claiming compliance with this standard must include:

- a local evaluation-fabric alignment document;
- at least one example evaluation record;
- evidence bundle references;
- validation or review gate references;
- monotonic progress or regression policy where epochs exist;
- integration with Sociosphere or Delivery Excellence where release or transition is affected.
