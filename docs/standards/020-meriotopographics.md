# Meriotopographic Relations (Normative)

## 0. Naming + Transport Note
**TriTRPC** (SocioProphet/tritrpc) is the canonical transport/envelope/encoding layer (aliases: triRPC, trirpc, triunerpc).
This document defines **semantic** relation predicates and invariants; TriTRPC is only the carrier.

## 1. Purpose
Meriotopographic relations express part–whole, placement/anchoring, derivation, epistemic, and governance semantics across Knowledge Context artifacts.
All Knowledge Context implementations MUST honor these predicates and invariants.

## 2. Predicate Registry

### 2.1 Structural (Mereological)
- part_of / has_part — strict part–whole; MUST be acyclic within a workspace scope.
- member_of / contains — loose collection membership; cycles permitted.

### 2.2 Topological (Placement / Anchoring)
- located_in — containment (workspace, document, section).
- adjacent_to — navigational proximity; no ordering implied.
- overlaps — partial span overlap; MUST reference anchors.
- anchors_to — binds an artifact/claim to an anchor.

### 2.3 Derivation / Dependency
- derives_from — lineage relation; MUST be acyclic globally.
- references — weak dependency; cycles permitted.
- cites — bibliographic dependency.

### 2.4 Epistemic
- supports — positive evidentiary relation.
- contradicts — negative evidentiary relation.

### 2.5 Governance / Trust
- asserted_by — who/what asserted the relation.
- validated_by — human quorum validation.
- attested_by — cryptographic or institutional attestation.
- redacted_by — privacy transform applied.
- masked_by — masking rule applied prior to indexing/export.

Custom predicates MUST use the prefix `x-<org>.<name>`.

## 3. Invariants

### 3.1 Acyclicity
- part_of and derives_from MUST form DAGs; violations MUST fail validation.

### 3.2 Anchors
- overlaps and anchors_to MUST reference a valid AnchorRef.

### 3.3 Privacy Ordering
- masked_by/redacted_by MUST precede indexing, embedding, or publishing steps.

### 3.4 Validation
- validated_by MUST include quorum metadata when required by policy.

## 4. Storage Mapping
- RDF: predicates map to IRIs; edges may be reified for provenance.
- Property graph: predicates are edge labels; invariants enforced at application layer.
- Hypergraph: predicates MAY be modeled as relation nodes.

## 5. Compliance
Implementations that violate these invariants are non-compliant with the Knowledge Context standard.
