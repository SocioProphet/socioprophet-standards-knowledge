# 081 — Operation Plane Memory and Knowledge Artifact Standard

Status: Draft v0.1
Authority: `SocioProphet/socioprophet-standards-knowledge`

## Purpose

Define the minimum knowledge-side standard for Workspace Operation Plane memory ingestion, evidence-linked memory artifacts, metadata discipline, correction/deletion propagation, and policy-governed agent visibility.

This standard is semantic-only and does not change TriTRPC framing, schema/context ID registries, fixture bytes, or existing roundtrip contracts.

## Alignment with `SocioProphet/prophet-core-contracts#1`

Operation Plane memory MUST be represented as explicit artifacts and operations:

- memory ingestion MUST emit a `WorkspaceOperation` artifact (not hidden indexing side effect);
- memory records MUST be represented as evidence-linked knowledge artifacts;
- merge decisions MUST emit a `DecisionCard` artifact with evidence and policy refs;
- agent visibility MUST be controlled by policy records and produce auditable access evidence.

## Required memory record model

Every Operation Plane memory artifact MUST carry:

```yaml
artifact_type: OperationPlaneMemoryArtifact
memory_id: stable identifier
workspace_ref: workspace identifier
memory_namespace: namespace path (see namespace model)
lifecycle_state: quarantined | admitted | activated | corrected | expired | deleted
source_trust_level: system_verified | workspace_verified | steward_reviewed | external_attested | unverified
evidence_refs: list of evidence artifact refs
provenance_refs: list of provenance root refs
confidence:
  score: 0.0-1.0
  method: rule | model | hybrid | human
  assessed_at: ISO-8601 datetime
retention:
  class: ephemeral | bounded | durable | legal_hold
  expires_at: ISO-8601 datetime or null
  decay_model: none | linear | step | event_driven
privacy:
  label: public | internal | restricted | secret
  visibility_policy_ref: policy record ref
embedding:
  model: embedding model name
  model_version: embedding model version
  vector_dimensions: integer
chunking:
  strategy: sentence_window | semantic_boundary | section_window | custom
  chunk_size_tokens: integer
  chunk_overlap_tokens: integer
  splitter_version: splitter/segmenter version
dedupe:
  dedupe_key: stable deterministic key
  merge_strategy: prefer_newer | prefer_higher_trust | weighted_merge | manual_only
freshness:
  observed_at: ISO-8601 datetime
  last_refreshed_at: ISO-8601 datetime
  freshness_state: fresh | aging | stale | expired
```

## Memory namespace model

`memory_namespace` MUST use a stable hierarchical form:

`workspace/{workspaceId}/operation-plane/{scope}/{artifactClass}/{topicPath}`

Rules:

- `workspaceId`, `scope`, and `artifactClass` are required segments;
- namespace assignment MUST be deterministic for the same subject/scope pair;
- cross-workspace merge MUST NOT rewrite source namespace; it may add linked alias namespaces.

## Source trust, evidence, and confidence

- `source_trust_level` MUST be explicit and MUST NOT be inferred at read time.
- `evidence_refs` MUST point to retrievable evidence artifacts.
- `provenance_refs` MUST preserve source-to-memory traceability.
- confidence score MUST include numeric score and method.
- confidence MAY decay over time under the declared decay model.

## Retention, expiry, and decay

- retention class MUST be declared at admission time.
- if `retention.class != legal_hold`, an expiry policy MUST be present (`expires_at` or decay rule).
- `expired` memory MUST remain evidentially traceable and MUST NOT be treated as active context.
- decayed memories SHOULD lower retrieval rank and agent influence before full expiry.

## Privacy label and agent visibility rules

Visibility MUST be policy-governed and auditable.

- every memory artifact MUST include `privacy.label` and `privacy.visibility_policy_ref`;
- agent read access MUST evaluate policy at access time;
- access decisions MUST emit auditable evidence (allow/deny + policy ref + reason);
- restricted or secret memory MUST NOT be returned to agents lacking policy grant.

## Embedding/chunking metadata

- embedding metadata MUST include model name and version to allow reproducible re-indexing.
- chunk metadata MUST include strategy and segmentation version.
- re-embedding with a new model/version SHOULD emit a correction artifact linking old and new vector lineage.

## Dedupe key and merge strategy

- `dedupe.dedupe_key` MUST be deterministic for semantically identical memory candidates.
- merge outcomes MUST produce a `DecisionCard` with:
  - candidate refs,
  - chosen merge strategy,
  - policy/evidence refs,
  - resulting memory ref.

