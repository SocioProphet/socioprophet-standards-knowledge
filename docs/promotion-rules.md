# Promotion rules v0.1

## Purpose

This document defines the minimum rules for promoting non-canonical material into canonical reusable knowledge.

## Promotion candidates

Promotion candidates include:
- Matrix threads that resolve real operational issues
- support conversations with repeated reuse value
- incident notes that become durable runbooks
- ad hoc scripts or snippets used successfully in repeated tasks
- draft documents with steward-confirmed operational value

## Promotion gates

A promotion MUST NOT complete unless the following conditions are satisfied:

1. provenance is present
2. policy scope is valid
3. duplicate or near-duplicate checks are complete
4. target content space is valid
5. the asset class after promotion is explicit
6. required human review is complete when the policy requires it

## Preferred promotion paths

- `ConversationAsset` -> `RunbookAsset`
- `ConversationAsset` -> `DocumentAsset`
- `ConversationAsset` -> `PublishedKnowledgeUnit`
- `CodeAsset` -> `PublishedKnowledgeUnit`
- `RunbookAsset` -> `PublishedKnowledgeUnit`

## Required promotion outputs

A successful promotion SHOULD emit:
- validation evidence
- promotion artifact
- publication artifact
- replay reference when a governed execution step was involved

## Rejection conditions

A promotion SHOULD be rejected when:
- provenance is missing
- policy prohibits the target publication scope
- the candidate is stale or contradicted by newer stewarded assets
- the candidate duplicates an existing canonical asset without meaningful delta
- the candidate contains unresolved sensitive information

## Steward accountability

Promotion into canonical status is a governed act. Agents may propose or draft, but steward accountability remains explicit unless policy narrows and delegates that responsibility.
