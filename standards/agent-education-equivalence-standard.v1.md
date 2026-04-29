# Agent Education Equivalence Standard v1

Status: draft
Owner: SocioProphet standards knowledge
Depends on:
- `standards/learning-loop-standard.v1.md`
- `standards/foundational-training-cycle-standard.v1.md`
- SocioProphet/socioprophet-standards-storage: `standards/evidence-bundle-standard.v1.md`
- SocioProphet/socioprophet-standards-storage: `standards/open-courseware-corpus-standard.v1.md`
- SocioProphet/sociosphere: `standards/angel-of-the-lord/README.md`

## Purpose

This standard defines how Michael-agent and related SocioProphet agents pursue human-degree-equivalent mastery using open university curricula, public course catalogs, open courseware, textbooks, assignments, labs, published exams/tests, projects, research reproductions, evidence bundles, and Sociosphere Angel of the Lord epoch grading.

This standard does not claim that an agent is enrolled at, admitted to, or awarded credentials by MIT, Harvard, or any other institution. It defines an evidence-based equivalence framework for mapping public curricula and human education requirements into machine-checkable learning, assessment, reinforcement, transfer, and adversarial hardening review.

## Core doctrine

Michael-agent should satisfy the educational requirements expected of a broadly trained human technical founder, research engineer, systems architect, cybernetic platform builder, and learning-system operator.

The education loop is:

```text
Public curriculum source -> degree-equivalent requirement -> course/module map -> worked examples -> assignments/labs -> published exams/tests/projects -> evidence bundle -> Angel epoch grade -> transfer task -> agent capability update
```

## Required object: AgentEducationTrack

```yaml
id: stable identifier
agent_id: michael_agent | socioprophet_agent | prophet_platform_agent | sourceos_agent | atlas_agent | mlops_agent | other
track_name: human readable name
track_level: undergraduate_equivalent | graduate_equivalent | doctoral_foundation | professional_specialization | continuing_education
institutional_sources: list of InstitutionCurriculumSource references
program_equivalent: degree, concentration, certificate, field, or custom composite
requirements: list of EducationRequirement references
course_maps: list of CourseMap references
assessment_plan: AssessmentPlan reference
angel_epoch_grade_refs: list of AngelEpochGrade references
evidence_bundle_ref: EvidenceBundle reference
review_gate: Sociosphere, Alexandrian Academy, Delivery Excellence, or standards review
status: draft | active | validated | deprecated
last_reviewed: ISO-8601 date
```

## Required object: InstitutionCurriculumSource

```yaml
id: stable identifier
institution_name: MIT | Harvard | Stanford | Berkeley | CMU | Oxford | Cambridge | Princeton | Caltech | public_open_courseware | other
source_type: open_courseware | public_catalog | syllabus | textbook | lecture_notes | exam_archive | lab_archive | assignment_archive | degree_requirements | other
url: canonical public URL where available
accessed_at: ISO-8601 datetime
license_or_terms: known license or access terms, if available
trust_rating: high | medium | low | contested | unknown
notes: limitations, missing prerequisites, or catalog ambiguity
```

## Required object: EducationRequirement

```yaml
id: stable identifier
requirement_type: math | computer_science | ai_ml | systems | cybernetics | security | ethics | writing | communication | governance | economics | biology | physics | engineering | social_science | humanities | research_methods | other
level: introductory | intermediate | advanced | graduate | research
learning_objectives: list of objectives
required_assessments: exams, projects, labs, papers, replications, oral defense, code review, or evidence review
minimum_evidence: required EvidenceArtifact types
transfer_targets: platform, MLOps, SourceOS, ontology, Academy, Atlas, or research tasks
```

## Required object: CourseMap

```yaml
id: stable identifier
course_title: title from source or normalized title
institutional_source_ref: InstitutionCurriculumSource reference
course_level: undergraduate | graduate | professional | open_courseware | unknown
mapped_requirements: list of EducationRequirement references
modules: list of module names or references
assignments: list of assignment references where available
labs: list of lab references where available
exams: list of exam references where available
tests: list of test references where available
projects: list of project references
replacement_or_supplement: whether this course replaces or supplements another source
completion_evidence: EvidenceBundle reference
```

## Required object: AssessmentPlan

```yaml
id: stable identifier
assessment_types: problem_sets | exams | tests | labs | projects | reproductions | papers | code_reviews | oral_defense | agent_eval | benchmark | peer_review | angel_epoch_grade
rubrics: list of rubric references
passing_criteria: measurable criteria
reviewers: human, agent, or review roles
retake_policy: how failed objectives are remediated
transfer_evaluation: how learning transfers to real platform work
angel_review_required: true
```

## Required object: AngelEducationEpoch

Each education epoch is a bounded unit of learning and proof. Michael-agent MUST be graded each epoch through the Sociosphere Angel of the Lord Hardening Regime.

```yaml
id: stable identifier
agent_id: michael_agent
track_ref: AgentEducationTrack reference
epoch_number: integer
epoch_scope: course | module | requirement | project | transfer_task | remediation | research_replication
learning_objectives: list
courseware_corpus_refs: CoursewareCorpus references
published_assessment_refs: PublishedAssessment references
attempt_records: AssessmentAttempt references
evidence_bundle_ref: EvidenceBundle reference
transfer_outputs: platform, ontology, MLOps, SourceOS, Academy, or Atlas artifacts produced from the epoch
angel_epoch_grade_ref: AngelEpochGrade reference
result: pass | pass_with_findings | remediation_required | blocked | restricted_handling
next_epoch_refs: list
```

