# ND Oracle Knowledge Model Semantic Repair v0.2.1

Status: proposed design repair only. This document does not authorise schema implementation, validator mutation, migration of authoritative knowledge objects, creation of new authoritative knowledge content, website/search/AI work, or deployment.

## 1. Purpose

Repair four semantic ambiguities identified during review of the accepted Knowledge Object Model v0.2 and Schema Implementation Plan v0.2 before they are encoded in JSON Schema.

This repair preserves the accepted six top-level object types:

- Concept
- Evidence
- Question
- Resource
- Perspective
- Experience

It does not add a seventh standalone Claim object or a standalone Source object in v0.2.1.

The repair addresses:

1. which objects may carry substantive claims;
2. the distinction between reusable Questions and embedded Uncertainties;
3. the distinction between source identity and claim-specific Evidence Contributions;
4. schema-version naming and typed reference structure.

## 2. Governing rule

The model must represent propositions, evidence, limitations, lived experience, perspectives, resources, and questions without silently converting one category into another.

The system should be able to answer, for any substantive proposition:

- what exactly is being claimed?
- which object owns the claim?
- what evidence contribution supports, challenges, constrains, or fails to resolve it?
- what uncertainty remains?
- which independently reusable questions remain open?
- what source produced the relevant evidence contribution?

## 3. Claim ownership

### 3.1 Claims remain embedded, stable and addressable

A Claim remains a stable record owned by a parent object. It is not a standalone top-level object in v0.2.1.

The shared Claim record belongs in the common schema definitions so claim-bearing object types use one semantic contract.

Minimum Claim fields:

```yaml
id: stable-local-claim-id
text: exact proposition
confidence: high | moderate | low | contested | not_applicable
evidence_refs: []
uncertainty_ids: []
question_refs: []
```

A claim's confidence applies only to its exact wording and scope.

### 3.2 Initial claim-bearing object types

In v0.2.1, the following top-level object types may carry `claims`:

- Concept
- Resource

Concept claims cover propositions about concepts, definitions, associations, boundaries, prevalence, mechanisms, history, and other concept-scoped assertions where justified.

Resource claims cover propositions that must not be hidden inside descriptive text, including availability, accessibility, ownership, efficacy, safety, cost, eligibility, compatibility, or other materially testable assertions about a resource.

### 3.3 Non-claim-bearing object types in the initial implementation

The following do not gain a generic `claims` collection in the initial v0.2.1 implementation:

- Evidence
- Question
- Perspective
- Experience

This is deliberate.

Evidence objects contribute findings to claims rather than becoming claim containers themselves.

Question objects preserve inquiry targets rather than assert answers.

Perspective objects preserve identifiable positions without automatically converting those positions into factual propositions.

Experience objects preserve reported experience patterns without automatically turning frequency, interpretation, mechanism, diagnosis, or prevalence into claims.

A future schema may allow additional object types to carry claims only after a specific need is demonstrated and reviewed.

## 4. Claim references

### 4.1 Use structured references in schema data

The accepted implementation plan proposed a canonical string such as:

```text
autism#autism-claim-2
```

For the schema representation, v0.2.1 instead uses a structured Claim reference:

```yaml
object_id: autism
claim_id: autism-claim-2
```

This preserves every existing object ID and claim ID while avoiding parsing ambiguity and making validator expectations explicit.

A display/index layer may derive a compact string such as `autism#autism-claim-2`, but that string is not the authoritative stored representation.

### 4.2 Claim-reference validation

The validator must reject a Claim reference when:

- the parent object does not exist;
- the parent object is not a claim-bearing type;
- the claim ID does not exist inside the parent object;
- the reference resolves to a different object type than expected by a typed route;
- the object or claim identifier is blank or malformed.

## 5. Question and Uncertainty are different semantic mechanisms

### 5.1 Question object

A Question is a first-class, independently navigable knowledge target.

Examples:

- How can autistic burnout be distinguished from depression?
- Which sensory accommodations help which people, in which settings, and for which outcomes?
- Does a particular task-initiation strategy reduce cognitive burden or merely add another reminder system to manage?

A Question may be linked from multiple Concepts, Resources, Evidence Contributions, Experiences, or Perspectives.

It has its own lifecycle, provenance, current understanding, evidence-needed description, and reopening conditions.

### 5.2 Embedded Uncertainty record

