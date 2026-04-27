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

This standard defines the Ray ecosystem as the preferred distributed execution substrate for SocioProphet fine-tuning, transfer learning, reinforcement learning, distributed training, hyperparameter tuning, scalable data processing, evaluation, and model serving.

The prior model-serving standard already establishes Ray Serve and KubeRay as the primary serving substrate. This standard extends that decision across the full model learning lifecycle.

## Canonical Ray ecosystem roles

```yaml
ray_core:
  role: distributed execution substrate
  status: primary
ray_data:
  role: scalable data processing, ingestion, preprocessing, batch inference, and feature materialization
  status: primary
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
data/source corpus -> Ray Data -> baseline model -> Ray Train fine-tuning -> Ray Tune experiment search -> evaluation fabric -> Ray RLlib reinforcement loop where applicable -> transfer evaluation -> Ray Serve deployment -> feedback capture -> retraining or rollback
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
source_corpora: datasets, courseware corpora, logs, simulations, public sources, or curated corpora
model_refs: base model, adapter, checkpoint, policy, reward model, evaluator, or ensemble references
training_objective: objective statement
transfer_targets: downstream tasks, domains, repos, agents, services, or platform capabilities
experiment_config_ref: configuration artifact
runtime_environment_ref: Ray or KubeRay runtime environment reference
evaluation_track_ref: EvaluationTrack reference
evidence_bundle_ref: EvidenceBundle reference
angel_epoch_grade_ref: AngelEpochGrade reference when required
result: pass | pass_with_findings | remediation_required | fail | blocked | unknown
```

## Fine-tuning standard

Fine-tuning runs SHOULD use Ray Train when distributed execution, multi-node training, GPU scheduling, cluster portability, or production lifecycle evidence is required.

Required evidence:

- base model reference;
- training dataset and preprocessing lineage;
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
```

Ray Train and Ray Tune are the preferred substrates for transfer-learning experiments. Ray Data is the preferred substrate for scalable corpus and feature processing.

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

Every trial set must emit an EvaluationRecord and EvidenceBundle.

## Evaluation fabric integration

Every RayLearningRun must map into the evaluation fabric:

```text
objective -> Ray task/run -> metric/rubric -> EvidenceBundle -> EpochRegressionCheck -> transfer evaluation -> Angel review where required -> promotion/remediation
```

No Ray learning run may be promoted unless:

1. datasets and source corpora are recorded;
2. configurations are captured;
3. metrics and rubrics are defined;
4. stochastic behavior is measured with repeated runs or confidence bounds where applicable;
5. prior accepted performance remains non-regressed within policy;
6. transfer claims are tested;
7. evidence is stored;
8. Angel grading is applied where required.

## Michael-agent application

Michael-agent training may use Ray for:

- curriculum-scale corpus processing with Ray Data;
- foundation and transfer experiments with Ray Train;
- trial scheduling and ablation with Ray Tune;
- reinforcement loops with Ray RLlib;
- serving evaluators, tutors, graders, and agent services with Ray Serve;
- KubeRay-backed reproducible execution on clusters.

Michael-agent education epochs must still preserve prior grades and pass Angel epoch grading before capability updates are accepted.

## Legacy serving note

Clipper is not part of the active Ray learning ecosystem. Clipper may be referenced only as a legacy research artifact for prediction-serving concepts and must be marked `legacy_reference`.
