# 044 — Agent Sandbox Lifecycle (v0.1 draft)

## Status

**Draft.** This document defines the canonical Capability Fabric lifecycle semantics for creating, admitting, materializing, executing, validating, and closing agent sandboxes.

This document is normative. It uses RFC-style language:
- **MUST / MUST NOT** = mandatory for compliance
- **SHOULD / SHOULD NOT** = strongly recommended
- **MAY** = optional

## Purpose

The Agent Sandbox Lifecycle standard defines the protocol-independent semantic objects and invariants required to run agentic work safely across CI systems, local workspaces, managed runners, or hosted control planes.

It exists to separate:
- sandbox meaning from transport encoding;
- admission policy from repository-specific workflow implementation;
- model/tool failures from successful work products;
- controlled execution from weakly controlled or externalized agent actions;
- receipts and attestations from informal log output.

## Relationship to Capability Fabric

This document extends the semantic core defined in `040-capability-fabric-core.md` and the realization-profile model defined in `041-capability-fabric-realization-profiles.md`.

An agent sandbox realization MUST declare:
- `FunctionIdentity` for the requested capability;
- `RealizationMetadata` for the selected runtime and runner;
- `DeliverySemantics` for the work unit;
- `ReceiptSemantics` for emitted outputs;
- `ExecutionControllabilityProfile` for the sandbox boundary;
- `ProofStrengthProfile` for any claims made by the run.

Transport-specific carriage of these objects belongs in realization profiles such as TriTRPC, MCP, A2A, or repository-local CI workflows. Transport profiles MUST NOT redefine the canonical meaning of the objects in this document.

## Lifecycle phases

### 1. Inception

Inception is the semantic admission phase for an agentic request.

An `InceptionRecord` MUST include:
- request identifier;
- actor identity reference;
- actor trust class;
- trigger source;
- requested capability reference;
- target repository or workspace reference;
- target branch / base / head references when applicable;
- normalized request body hash;
- duplicate-suppression decision;
- protected-path decision;
- initial controllability estimate;
- initial proof-strength ceiling;
- admission outcome.

Inception MUST treat repository text, issue comments, PR comments, review comments, and model-visible prompt material as untrusted data unless explicitly elevated by policy.

Inception SHOULD suppress duplicate request storms, including repeated identical agent-trigger comments from the same actor over the same target within a configured time window.

### 2. Genesis

Genesis is the sandbox materialization phase.

A `GenesisManifest` MUST include:
- sandbox identifier;
- parent `InceptionRecord` reference;
- runner / execution substrate reference;
- control-plane revision;
- workspace revision;
- tool policy reference;
- egress policy reference;
- credential policy reference;
- memory/session policy reference;
- execution budget reference;
- failure policy reference;
- receipt policy reference;
- materialization timestamp;
- manifest digest.

Genesis MUST separate trusted control-plane code from untrusted workspace content. If both are checked out in one runner, they MUST be placed in distinct paths and untrusted workspace content MUST NOT supply control-plane helper scripts.

Genesis MUST emit a receipt or attestation before analysis or execution begins.

### 3. Analyze

Analyze is the planning and read-only inspection phase.

The analyze phase MAY inspect source code, logs, CI output, comments, and repository metadata. It MUST NOT mutate the target branch or external systems unless the realization profile explicitly defines a read/write split and the write phase has not yet been reached.

Analyze SHOULD emit:
- analysis summary;
- proposed patch or patch reference;
- evidence references;
- failure classification if the phase cannot complete.

### 4. Validate

Validate is the deterministic reapplication and verification phase.

Validation MUST run from a clean workspace or clean materialized target state. It MUST verify that generated patches do not touch protected paths unless an explicit governance exception has been granted.

Validation SHOULD include repository-native checks, schema checks, fixture checks, action-pin checks, secret scanning, and policy checks appropriate to the repository.

### 5. Write

Write is the only phase allowed to mutate a repository branch, pull request branch, external artifact store, or durable workspace.

A write phase MUST require:
- successful validation;
- no head drift from the validated target unless explicitly reconciled;
- write credential minted or exposed only for this phase;
- protected-path approval if required;
- emitted write receipt;
- durable audit trail.

