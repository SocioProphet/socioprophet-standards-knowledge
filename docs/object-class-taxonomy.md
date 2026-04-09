# Object class taxonomy v0.1

## Purpose

This document defines the first canonical object classes used by the Agentic Open Knowledge Commons.

These classes are referenced by `GeneralDescriptor.spec.object.objectType`.

## Core object classes

### DocumentAsset
Narrative or structured authored content.
Examples:
- architecture note
- design doc
- SOP
- knowledge article
- FAQ

### CodeAsset
Reusable code-oriented material.
Examples:
- repo file
- module
- script
- snippet
- configuration template

### RunbookAsset
Operational guidance intended for repeatable execution.
Examples:
- incident runbook
- support remediation flow
- deployment recovery procedure

### PromptAsset
Reusable prompt or prompt-fragment with stewarded intent.
Examples:
- prompt template
- evaluation rubric
- classification prompt

### BundleAsset
Execution-ready or execution-related package.
Examples:
- agentplane bundle
- transformation package
- publication package

### PolicyAsset
Normative policy or validation material.
Examples:
- policy pack
- access rule set
- promotion criteria bundle

### ConversationAsset
A conversation-derived unit not yet promoted or normalized into another asset class.
Examples:
- Matrix thread
- support chat transcript
- annotated review exchange

### EvidenceArtifact
Evidence emitted by governed workflows or execution.
Examples:
- validation artifact
- run artifact
- replay artifact
- publication receipt

### GraphTraversalAsset
A reusable traversal, cairn, query route, or graph-reasoning unit.
Examples:
- cairn path
- graph search plan
- ontology traversal template

### PublishedKnowledgeUnit
A canonical promoted unit intended for durable retrieval and reuse.
Examples:
- promoted runbook
- canonical support article
- steward-approved operational pattern

## Classification rule

An object should be assigned the narrowest correct class that preserves downstream behavior and governance.

## Promotion rule

A `ConversationAsset` should not remain the terminal state when it represents durable reusable knowledge. It should usually promote into `RunbookAsset`, `DocumentAsset`, or `PublishedKnowledgeUnit` after validation.
