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

The standard intentionally mirrors the successful Fedora/Red Hat family pattern: separate server/core images, desktop atomic images, IoT/edge images, universal/minimal container bases, boot/recovery artifacts, and layered workload images. SourceOS should build, package, and interoperate with those market patterns rather than inventing a single overloaded image.

## Core doctrine

```text
immutable system image = host substrate and integration surface
Nix closure = user/agent environment and tool composition
service image = minimal OCI runtime artifact
ReleaseSet = signed composition of system image + closures + policy + evidence
```

The system image should be boring, small, rollbackable, and policy-managed. Rich software choice belongs in Nix-built user and agent spaces, not in the host base.

## Fedora / Red Hat pattern alignment

SourceOS image families should track these upstream-style families conceptually:

| Upstream-style pattern | SourceOS family | SourceOS role |
|---|---|---|
| Fedora CoreOS / RHEL CoreOS style | `sourceos_core_server` | Headless immutable server/control-plane host |
| Fedora Silverblue style | `sourceos_silverblue_gnome` | GNOME workstation host integration surface |
| Fedora Kinoite style | `sourceos_kinoite_kde` | KDE workstation host integration surface |
| Fedora IoT / Edge style | `sourceos_edge_iot` | Edge/local mesh appliance and constrained node |
| Universal Base Image / minimal base style | `sourceos_ubi_service_base` | Minimal service userspace when scratch/distroless is insufficient |
| Boot ISO / installer / recovery style | `sourceos_recovery` | Install, live, recovery, rollback, enrollment |
| Container-native workload images | `minimal_service_oci`, `beam_pipeline`, `ray_learning` | Application and learning workloads |
| User profile / toolbox style | `nix_user_agent_closure` | User apps, DE choices, dev tools, agent tools |

This alignment is a packaging and lifecycle discipline, not a license to pull bloat into the system plane.

## Canonical image families

### 1. Core server / headless control-plane host image

Use for control-plane nodes, local mesh nodes, server-style appliances, cloud twins, fleet infrastructure, and headless deployment targets.

```yaml
image_family: sourceos_core_server
upstream_pattern: Fedora CoreOS / RHEL CoreOS style
base_style: CoreOS-like OSTree immutable image
system_plane_contents:
  - kernel and hardware enablement
  - container runtime primitives
  - networking primitives
  - policy enforcement hooks
  - fingerprint/reporting agent
  - update/rollback machinery
  - minimal host services required for fleet operation
forbidden_by_default:
  - full desktop environments
  - browsers
  - development toolchains
  - agent toolchains
  - user applications
  - model training stacks
```

### 2. GNOME desktop/workstation host image

Use for SourceOS desktop machines, M2 dual-boot Linux, workstation hosts, developer laptops, and machines that need local display/audio/input integration with a GNOME/Silverblue-style base.

```yaml
image_family: sourceos_silverblue_gnome
upstream_pattern: Fedora Silverblue style
base_style: Silverblue/OSTree Fedora-family immutable desktop host
system_plane_contents:
  - kernel and hardware enablement
  - graphics primitives: DRM/KMS, Mesa or target hardware equivalent
  - Wayland/session bootstrap primitives
  - GNOME-compatible host integration primitives
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

### 3. KDE desktop/workstation host image

Use for KDE/Windows-like workstation targets where a Kinoite-style host is the right integration surface.

```yaml
image_family: sourceos_kinoite_kde
upstream_pattern: Fedora Kinoite style
base_style: Kinoite/OSTree Fedora-family immutable desktop host
system_plane_contents:
  - kernel and hardware enablement
  - graphics primitives
  - Wayland/session bootstrap primitives
  - KDE-compatible host integration primitives
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

### 4. Edge / IoT / local mesh image

Use for small always-on nodes, local mesh appliances, constrained devices, lab nodes, and edge control points.

```yaml
image_family: sourceos_edge_iot
upstream_pattern: Fedora IoT / RHEL for Edge style
base_style: small immutable OSTree edge image
system_plane_contents:
  - kernel and hardware enablement
  - networking and mesh primitives
  - container runtime where needed
  - device identity and fingerprinting
  - policy enforcement hooks
  - update/rollback machinery
forbidden_by_default:
  - desktop environments
  - heavy analytics stacks
  - development toolchains
  - model training stacks unless explicitly an edge accelerator profile
```

