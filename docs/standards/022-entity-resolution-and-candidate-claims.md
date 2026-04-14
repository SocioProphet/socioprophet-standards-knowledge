# Entity Resolution and Candidate Claims (Normative)

This document defines the minimal contract for merge/split decisions over entities and for promoting inferred links back into the Knowledge Context.

## 1) Scope
The canonical artifact introduced here is `EntityResolutionRecord`.

## 2) Resolution rules
- Entity resolution operations MUST be recorded as one of: `merge`, `split`, `link`, or `reject`.
- Every `EntityResolutionRecord` MUST identify the candidate nodes considered.
- A merge or link decision SHOULD identify a decided node.
- Resolution activity SHOULD carry a score and MAY carry a textual rationale.

## 3) Provenance rules
- Resolution outputs MUST be attributable through `ProvenanceRecord`.
- Offline graph-cleaning or link-prediction jobs MUST record the producing component and run identifier.

## 4) Candidate claim rules
- Inferred links or claims produced by offline jobs MUST enter the system as candidate artifacts, not as silently promoted truth.
- Candidate claims SHOULD remain reviewable until accepted by the applicable validation policy.
- Resolution and candidate-claim promotion MUST preserve replayability and auditability.

## 5) Runtime posture
Reasoning and large-scale graph inference MAY run offline. The online store and graph surface SHOULD prioritize retrieval, provenance, validation state, and deterministic replay over heavyweight runtime reasoning.