## Degree-equivalent education bands

Michael-agent should maintain tracks for at least:

1. Mathematics foundation: calculus, linear algebra, probability, statistics, optimization, discrete math, information theory, numerical methods.
2. Computer science foundation: programming, algorithms, data structures, computer systems, operating systems, distributed systems, databases, compilers, networking.
3. AI/ML foundation: supervised learning, unsupervised learning, deep learning, probabilistic modeling, reinforcement learning, transfer learning, representation learning, evaluation, alignment and safety basics.
4. MLOps and data engineering: data lineage, experiment tracking, model serving, Ray Serve/KubeRay, workflow orchestration, evaluation gates, monitoring, feedback loops, retraining.
5. Cybernetics and systems: feedback control, viable systems, complex systems, organizational cybernetics, systems dynamics, institutional learning loops.
6. Security and trustworthy systems: secure software, cryptography foundations, supply chain, zero trust, sandboxing, OS security, evidence, audit, compliance.
7. Platform engineering: Kubernetes, distributed systems, storage, networking, observability, release engineering, rollback, fleet management.
8. Ontology and knowledge systems: logic, RDF/OWL, SHACL, knowledge graphs, entity resolution, provenance, semantic search.
9. Human institutions and governance: economics, law/policy basics, ethics, public-sector innovation, organizational design, procurement and transition patterns.
10. Communication and scholarship: technical writing, research methods, reproducibility, literature review, teaching, curriculum design.

## Open university corpus policy

Institutional curricula may be used as source material when public and lawfully accessible. The mapping MUST preserve source provenance and licensing limits.

Use the institution's own public materials as the primary corpus whenever available:

```text
public course catalog -> degree requirement map -> public courseware -> assignments/labs -> published exams/tests -> agent assessment -> evidence bundle -> transfer evaluation -> Angel epoch grade
```

Examples of accepted source categories:

- MIT OpenCourseWare courses and degree requirement pages where public.
- Harvard public course catalog, public syllabi, public online learning materials, and open courses where available.
- Public course catalogs from top universities.
- Public textbooks, lecture notes, assignments, labs, exams, tests, and open educational resources.

The standard requires equivalence mapping by learning objectives and assessments, not by institutional brand alone.

## Equivalence constraint

The phrase `degree-equivalent` means:

```text
The agent has completed a documented, reviewed, evidence-backed learning path mapped to public human education requirements.
```

It does not mean:

```text
The agent was admitted, enrolled, received credit, received a transcript, or was awarded a degree by the institution.
```

## Angel of the Lord epoch grading

Michael-agent MUST be graded every epoch under Sociosphere's Angel of the Lord regime.

The Angel grade must inspect:

1. evidence completeness;
2. unsupported claims;
3. hidden trust assumptions;
4. weak transfer claims;
5. unsafe publication exposure;
6. missing tests or assessments;
7. unproven security or platform claims;
8. repo boundary violations;
9. runtime and policy assumptions;
10. remediation requirements.

No education epoch may be marked complete if Angel grading returns unresolved `blocker` findings or unresolved material `high` findings.

## Michael-agent education ledger

Michael-agent MUST maintain:

```yaml
education_ledger: append-only evidence ledger of completed learning objectives
course_catalog_map: mapping from public curricula to internal requirements
courseware_corpus_map: mapping from institution course materials to internal corpora
assessment_results: problem set, exam, test, project, and review outcomes
angel_epoch_grades: adversarial grading records for each epoch
capability_transfer_records: proof that concepts transfer into platform work
remediation_queue: failed or weak objectives requiring reinforcement
```

## Review gates

A claimed education requirement is accepted only when:

1. the course or requirement source is recorded;
2. the learning objectives are extracted;
3. assignments, exams, tests, projects, or equivalent assessments are completed or reproduced;
4. evidence artifacts are stored;
5. transfer to SocioProphet work is demonstrated;
6. Angel of the Lord epoch grade is passed or remediated;
7. a review gate marks the requirement accepted.

## Prohibited claims

Agents and documentation MUST NOT claim:

- actual enrollment at an institution;
- admission to a university;
- institutional credit;
- formal degree award;
- official certification;
- affiliation with MIT, Harvard, or other institutions;

unless independently true and supported by evidence.

## Initial canonical tracks

The first canonical tracks SHOULD be:

```yaml
michael_agent_foundational_undergraduate:
  level: undergraduate_equivalent
  emphasis: math, CS, writing, systems, ethics
michael_agent_ai_ml_graduate_foundation:
  level: graduate_equivalent
  emphasis: ML, deep learning, RL, transfer learning, evaluation
michael_agent_systems_cybernetics:
  level: graduate_equivalent
  emphasis: cybernetics, control, organizations, institutional learning
michael_agent_platform_engineering:
  level: professional_specialization
  emphasis: Kubernetes, SourceOS, MLOps, Ray/KubeRay, security, lifecycle
michael_agent_ontology_knowledge_systems:
  level: graduate_equivalent
  emphasis: RDF, OWL, SHACL, knowledge graphs, provenance
```