A write phase MUST NOT run untrusted repository build scripts after write credentials are available unless the realization profile explicitly proves isolation.

### 6. Shutdown

Shutdown closes the sandbox and emits final receipts.

Shutdown MUST revoke or allow expiry of credentials, close sessions, flush receipts, preserve required evidence, and classify final outcome.

Shutdown MUST NOT convert infrastructure, model, or tool failure into a successful write outcome.

## Failure policy

The following failures MUST be classified as infrastructure or control-plane failures unless a stronger repository-specific reason exists:
- model rate limit exhaustion;
- model unavailable;
- tool/MCP server unavailable;
- artifact-attestation verification failure;
- egress-policy denial;
- credential minting failure;
- runner bootstrap failure;
- cleanup callback failure.

For these failures:
- `allow_partial_push` MUST be false by default;
- `allow_push_after_infra_failure` MUST be false;
- the sandbox SHOULD emit a sealed failure bundle;
- the sandbox MAY emit retry guidance or checkpoint artifacts;
- the sandbox MUST NOT claim successful capability completion.

## Required semantic objects

### AgentSandboxSpec

`AgentSandboxSpec` captures the admitted request and the intended sandbox contract.

Required fields:
- `schema_version`
- `sandbox_id`
- `inception_ref`
- `target_ref`
- `capability_ref`
- `actor_ref`
- `trust_class`
- `execution_budget_ref`
- `failure_policy_ref`
- `memory_policy_ref`
- `receipt_policy_ref`

### AgentGenesisManifest

`AgentGenesisManifest` captures materialized sandbox state.

Required fields:
- `schema_version`
- `sandbox_id`
- `spec_ref`
- `control_plane_ref`
- `workspace_ref`
- `tool_policy_ref`
- `egress_policy_ref`
- `credential_policy_ref`
- `materialized_at`
- `manifest_digest`

### AgentFailureBundle

`AgentFailureBundle` captures classified failures without granting write authority.

Required fields:
- `schema_version`
- `sandbox_id`
- `failure_kind`
- `failure_class`
- `retry_after_seconds`
- `allow_partial_push`
- `allow_push_after_infra_failure`
- `evidence_refs`
- `sealed_at`

### AgentSandboxReceipt

`AgentSandboxReceipt` captures phase outcomes.

Required fields:
- `schema_version`
- `receipt_id`
- `sandbox_id`
- `phase`
- `outcome`
- `payload_digest`
- `signature_or_attestation_ref`
- `created_at`

## Controllability and proof strength

A sandbox MUST NOT claim proof strength stronger than its controllability class permits.

Recommended mapping:
- isolated local deterministic runner with pinned tools and attestations: `C3`, `INTRINSIC` or `ATTESTED_OBSERVATIONAL` depending evidence completeness;
- hosted ephemeral CI runner with pinned workflows and attestations: `C2`, `ATTESTED_OBSERVATIONAL`;
- hosted CI runner with broad network and live package installs: `C1`, `TRANSCRIPT_OBSERVATIONAL`;
- proprietary opaque coding-agent runtime: `C1` or `C0`, usually `TRANSCRIPT_OBSERVATIONAL` unless externally attested;
- human-in-the-loop manual patch application: `HUMAN`, `HUMAN_ATTESTED`.

## Cross-repository placement rule

Canonical lifecycle semantics belong in this standard.

Transport repositories, including TriTRPC, MAY define:
- wire carriage;
- typed blob profiles;
- digest/signature/reference binding;
- fixture and verifier behavior;
- deterministic serialization profiles.

Transport repositories MUST NOT redefine the semantic meaning of `AgentSandboxSpec`, `AgentGenesisManifest`, `AgentFailureBundle`, or `AgentSandboxReceipt`.

Runtime repositories MAY implement these semantics as concrete CI workflows, local runners, agent-plane jobs, or workspace controllers.

## Machine-readable companions

The canonical JSON Schema companion for this draft is:

- `schemas/jsonschema/capability-fabric/agent-sandbox-lifecycle.v0.schema.json`

## Change control

Changes that alter required fields, enum values, phase semantics, controllability rules, or failure-policy invariants MUST update the machine-readable companion schema in the same PR.
