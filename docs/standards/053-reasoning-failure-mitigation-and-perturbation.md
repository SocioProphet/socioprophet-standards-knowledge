# Standard 053: Reasoning Failure Mitigation and Perturbation v0.1

Parent: SocioProphet/sociosphere#271 and SocioProphet/socioprophet-standards-knowledge#69.

## Purpose

This standard defines the knowledge-layer contract for reasoning-failure cases, perturbation suites, mitigation patterns, evaluator-bias controls, and exactness gates. It is intentionally standards-first: Ontogenesis owns the failure vocabulary, while runtime systems own execution, traces, receipts, policy actions, routing, storage, and UI.

A model or agent is not reliable because it answers correctly once. A model or agent is reliable only when the answer survives invariant-preserving perturbation, deterministic or tool-backed verification where available, provenance inspection, and domain-specific validation.

## Normative vocabulary ownership

Reasoning-failure mode identifiers MUST reference `https://socioprophet.github.io/ontogenesis/platform/reasoning-failure#` terms or a documented downstream extension approved by Ontogenesis.

This standard MUST NOT define a competing failure ontology. It defines portable artifact shapes and validation expectations for systems that consume the Ontogenesis vocabulary.

## ReasoningFailureCase artifact

A `ReasoningFailureCase` artifact MUST include:

- stable `caseId`;
- `failureModeRefs`;
- `taskClass`;
- `domain`;
- `severity`;
- `invariant`;
- `expectedOutcome`;
- `observedOutput`;
- `verifier`;
- `evidenceReceiptRefs`;
- `mitigationRefs`;
- `residualRisk`;
- `riskAction`;
- `privacyBoundary`.

For production or customer-adjacent use, raw prompts, raw customer data, secrets, browser profiles, token stores, private app databases, and unredacted telemetry MUST NOT be embedded directly. Use evidence receipt refs, digests, redaction provenance, or synthetic fixtures.

## PerturbationSuite artifact

A `PerturbationSuite` artifact MUST include:

- stable `suiteId`;
- `targetCaseId`;
- invariant-preserving `perturbations`;
- expected invariant behavior;
- verifier family;
- negative controls where applicable;
- evaluator-bias controls if LLM-as-judge is used.

## Required perturbation families

Implementations SHOULD support at least these perturbation families:

- option/order randomization;
- variable, entity, and identifier renaming;
- relation reversal and inverse tests;
- number/value swaps and impossible-condition cases;
- distractor injection;
- paraphrase and framing changes;
- few-shot/example position changes;
- code mutation and identifier-swap tests;
- modality disagreement tests across screenshot, DOM, text, map, PDF, geometry, and metadata evidence;
- multi-agent role, order, communication, and termination perturbations.

## Exactness profile

Exactness-sensitive tasks include IDs, filenames, checksums, signatures, version strings, package names, schema refs, config fields, YAML/TOML/JSON keys, boot/release refs, and cryptographic-looking values.

Exactness-sensitive outputs MUST be verified with deterministic tooling before runtime admission. LLM-authored prose is advisory only.

## Evaluator-bias controls

When LLM-as-judge is used, systems MUST record it as advisory unless backed by deterministic, symbolic, schema, policy, tool, or human-review evidence. Evaluation runs SHOULD include:

- judge order randomization;
- answer order randomization;
- verbosity-bias checks;
- source popularity bias checks;
- benchmark contamination notes;
- multi-judge variance when available.

## Causal and temporal labels

Causal claims SHOULD be labeled as correlation, mechanism, intervention, counterfactual, confounder-risk, or unsupported. Temporal claims SHOULD distinguish event time, observed time, valid time, issue time, release time, and stale-source risk.

## Multimodal contradiction controls

When rendered UI, DOM/accessibility tree, OCR/text, PDF text, pixel evidence, map geometry, metadata, or tile attribution disagree, systems MUST preserve the contradiction and require a verifier or review gate before claiming resolution.

## Mitigation pattern catalog

Mitigation references SHOULD use Ontogenesis mitigation terms such as deterministic tool delegation, reverse relation testing, semantic-aware permutation testing, graph synthetic data, logic scaffolding, self-challenge counterexamples, ontology-guided intervention, simulator/world-model grounding, independent verifier, and agent trace monitoring.

## Downstream consumers

- Prophet Platform runs suites and emits receipts.
- AgentPlane records typed traces and termination/verifier decisions.
- Guardrail Fabric maps failed or uncertain signals to runtime actions.
- Policy Fabric gates memory, tools, export, and termination.
- Model Governance Ledger stores receipts for promotion, waiver, rollback, and revocation.
- Agent Registry adjusts authority.
- Model Router routes by failure-risk class and verifier requirement.
- Sherlock indexes cases, evidence, contradictions, causal labels, temporal labels, and mitigations.
- DeliveryExcellence reports robustness and recurrence metrics.
