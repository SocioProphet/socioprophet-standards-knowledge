# Ray Learning Ecosystem Standard v1

Status: draft
Owner: SocioProphet standards knowledge
Depends on:
- `standards/learning-loop-standard.v1.md`
- `standards/evaluation-fabric-standard.v1.md`
- `standards/model-serving-loop-standard.v1.md`
- SocioProphet/socioprophet-standards-storage: `standards/evidence-bundle-standard.v1.md`
- SocioProphet/socioprophet-standards-storage: `standards/evaluation-record-standard.v1.md`
- SocioProphet/sociosphere: `standards/angel-of-the-lord/README.md`

## Purpose

This standard defines the Ray ecosystem as the preferred distributed execution substrate for SocioProphet fine-tuning, transfer learning, reinforcement learning, distributed training, hyperparameter tuning, evaluation, and model serving.

Apache Beam is the preferred canonical substrate for durable, portable, production-grade data processing pipelines unless there is a clear reason not to use it. Ray Data may be used for Ray-local and in-memory training/serving data paths, but it should interoperate with Beam or consume Beam-produced datasets where persistent, portable, cross-run lineage is required.

The prior model-serving standard already establishes Ray Serve and KubeRay as the primary serving substrate. This standard extends Ray across the model learning lifecycle while preserving Beam-first data pipeline governance.

## Canonical ecosystem roles

```yaml
apache_beam:
  role: canonical portable data processing, durable ETL, corpus preparation, streaming/batch pipeline governance, and cross-run data lineage
  status: primary_data_pipeline
ray_core:
  role: distributed execution substrate for Ray-native training, tuning, RL, evaluation, and serving work
  status: primary
ray_data:
  role: Ray-local data loading, in-memory preprocessing, batch inference, feature materialization near training/serving, and Beam-interoperable adapter paths
  status: ray_local_adapter
ray_train:
  role: distributed model training and fine-tuning orchestration
  status: primary
ray_tune:
  role: hyperparameter optimization, experiment search, ablation studies, and trial management
  status: primary
ray_rllib:
  role: reinforcement learning training, simulation-loop integration, policy evaluation, and multi-agent RL
  status: primary
ray_serve:
  role: online inference, model application graphs, service composition, and production serving
  status: primary
kuberay:
  role: Kubernetes-native Ray cluster lifecycle, RayJob, RayService, and production cluster management
  status: primary
```

## Canonical lifecycle

```text
data/source corpus -> Apache Beam durable pipeline -> versioned dataset/features -> Ray Data adapter when needed -> baseline model -> Ray Train fine-tuning -> Ray Tune experiment search -> evaluation fabric -> Ray RLlib reinforcement loop where applicable -> transfer evaluation -> Ray Serve deployment -> feedback capture -> Beam/Ray retraining data path -> retraining or rollback
```

## Required object: RayLearningRun

```yaml
id: stable identifier
run_type: pretraining | fine_tuning | transfer_learning | reinforcement_learning | evaluation | serving | mixed
ray_components:
  - ray_core
  - ray_data
  - ray_train
  - ray_tune
  - ray_rllib
  - ray_serve
  - kuberay
data_pipeline_components:
  - apache_beam
source_corpora: datasets, courseware corpora, logs, simulations, public sources, or curated corpora
beam_pipeline_refs: Beam pipeline, transform, runner, or output dataset references where applicable
ray_data_refs: Ray Data dataset, adapter, or in-memory processing references where applicable
model_refs: base model, adapter, checkpoint, policy, reward model, evaluator, or ensemble references
training_objective: objective statement
transfer_targets: downstream tasks, domains, repos, agents, services, or platform capabilities
experiment_config_ref: configuration artifact
runtime_environment_ref: Ray, KubeRay, Beam runner, or mixed runtime environment reference
evaluation_track_ref: EvaluationTrack reference
evidence_bundle_ref: EvidenceBundle reference
angel_epoch_grade_ref: AngelEpochGrade reference when required
result: pass | pass_with_findings | remediation_required | fail | blocked | unknown
```

## Beam-first data processing rule

Beam is the default for:

- durable ETL;
- public-courseware and corpus capture pipelines;
- batch and streaming ingestion;
- data normalization and enrichment;
- feature preparation requiring lineage;
- multi-run reproducibility;
- portability across runners;
- production dataflow governance;
- dataset versioning and audit evidence.

Ray Data is appropriate when:

- the data path is tightly coupled to Ray Train, Ray Tune, Ray RLlib, or Ray Serve;
- in-memory or near-training preprocessing is materially simpler;
- batch inference is being executed inside a Ray cluster;
- the source dataset was already produced and versioned by Beam or another governed pipeline;
- an explicit justification is recorded for not using Beam.