### 5. Recovery/installer image

Use for boot picker entries, live repair, install, rollback, key-gated enrollment, and SourceOS Recovery Environment flows.

```yaml
image_family: sourceos_recovery
upstream_pattern: installer / recovery / live ISO style
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

### 6. Service container image

Use for Prophet Platform services, APIs, gateways, workers, and small control-plane components.

```yaml
image_family: minimal_service_oci
upstream_pattern: scratch / distroless / UBI minimal / Fedora minimal style
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

### 7. UBI/Fedora minimal service base

Use when a service cannot practically run from scratch/distroless and needs a supported userspace base.

```yaml
image_family: sourceos_ubi_service_base
upstream_pattern: Red Hat UBI minimal / Fedora minimal style
base_style: minimal userspace OCI base
allowed_contents:
  - runtime libraries required by the service
  - CA certificates when needed
  - timezone/locale only when justified
  - minimal debug hooks only in debug variants
forbidden_by_default:
  - package manager in production image unless explicitly required
  - shell in production image unless explicitly required
  - compiler/build tools
  - desktop/user applications
```

### 8. Beam pipeline image

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

### 9. Ray learning image

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

### 10. User/agent closure image or bundle

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
| Headless control plane / server | `sourceos_core_server` | Small, stable, fleet-safe, rollbackable |
| GNOME/Mac-like workstation host | `sourceos_silverblue_gnome` | Immutable GNOME-oriented integration surface |
| KDE/Windows-like workstation host | `sourceos_kinoite_kde` | Immutable KDE-oriented integration surface |
| Edge/local mesh appliance | `sourceos_edge_iot` | Small edge image with identity, networking, rollback |
| Recovery/install/rollback | `sourceos_recovery` | Purpose-built, no app bloat, key-gated enrollment |
| API/gateway/service | `minimal_service_oci` or `sourceos_ubi_service_base` | Minimal runtime and digest evidence |
| Durable ETL/corpus pipeline | `beam_pipeline` | Portable dataflow and lineage |
| Fine-tuning/RL/serving | `ray_learning` | Distributed learning and serving substrate |
| User apps and DE preference | `nix_user_agent_closure` | Choice without system-plane bloat |
| Agent tools/runtimes | `nix_user_agent_closure` or isolated OCI/microVM | Policy-governed capability and rollback |

## Build and package discipline

SourceOS should reuse Fedora/Red Hat patterns where they fit:

- OSTree/rpm-ostree-style immutable host composition for system images.
- CoreOS-style declarative provisioning patterns for headless/server hosts.
- Silverblue/Kinoite-style atomic desktop host patterns for workstations.
- UBI/Fedora-minimal-style service base patterns when service images need userspace.
- Installer/recovery/live image patterns for BootReleaseSet and SourceOS Recovery Environment.
- SBOM/provenance/signing/promotion evidence for all promoted images.

Nix remains the lifecycle and composition plane for user and agent spaces and for policy-controlled closure generation. Nix must not be used as an excuse to mutate the immutable host arbitrarily.

## Bloat control rules

1. Do not put user applications in the immutable host unless required for host integration.
2. Do not put agent toolchains in the immutable host.
3. Do not put model training stacks in the immutable host.
4. Do not use mutable package installation as a normal system-plane operation.
5. Do not treat Ubuntu, Debian, or Alpine as the SourceOS host substrate.
6. Runtime service images should not contain package managers, shells, or compilers unless justified.
7. Each exception requires an evidence record, justification, owner, expiration or migration target.

## Promotion requirements

An immutable image or service image may be promoted only when it has:

- image family classification;
- upstream-style pattern classification;
- source inputs and build metadata;
- content digest or closure hash;
- SBOM/provenance where applicable;
- evaluation record;
- rollback path;
- Angel of the Lord review where source exposure, release, or platform-boundary risk applies.