## Correction workflow and deletion propagation

Correction and deletion MUST be first-class operations:

- corrections MUST create `WorkspaceOperation` records and `corrected` memory artifacts with backward refs;
- deletion MUST propagate to dependent projections/chunks and emit deletion evidence;
- delete propagation MUST preserve audit trail while preventing further agent retrieval of deleted memory;
- quarantine/admission/activation/correction/expiry/deletion transitions MUST all be evidence-linked.

## Memory artifact admission gates

A candidate memory MUST be blocked from `admitted` unless all gates pass:

1. evidence gate: evidence/provenance refs present;
2. policy gate: privacy + visibility policy valid;
3. dedupe gate: dedupe key computed and merge decision recorded;
4. quality gate: confidence score and freshness timestamps present.

Failed gates MUST keep memory in `quarantined` with gate-failure evidence.

## Knowledge freshness indicators

Memory freshness MUST be externally visible through:

- `freshness.observed_at`
- `freshness.last_refreshed_at`
- `freshness.freshness_state`
- optional `freshness.next_review_at`

Agents SHOULD prefer `fresh` over `aging`, and SHOULD deprioritize `stale`/`expired` unless a task explicitly requests historical context.

## Required examples

### 1) Memory ingestion operation artifact

```yaml
artifact_type: WorkspaceOperation
operation_kind: memory_ingestion
operation_id: opmem_2026_05_07_001
workspace_ref: ws_alpha
memory_candidate_ref: memcand_customer_policy_17
result_state: quarantined
evidence_refs:
  - ev_ingest_receipt_441
  - ev_source_doc_992
```

### 2) Evidence-linked note/page artifact

```yaml
artifact_type: OperationPlaneMemoryArtifact
memory_id: mem_note_customer_policy_17
memory_namespace: workspace/ws_alpha/operation-plane/customer-support/note/policy/returns
lifecycle_state: admitted
source_trust_level: workspace_verified
evidence_refs:
  - ev_source_doc_992
provenance_refs:
  - prov_doc_992_root
confidence:
  score: 0.81
  method: hybrid
  assessed_at: 2026-05-07T05:30:00Z
```

### 3) Semantic chunk artifact

```yaml
artifact_type: OperationPlaneMemoryArtifact
memory_id: mem_chunk_customer_policy_17_03
memory_namespace: workspace/ws_alpha/operation-plane/customer-support/chunk/policy/returns
lifecycle_state: activated
embedding:
  model: text-embedding-3-large
  model_version: 2026-02-15
  vector_dimensions: 3072
chunking:
  strategy: semantic_boundary
  chunk_size_tokens: 320
  chunk_overlap_tokens: 48
  splitter_version: seg-v2.1
```

### 4) Corrected memory artifact

```yaml
artifact_type: OperationPlaneMemoryArtifact
memory_id: mem_note_customer_policy_17_v2
lifecycle_state: corrected
correction_of_ref: mem_note_customer_policy_17
correction_operation_ref: opmem_2026_05_07_022
evidence_refs:
  - ev_errata_notice_22
  - ev_source_doc_1010
```

### 5) Expired/decayed memory artifact

```yaml
artifact_type: OperationPlaneMemoryArtifact
memory_id: mem_market_signal_q3_2024
lifecycle_state: expired
retention:
  class: bounded
  expires_at: 2026-04-30T23:59:59Z
  decay_model: linear
freshness:
  observed_at: 2024-07-04T09:00:00Z
  last_refreshed_at: 2026-05-01T18:10:00Z
  freshness_state: expired
```

### 6) Agent-visible memory policy record

```yaml
artifact_type: AgentMemoryVisibilityPolicy
policy_id: pol_mem_visibility_ws_alpha_v1
workspace_ref: ws_alpha
rules:
  - match: {privacy_label: restricted, agent_role: support_agent}
    effect: deny
  - match: {privacy_label: internal, agent_role: support_agent}
    effect: allow
audit_required: true
```

### 7) Memory merge DecisionCard example

```yaml
artifact_type: DecisionCard
decision_id: dcard_mem_merge_2026_05_07_003
decision_kind: memory_merge
workspace_ref: ws_alpha
candidate_memory_refs:
  - mem_note_customer_policy_17
  - mem_note_customer_policy_17_dup
merge_strategy: prefer_higher_trust
result_memory_ref: mem_note_customer_policy_17_canonical
evidence_refs:
  - ev_similarity_report_55
  - ev_steward_review_88
policy_refs:
  - pol_mem_merge_ws_alpha_v1
```
