# Immutable Image Substrate Standard v1

Status: draft
Owner: SocioProphet standards knowledge
Depends on:
- SocioProphet/prophet-platform: `docs/SOURCEOS_CONTROL_PLANE_CONTRACTS.md`
- SocioProphet/prophet-platform: `docs/CONTAINER_BUILD_SUBSTRATE.md`
- SocioProphet/socioprophet-standards-storage: `standards/evidence-bundle-standard.v1.md`
- SocioProphet/sociosphere: `standards/angel-of-the-lord/README.md`

## Purpose

This standard defines the immutable image substrate taxonomy for SourceOS, Prophet Platform, desktop/server hosts, service containers, Beam/Ray workloads, and agent/user spaces.

The goal is to avoid bloat by assigning each image family a narrow role and preventing desktop environments, development toolchains, model tooling, browsers, and agent experiments from leaking into the immutable system plane.

## Core doctrine

```text
immutable system image = host substrate and integration surface
Nix closure = user/agent environment and tool composition
service image = minimal OCI runtime artifact
ReleaseSet = signed composition of system image + closures + policy + evidence
```

The system image should be boring, small, rollbackable, and policy-managed. Rich software choice belongs in Nix-built user and agent spaces, not in the host base.

## Canonical image families

### 1. Headless/server host image

Use for control-plane nodes, local mesh nodes, server-style appliances, cloud twins, and fleet infrastructure.

```yaml
image_family: fcos_server
base_style: Fedora CoreOS / CoreOS-like OSTree immutable image
system_plane_contents:
  - kernel and hardware enablement
  - container runtime primitives
  - networking primitives
  - policy enforcement hooks
  - fingerprint/reporting agent
  - update/rollback machinery
forbidden_by_default:
  - full desktop environments
  - browsers
  - development toolchains
  - agent toolchains
  - user applications
  - model training stacks
```

### 2. Desktop/workstation host image

Use for SourceOS desktop machines, M2 dual-boot Linux, workstation hosts, developer laptops, and machines that need local display/audio/input integration.

```yaml
image_family: silverblue_desktop
base_style: Silverblue/Kinoite/OSTree Fedora-family immutable desktop host
system_plane_contents:
  - kernel and hardware enablement
  - graphics primitives: DRM/KMS, Mesa or target hardware equivalent
  - Wayland/session bootstrap primitives
  - PipeWire/WirePlumber base audio plumbing
  - xdg-desktop-portal framework support
  - container/VM/microVM runtime hooks
  - policy enforcement hooks
  - fingerprint/reporting agent
  - update/rollback machinery
forbidden_by_default:
  - full app suites
  - arbitrary desktop package sprawl
  - development toolchains
  - agent runtimes and model stacks
  - broad mutable package installation
```

Desktop choice, such as GNOME, KDE, macOS-like, or Windows-like user experience, should compile into Nix-managed user-plane closures and configuration bundles. The immutable desktop host provides the integration surface, not the whole personalized workstation payload.

### 3. Recovery/installer image

Use for boot picker entries, live repair, install, rollback, key-gated enrollment, and SourceOS Recovery Environment flows.

```yaml
image_family: sourceos_recovery
base_style: minimal immutable live/recovery image
system_plane_contents:
  - network bootstrap
  - device claim generation
  - enrollment client
  - artifact fetch and signature verification
  - ReleaseSet / BootReleaseSet application tools
  - rollback and repair tools
forbidden_by_default:
  - general-purpose user desktop
  - persistent user apps
  - broad shell/tool bloat not needed for recovery
```

### 4. Service container image

Use for Prophet Platform services, APIs, gateways, workers, and small control-plane components.

```yaml
image_family: minimal_service_oci
preferred_runtime_bases:
  - scratch
  - distroless/static
  - Wolfi/Chainguard-style minimal
  - UBI minimal or Fedora minimal when a userspace is required
forbidden_by_default:
  - Ubuntu/Debian/Alpine as implicit host substrate
  - package managers in runtime images unless justified
  - shells in runtime images unless justified
  - compilers/build tools in runtime images
```

Builder stages may use convenient build images, but runtime stages must remain minimal and evidence-bound.

### 5. Beam pipeline image

Use for durable data-processing pipeline execution.

```yaml
image_family: beam_pipeline
canonical_data_substrate: Apache Beam
runtime_base: minimal userspace required by Beam runner and language SDK
requirements:
  - DataPipelineDecision
  - lineage evidence
  - replayability evidence
  - EvaluationRecord
```

### 6. Ray learning image

Use for Ray Train, Ray Tune, Ray RLlib, Ray Serve, and KubeRay workloads.

```yaml
image_family: ray_learning
canonical_learning_substrate: Ray ecosystem
canonical_data_path: Beam-produced/versioned data consumed through Ray-local adapters where needed
requirements:
  - RayLearningRun
  - EvaluationRecord
  - EpochRegressionCheck
  - model/checkpoint evidence
```

Ray Data is a Ray-local adapter, not the durable source-of-truth data pipeline unless a Beam exception is recorded.

### 7. User/agent closure image or bundle

Use for personalized user profiles, desktop environments, toolchains, agent environments, and workspace-specific capabilities.

```yaml
image_family: nix_user_agent_closure
base_style: Nix closure, profile, dev shell, bundle, or OCI image generated from Nix
contents:
  - user apps
  - GNOME/KDE/macOS-like/Windows-like profiles
  - developer tools
  - agent tools
  - language runtimes
  - ML/model tools
requirements:
  - BOM
  - closure hash
  - policy bundle
  - rollback generation
```

## Selection matrix

| Need | Preferred substrate | Why |
|---|---|---|
| Headless control plane / server | FCOS/CoreOS-like OSTree | Small, stable, fleet-safe, rollbackable |
| Desktop/workstation host | Silverblue/Kinoite/OSTree desktop host | Immutable host with graphics/audio/portal integration |
| Recovery/install/rollback | Minimal SourceOS recovery image | Purpose-built, no app bloat, key-gated enrollment |
| API/gateway/service | scratch/distroless/Wolfi/UBI-minimal OCI | Minimal runtime and digest evidence |
| Durable ETL/corpus pipeline | Beam pipeline image | Portable dataflow and lineage |
| Fine-tuning/RL/serving | Ray/KubeRay workload image | Distributed learning and serving substrate |
| User apps and DE preference | Nix user closure | Choice without system-plane bloat |
| Agent tools/runtimes | Nix agent closure or isolated OCI/microVM | Policy-governed capability and rollback |

## Bloat control rules

1. Do not put user applications in the immutable host unless required for host integration.
2. Do not put agent toolchains in the immutable host.
3. Do not put model training stacks in the immutable host.
4. Do not use mutable package installation as a normal system-plane operation.
5. Do not treat Ubuntu, Debian, or Alpine as the SourceOS host substrate.
6. Runtime service images should not contain package managers, shells, or compilers unless justified.
7. Each exception requires an evidence record, justification, owner, and migration target.

## Promotion requirements

An immutable image or service image may be promoted only when it has:

- image family classification;
- source inputs and build metadata;
- content digest or closure hash;
- SBOM/provenance where applicable;
- evaluation record;
- rollback path;
- Angel of the Lord review where source exposure, release, or platform-boundary risk applies.