If Ray Data is used as the durable source-of-truth pipeline, the run MUST include a `beam_exception_reason` and evidence that lineage, replayability, and portability requirements are still satisfied.

## Required object: DataPipelineDecision

```yaml
id: stable identifier
run_ref: RayLearningRun or pipeline reference
canonical_pipeline: apache_beam | ray_data | mixed | other
beam_pipeline_ref: reference when Beam is used
ray_data_ref: reference when Ray Data is used
beam_exception_reason: required when Beam is not used for durable corpus/data processing
lineage_evidence_ref: EvidenceBundle reference
replayability_evidence_ref: EvidenceBundle reference
portability_evidence_ref: EvidenceBundle reference
accepted_by: standards, MLOps, Angel, or platform review role
```

## Fine-tuning standard

Fine-tuning runs SHOULD use Ray Train when distributed execution, multi-node training, GPU scheduling, cluster portability, or production lifecycle evidence is required.

Required evidence:

- base model reference;
- training dataset and preprocessing lineage;
- Beam pipeline reference for durable data preparation or documented Beam exception;
- Ray Data adapter reference where used;
- training configuration;
- checkpoint references;
- evaluation metrics;
- regression check against prior accepted models;
- transfer evaluation where the fine-tuned model claims broader utility;
- rollback or demotion path.

## Transfer learning standard

Transfer learning runs MUST record:

```yaml
source_domain: where the representation or model is learned
target_domain: where it is applied
frozen_or_trainable_components: encoder, head, adapter, LoRA, policy, retriever, reranker, etc.
transfer_hypothesis: why transfer should work
invariants: what should remain stable across domains
adaptations: what changes in target domain
evaluation: target task metrics and transfer task evidence
regression_check: whether source-domain performance is preserved within tolerance
data_pipeline_decision: DataPipelineDecision reference
```

Ray Train and Ray Tune are the preferred substrates for transfer-learning experiments. Beam is the preferred substrate for scalable corpus and feature processing. Ray Data is a Ray-local adapter unless explicitly justified otherwise.

## Reinforcement learning standard

Reinforcement learning runs SHOULD use Ray RLlib where simulation, policy optimization, multi-agent environments, offline RL, online RL, or feedback-loop training is required.

Required evidence:

- environment specification;
- policy/model reference;
- observation and action spaces;
- reward function or preference signal;
- safety bounds;
- exploration policy;
- evaluation policy;
- Beam pipeline references for offline RL datasets or replay buffers where persistent lineage is required;
- baseline comparison;
- stochastic repeated-run evidence;
- regression check against prior accepted policies;
- Angel review where agent behavior, platform policy, or public/release claims are affected.

## Ray Tune and trial discipline

Ray Tune or equivalent trial-management infrastructure SHOULD be used for:

- hyperparameter search;
- ablation studies;
- architecture comparisons;
- fine-tuning strategy comparison;
- RL algorithm comparison;
- stochastic repeat scheduling;
- early stopping and promotion decisions.

Every trial set must emit an EvaluationRecord and EvidenceBundle. Trial datasets must trace back to Beam-governed data pipelines unless a Beam exception is recorded.

## Evaluation fabric integration

Every RayLearningRun must map into the evaluation fabric:

```text
objective -> Beam data pipeline or documented exception -> Ray task/run -> metric/rubric -> EvidenceBundle -> EpochRegressionCheck -> transfer evaluation -> Angel review where required -> promotion/remediation
```

No Ray learning run may be promoted unless:

1. datasets and source corpora are recorded;
2. Beam pipeline or DataPipelineDecision evidence exists;
3. configurations are captured;
4. metrics and rubrics are defined;
5. stochastic behavior is measured with repeated runs or confidence bounds where applicable;
6. prior accepted performance remains non-regressed within policy;
7. transfer claims are tested;
8. evidence is stored;
9. Angel grading is applied where required.

## Michael-agent application

Michael-agent training may use Ray for:

- Ray Train foundation and transfer experiments;
- Ray Tune trial scheduling and ablation;
- Ray RLlib reinforcement loops;
- Ray Serve evaluators, tutors, graders, and agent services;
- KubeRay-backed reproducible execution on clusters.

Michael-agent data and curriculum-scale corpus processing should default to Beam for durable capture, enrichment, and replayable lineage. Ray Data may consume Beam outputs for near-training or near-serving processing.

Michael-agent education epochs must still preserve prior grades and pass Angel epoch grading before capability updates are accepted.

## Legacy serving note

Clipper is not part of the active Ray learning ecosystem. Clipper may be referenced only as a legacy research artifact for prediction-serving concepts and must be marked `legacy_reference`.