An Uncertainty is a stable embedded epistemic limitation. It is not automatically a standalone Question.

Examples:

- the study used a small self-selected sample;
- the finding may not generalise outside the studied age group;
- measurement may not distinguish two competing mechanisms;
- the evidence supports a package but not the contribution of an individual component;
- the source does not establish prevalence.

Minimum Uncertainty fields:

```yaml
id: stable-local-uncertainty-id
text: explicit limitation or unknown
why_it_matters: consequence for interpretation
status: open | reduced | resolved | not_currently_resolvable
evidence_needed: optional description
```

Where resolution is recorded, the earlier uncertainty must remain inspectable rather than being deleted.

### 5.3 Where Uncertainties may live

The common Uncertainty record may be embedded in:

- a claim-bearing Concept;
- a claim-bearing Resource;
- an Evidence Contribution;
- a Relation where the uncertainty concerns the relationship itself.

Other uses require explicit review rather than automatic generalisation.

### 5.4 Promotion rule

An embedded Uncertainty may be promoted to a standalone Question only when the issue becomes independently useful, reusable, or genuinely researchable across objects.

Promotion must record an explicit mapping from the original uncertainty to the new Question object.

Promotion must not delete the original uncertainty record or rewrite its historical meaning.

### 5.5 Migration rule for v0.1 uncertainties

No v0.1 uncertainty is automatically promoted to a Question during migration.

Each existing uncertainty must be classified as one of:

- retained as an embedded uncertainty;
- promoted to a standalone Question with an explicit mapping;
- split into multiple records only through separately reviewed semantic change;
- unresolved mapping requiring owner review.

No item may disappear into an unclassified migration state.

## 6. Evidence object: source identity plus claim-specific contributions

### 6.1 Evidence object does not equal conclusion

An Evidence object represents an identifiable source together with the specific contributions that source makes to exact Oracle claims.

A whole paper, report, guideline, dataset, book, survey, historical record, or published lived-experience source must not be given one undifferentiated role such as "supportive" when different parts of it bear differently on different claims.

### 6.2 Source identity layer inside Evidence

Evidence object source-level fields should include at least:

```yaml
id: stable-evidence-id
type: evidence
title: ...
source_kind: ...
citation: ...
locators: ...
date: ...
accessed: ...
authorship: ...
methodology_summary: ...
status: ...
provenance: ...
contributions: ...
```

This source identity is not itself an evidential conclusion.

### 6.3 Evidence Contribution

Each Evidence object contains one or more claim-specific Evidence Contributions.

Minimum contribution fields:

```yaml
id: stable-local-contribution-id
claim_ref:
  object_id: autism
  claim_id: autism-claim-2
role: supportive
finding: exact bounded contribution relevant to this claim
population_or_context: ...
method_or_analysis_notes: ...
uncertainties: ...
```

Allowed initial evidence roles remain:

- compatible
- supportive
- discriminating
- contradictory
- falsifying
- inconclusive

Each role applies to the exact claim identified by `claim_ref`, not to the Evidence object globally.

### 6.4 Contribution explanation is mandatory

A bare role label is insufficient.

Every Evidence Contribution must state the bounded finding or observation that justifies the role assignment.

The system must preserve the distinction between:

- source existence;
- source result;
- evidence role relative to one exact claim;
- limitations on that contribution;
- the Oracle's eventual confidence in the claim.

### 6.5 One source may contribute differently to different claims

One Evidence object may contain multiple contributions, for example:

```yaml
contributions:
  - id: contribution-1
    claim_ref:
      object_id: concept-a
      claim_id: claim-1
    role: supportive
    finding: ...

  - id: contribution-2
    claim_ref:
      object_id: concept-b
      claim_id: claim-3
    role: inconclusive
    finding: ...
```

This is expected behaviour, not an exception.

### 6.6 Reciprocal evidence routing

A claim's `evidence_refs` identify Evidence objects that contain contributions about that exact claim.

The validator must require reciprocity:

- if a Claim references an Evidence object, that Evidence object must contain at least one Contribution targeting the exact Claim;
- if an Evidence Contribution targets a Claim, that Claim must reference the parent Evidence object.

This generalises the useful reciprocal source/claim integrity already enforced in v0.1.

## 7. Source locators

Evidence must not assume that every source is a webpage.

The `locators` structure should support typed locators including at least:

