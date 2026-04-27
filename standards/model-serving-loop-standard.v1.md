# Model Serving Learning Loop Standard v1

Status: draft
Owner: SocioProphet standards knowledge
Scope: online inference, model-serving feedback loops, runtime classification, observability, rollback, and evidence requirements for SocioProphet MLOps and Prophet Platform.

## Purpose

This standard defines how SocioProphet represents model-serving systems as learning loops. It corrects legacy assumptions around Clipper and establishes Ray Serve plus KubeRay as the preferred primary serving substrate for new work.

## Runtime status policy

Every serving runtime referenced by SocioProphet MUST be assigned a runtime status.

```yaml
runtime_status: primary | supported | specialized | experimental | legacy_reference | deprecated
```

Canonical v1 runtime classification:

```yaml
ray_serve:
  runtime_status: primary
  role: default Python-native online inference and application-graph serving runtime
kuberay:
  runtime_status: primary
  role: Kubernetes operator/control plane for Ray clusters and Ray Serve production deployment
kserve:
  runtime_status: supported
  role: Kubernetes-native model serving and inference service abstraction
seldon:
  runtime_status: supported
  role: Kubernetes-native serving, experimentation, and inference graph compatibility lane
triton:
  runtime_status: specialized
  role: high-performance GPU inference, especially NVIDIA-optimized workloads
bentoml:
  runtime_status: supported
  role: packaging and deployment lane for model services
mlflow:
  runtime_status: supported
  role: experiment/model registry and serving compatibility lane
torchserve:
  runtime_status: supported
  role: PyTorch-specific serving compatibility lane
tensorflow_serving:
  runtime_status: supported
  role: TensorFlow-specific serving compatibility lane
clipper:
  runtime_status: legacy_reference
  role: historical research artifact for prediction serving concepts; not an active default
```

## Required object: ModelServingDeployment

```yaml
id: stable identifier
name: deployment name
runtime: ray_serve | kuberay | kserve | seldon | triton | bentoml | mlflow | torchserve | tensorflow_serving | legacy_clipper | other
runtime_status: primary | supported | specialized | experimental | legacy_reference | deprecated
models: list of model references
model_registry_refs: list of registry references, if any
serving_graph: DAG or composition reference
endpoint_refs: endpoint or route references
resource_requirements: CPU, memory, GPU, accelerator, node, or cluster requirements
autoscaling_policy: scaling rules
batching_policy: batching and queueing rules
routing_policy: traffic split, canary, shadow, A/B, or bandit policy
observability_policy: metrics, logs, traces, health checks
feedback_capture_policy: what feedback is captured and how
evidence_bundle_ref: EvidenceBundle reference
rollback_policy: rollback or demotion path
owner: repo, team, or agent steward
```

## Required object: ModelServingFeedbackLoop

```yaml
id: stable identifier
deployment_ref: ModelServingDeployment reference
input_signal: request telemetry, user feedback, evaluator signal, operational incident, drift signal, cost signal, or latency signal
measurement_window: time or event window
metrics: latency, throughput, error rate, cost, quality, safety, drift, bias, robustness, or task-specific metrics
feedback_artifacts: EvidenceArtifact references
transition_gate: continue | rollback | retrain | reconfigure | scale | deprecate | investigate
next_action: human or agent action recommendation
confidence_rating: high | medium | low | contested | unknown
```

## Required evidence

A model-serving deployment is not accepted unless it has:

1. model lineage;
2. dataset or training lineage where available;
3. evaluation evidence;
4. deployment manifest;
5. runtime classification;
6. observability policy;
7. feedback capture policy;
8. rollback policy;
9. evidence bundle reference.

## Ray Serve default guidance

New SocioProphet serving-loop work SHOULD default to Ray Serve and KubeRay when requirements include:

- Python-native model/application composition;
- multi-model serving graphs;
- autoscaling online inference;
- batch or dynamic request handling;
- Kubernetes deployment;
- local-to-cluster parity;
- integration with agentic orchestration;
- LLM, embedding, reranking, or multi-stage inference services.

## Clipper legacy handling

Clipper-era material may be retained only as a historical reference for concepts such as low-latency prediction serving, adaptive batching, model selection, and feedback-aware serving.

Any Clipper reference MUST include:

```yaml
runtime_status: legacy_reference
active_default: false
migration_target: ray_serve | kuberay | kserve | triton | other
```

No new SocioProphet implementation should select Clipper as the active default serving runtime.

## Relationship to Learning Loop Standard

A serving deployment is a `ModelDeploymentFeedbackLoop` under the Learning Loop Knowledge Standard. It consumes evidence from storage standards and emits feedback signals that may trigger retraining, runtime reconfiguration, rollback, ontology updates, or platform capability updates.