- HTTPS URL
- DOI
- ISBN
- archive identifier
- dataset/repository identifier
- explicit offline citation

A source may have more than one locator.

The validator should validate each locator according to its declared type.

The absence of an online URL must not make a legitimate offline or archival source invalid.

## 8. Resource claims remain separate from endorsement

Resource objects may carry claims because practical resource information often contains testable propositions.

Examples include:

- this service is available in a defined region;
- this app requires a subscription;
- this accommodation was studied for a defined outcome;
- this product contains a particular feature;
- this intervention has or lacks controlled evidence for a defined use.

The existence of a Resource object remains distinct from:

- efficacy;
- safety;
- recommendation;
- popularity;
- commercial claims;
- lived experience.

A Resource may therefore exist with no efficacy claim and no efficacy evidence.

Commercial ownership, sponsorship, affiliate relationships, declared conflicts, and other relevant interests remain separately representable.

## 9. Perspective boundary

A Perspective object records an identifiable position, framing, interpretation, or school of thought.

It may contain:

- who or what is represented;
- scope of representation;
- the position;
- reasoning;
- supporting material references;
- disagreements and competing perspectives;
- provenance.

It does not gain truth status because it is held by a professional body, institution, community, majority, expert, or lived-experience group.

If a Perspective contains a factual proposition that ND Oracle needs to evaluate as a factual claim, that proposition must be represented separately as a Claim in an appropriate claim-bearing object rather than being silently promoted from the Perspective text.

## 10. Experience boundary

An Experience object represents a published, aggregated, or otherwise appropriately sourced experience pattern.

It may record:

- description;
- contexts;
- who reports or is represented;
- variability;
- related concepts;
- evidence/source routes;
- related questions;
- provenance.

It does not automatically establish:

- diagnosis;
- mechanism;
- prevalence;
- causation;
- treatment efficacy;
- universality.

Contradictory and minority experiences must remain representable.

Report frequency must not be interpreted as prevalence without separate prevalence evidence.

## 11. Typed object references

### 11.1 Common Object reference

Generic cross-object references should use a typed structure where the target type is not already unambiguous from the containing field:

```yaml
object_id: sensory-overload
object_type: experience
```

The validator must confirm both the ID and declared type.

### 11.2 Type-specific references

Fields whose semantics already constrain the target type may use a narrower structure, for example:

```yaml
evidence_ref:
  object_id: evidence-123
```

or:

```yaml
question_ref:
  object_id: differential-question-1
```

The schema and validator must still enforce the expected target type.

### 11.3 No ambiguous generic ID bags

Fields such as `supporting_material_ids` should not remain untyped bags of arbitrary IDs when the system needs to know whether each target is Evidence, Perspective, Resource, Experience, Question, or another allowed type.

Use typed references or explicitly constrained reference fields instead.

## 12. Relation representation

The v0.2 richer Relation object remains accepted in principle but is repaired to use typed target references and local uncertainty records.

Recommended structure:

```yaml
type: associated_with
target_ref:
  object_id: sensory-processing
  object_type: concept
reason: "..."
confidence: moderate
evidence_refs:
  - object_id: evidence-id
question_refs:
  - object_id: question-id
uncertainties:
  - id: relation-uncertainty-1
    text: "..."
    why_it_matters: "..."
    status: open
```

Structural reciprocity remains required initially only for:

```text
broader_than <-> narrower_than
```

No other inverse rule should be invented without explicit semantic definition.

Causal relation terms remain excluded from the initial implementation until a separately reviewed evidential standard exists.

## 13. Schema naming repair

All type schema files participating in the overall object schema version `0.2` should be named consistently:

```text
schema/
├── object-v0.1.json
├── schema-v0.1.md
├── object-v0.2.json
├── schema-v0.2.md
├── common-v0.2.json
└── types/
    ├── concept-v0.2.json
    ├── evidence-v0.2.json
    ├── question-v0.2.json
    ├── resource-v0.2.json
    ├── perspective-v0.2.json
    └── experience-v0.2.json
```

Do not use filenames such as `evidence-v0.1.json` inside an object schema that declares `schema_version: "0.2"` unless a separate and explicit type-schema versioning mechanism is introduced later.

The initial implementation should have one unambiguous schema version meaning.

## 14. Revised v0.2 semantic graph

The repaired epistemic structure is:

```text
                    Question
                       ^
                       |
Concept / Resource -> Claim <- Evidence Contribution
       |               |              |
       |               v              v
       |          Uncertainty      Evidence source identity
       |
       +---- Relations / Experiences / Perspectives
```

More explicitly:

- Concepts and Resources may own Claims.
- Evidence objects identify sources.
- Evidence Contributions connect a source to an exact Claim with a bounded role and finding.
- Uncertainties remain attached to the exact epistemic location where the limitation applies.
- Questions are independently reusable inquiry targets.
- Experiences and Perspectives remain separate categories and do not become proof merely by being connected.

## 15. Migration consequences

The five current v0.1 concepts remain unchanged during schema implementation.

Later migration must preserve every existing:

- object ID;
- claim ID and exact text;
- claim confidence;
- source route;
- uncertainty route;
- perspective;
- relation;
- scope boundary;
- ecosystem entry point or explicit successor mapping;
- provenance and review state.

For each embedded v0.1 source, migration must explicitly determine whether it becomes an Evidence object and, if so, which claim-specific Evidence Contributions are created from its existing reciprocal support routes.

The migration must not infer new findings, stronger evidence roles, narrower populations, causal meaning, or additional conclusions merely because the structure is being normalised.

## 16. Fixture consequences

The later schema implementation should prove the repair with synthetic fixtures covering at least:

1. a Concept with a substantive Claim, embedded Uncertainty, Evidence route, and standalone Question route;
2. a Resource with a factual availability Claim but no efficacy claim;
3. an Evidence object with two Contributions carrying different roles for two exact Claims;
4. an Evidence Contribution with a local Uncertainty that is not promoted to a Question;
5. a Question referenced from multiple object types;
6. typed cross-object references that reject a correct ID paired with the wrong declared type;
7. reciprocal Claim/Evidence Contribution routing;
8. contradictory Experience objects that coexist without forced consensus;
9. a Perspective whose factual assertion is not silently treated as an evaluated Claim;
10. a non-URL Evidence locator.

## 17. Required negative tests after repair

The implementation must reject at least:

- an Evidence role applied globally without an exact Claim reference;
- an Evidence Contribution targeting a missing Claim;
- a Claim referencing Evidence that lacks a reciprocal Contribution;
- an Evidence Contribution targeting a Claim that does not reciprocally reference the Evidence object;
- a Resource efficacy statement hidden in an untracked field instead of a Claim where the schema requires explicit assertion tracking;
- promotion of an embedded Uncertainty to a Question without an explicit mapping in migration proof;
- a typed object reference whose declared type does not match the target object;
- a Perspective or Experience object carrying an undeclared generic `claims` collection in the initial v0.2.1 implementation;
- ambiguous untyped supporting-material references where the schema requires typed targets;
- type-schema filenames or dispatcher references that mix v0.1 and v0.2 version semantics without an explicit versioning mechanism.

## 18. Decisions explicitly deferred

This repair does not decide:

- whether Claims should ever become standalone objects;
- whether Source should ever become a standalone object separate from Evidence;
- public contribution/testimony storage;
- personal-data consent and withdrawal workflows;
- final causal relation vocabulary;
- database or graph-database technology;
- search index design;
- AI retrieval or generation;
- public UI behaviour;
- migration of any authoritative knowledge object.

Those remain downstream decisions.

## 19. Acceptance criteria

This semantic repair is ready to govern schema implementation only if review confirms:

- the six accepted top-level object types remain intact;
- claims have explicit ownership and one shared record contract;
- only Concept and Resource are initial claim-bearing types;
- Questions and embedded Uncertainties are structurally distinct;
- v0.1 uncertainties are not automatically promoted;
- Evidence source identity is separated from claim-specific Evidence Contributions;
- evidence roles attach to exact Claims rather than whole sources;
- Claim/Evidence Contribution routing is reciprocal;
- typed references prevent ambiguous cross-object IDs;
- schema version naming has one clear meaning;
- no repair weakens provenance, uncertainty, population/context, dissent, or migration-preservation requirements;
- no authoritative knowledge content changes as part of adopting the repair.

## 20. Next protected boundary

If this repair is accepted, the next lane is to revise the v0.2 schema implementation plan to incorporate these decisions and then implement schemas, validator compatibility, fixtures, and regression tests in a separately reviewable candidate.

Acceptance of this document alone does not authorise migration of authoritative knowledge objects or creation of new authoritative ND content.
