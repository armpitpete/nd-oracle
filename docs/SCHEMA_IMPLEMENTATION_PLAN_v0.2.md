# ND Oracle Schema Implementation Plan v0.2

Status: revised implementation plan aligned with `docs/KNOWLEDGE_MODEL_SEMANTIC_REPAIR_v0.2.1.md`. This document does not itself authorise schema mutation, validator changes, migration of existing authoritative knowledge objects, creation of new authoritative knowledge content, website/search/AI work, or deployment.

## 1. Purpose

Translate the accepted ND Oracle Knowledge Object Model v0.2, as clarified by the semantic repair v0.2.1, into an implementable schema and validation plan without losing any v0.1 knowledge, provenance, uncertainty, evidential meaning, population/context scope, or dissent.

The implementation remains deliberately staged:

1. schema definition;
2. validator compatibility;
3. fixture-based proof;
4. deterministic migration proof;
5. later migration of authoritative objects under a separate protected gate.

The five existing v0.1 concepts remain authoritative and unchanged until a separately reviewed migration candidate is accepted.

## 2. Governing invariants

Implementation must preserve these invariants:

- v0.1 objects continue to validate during the transition;
- no existing object ID changes silently;
- no existing claim ID or exact claim wording changes as a side effect of migration;
- no evidence route, uncertainty route, perspective, population, context, dissent, review state, or provenance is lost;
- experience is not converted into proof of diagnosis, mechanism, prevalence, causation, or efficacy;
- perspective is not converted into fact;
- resource existence, popularity, or availability is not converted into efficacy or endorsement;
- guidance is not converted into demonstrated efficacy;
- evidence merely compatible with a theory or claim is not represented as uniquely supportive;
- a source is not treated as a conclusion;
- relations do not imply unsupported causation;
- local uncertainty is preserved even when it does not justify a standalone Question object;
- unresolved Questions remain inspectable and reopenable;
- every typed cross-object reference resolves deterministically;
- schema implementation does not create new authoritative ND knowledge merely to exercise code paths.

## 3. Compatibility strategy

Use an additive transition rather than a big-bang migration.

During the compatibility phase the repository validator accepts both:

- `schema_version: "0.1"` concept objects under the existing v0.1 schema; and
- `schema_version: "0.2"` objects under the new multi-object dispatcher.

The five current concepts remain v0.1 initially. New v0.2 structures are proven with explicitly non-authoritative test fixtures.

Only after the v0.2 schema and validator survive positive, negative, cross-reference, and migration-regression tests should a separate migration proposal convert any authoritative concept.

## 4. Authoritative v0.2 top-level object types

The accepted six top-level object types remain:

- Concept
- Evidence
- Question
- Resource
- Perspective
- Experience

There is no standalone Claim object in v0.2 and no standalone Source object in v0.2.

Two important embedded epistemic record types are nevertheless first-class within the schema:

- **Claim record** — a stable, addressable proposition owned by a permitted parent object;
- **Uncertainty record** — a stable local limitation, ambiguity, unknown, boundary, or unresolved dependency attached to a claim, relation, evidence contribution, or other permitted parent record.

Evidence objects also contain one or more **Evidence Contribution records**, each of which describes what the identified source contributes to one exact claim.

## 5. Proposed schema file layout

```text
schema/
├── object-v0.1.json                 # unchanged compatibility schema
├── schema-v0.1.md                   # unchanged historical contract
├── object-v0.2.json                 # top-level v0.2 dispatcher
├── schema-v0.2.md                   # human-readable v0.2 contract
├── common-v0.2.json                 # shared envelope + record definitions
└── types/
    ├── concept-v0.2.json
    ├── evidence-v0.2.json
    ├── question-v0.2.json
    ├── resource-v0.2.json
    ├── perspective-v0.2.json
    └── experience-v0.2.json
```

All files participating in the v0.2 object system use `v0.2` naming. Do not introduce a second implicit type-schema version unless a future design explicitly requires it.

`object-v0.2.json` dispatches deterministically by `type` using JSON Schema 2020-12 `oneOf` or an equivalent fail-closed discriminator.

## 6. Shared object envelope

Every v0.2 top-level object shares a deliberately small common envelope:

```yaml
schema_version: "0.2"
id: stable-lowercase-id
type: concept | evidence | question | resource | perspective | experience
status: ...
provenance: ...
```

Shared definitions in `common-v0.2.json` should include:

- stable object identifier;
- stable local record identifier;
- non-blank text;
- ISO dates where applicable;
- lifecycle/review state;
- provenance;
- confidence vocabulary;
- canonical claim reference;
- typed object reference;
- Claim record;
- Uncertainty record;
- Evidence Contribution record;
- relation representation.

The common layer must not become a universal oversized envelope. Type-specific meaning stays in the type schemas.

## 7. Claim model

Claims remain embedded but are stable and addressable.

### 7.1 Claim ownership

For v0.2, the initial permitted claim-owning top-level types are:

- **Concept**
- **Resource**

This is intentionally conservative. Evidence objects contribute to claims rather than becoming general claim containers. Questions express inquiry targets. Perspectives express attributed positions. Experiences represent reported experiential patterns. If later evidence shows that another object type needs its own substantive claim collection, that is a separately reviewed schema extension.

### 7.2 Shared Claim record

A shared Claim record should require at least:

```yaml
id: local-stable-id
text: exact proposition
confidence: high | moderate | low | contested | not_applicable
evidence_ids:
  - evidence-id
uncertainties:
  - id: local-uncertainty-id
    statement: ...
    why_it_matters: ...
    reopening_or_reduction_condition: ...
question_ids:
  - question-id
```

The exact field names may be refined during schema coding, but these semantic requirements are fixed:

- claim identity is stable within its owning object;
- confidence belongs to the exact proposition and scope, not to the whole object;
- evidence routes identify Evidence objects;
- uncertainty remains available even when no standalone Question exists;
- a claim may also route to standalone Questions where an uncertainty is independently reusable or researchable.

### 7.3 Canonical claim references

Cross-object references to claims use:

```text
<object-id>#<claim-id>
```

Example:

```text
autism#autism-claim-2
```

The validator rejects:

- malformed canonical claim references;
- references to missing objects;
- references to missing claim IDs inside an existing object;
- references to an object type that is not permitted to own claims;
- ambiguous duplicate local claim IDs within the same object.

A future schema may promote Claims to standalone objects only if real reuse patterns justify it.

## 8. Uncertainty and Question are distinct

The schema must preserve a structural distinction between **local Uncertainty records** and **standalone Question objects**.

### 8.1 Uncertainty record

An Uncertainty record represents a known limitation, unknown, ambiguity, scope boundary, measurement problem, transfer problem, missing comparison, or other unresolved issue local to a specific epistemic record.

It may be embedded in:

- a Claim record;
- an Evidence Contribution record;
- a relation record;
- another schema location explicitly approved during implementation.

A local uncertainty must have a stable local ID and enough information to preserve why it matters and what evidence or condition could reduce, resolve, or reopen it.

Example:

```yaml
id: small-self-selected-sample
statement: "The sample is small and self-selected."
why_it_matters: "Transfer to the wider population is uncertain."
reopening_or_reduction_condition: "Larger representative replication."
```

### 8.2 Question object

A Question object is independently useful, navigable, reusable, or researchable across one or more objects.

Minimum semantic fields:

- `id`
- `type: question`
- `question`
- `status`
- `why_it_matters`
- typed `related_objects`
- `current_understanding`
- `evidence_needed`
- `reopening_conditions`
- `provenance`

Allowed initial statuses:

- `open`
- `partially_resolved`
- `resolved`
- `not_currently_answerable`

Resolution must preserve the prior uncertainty route, evidential basis, dissent where relevant, and reopening conditions.

### 8.3 Promotion rule

No migration or validator logic may automatically convert every v0.1 uncertainty into a Question.

Promotion to a standalone Question requires an explicit mapping because the uncertainty is independently useful, reusable, or genuinely researchable across objects.

Otherwise it remains a local Uncertainty record.

## 9. Concept schema v0.2

Required conceptual fields from the accepted model:

- `id`
- `type: concept`
- `name`
- `aliases`
- `status`
- `summary`
- `scope`
- `claims`
- `relations`
- `question_ids`
- `provenance`

Claims use the shared Claim record.

Concept scope must continue to state what the concept includes and excludes where relevant. A Concept is not automatically a diagnosis, theory, experience, resource, or intervention.

Migration of embedded v0.1 sources, uncertainties, and perspectives is deferred. The implementation must support lossless migration proof before any authoritative concept is rewritten.

## 10. Evidence schema v0.2

An Evidence object represents an identifiable source plus one or more claim-specific Evidence Contributions. It does not equate the source with its evidential force.

### 10.1 Source identity fields

Minimum source-identity fields:

- `id`
- `type: evidence`
- `title`
- `source_kind`
- `citation`
- `locator`
- `date`
- `accessed`
- `authorship`
- `status`
- `provenance`

Source identity may also include declared conflicts or funding where relevant.

### 10.2 Evidence Contributions

Each Evidence object contains one or more contribution records. A contribution must identify the exact claim it bears on.

Minimum semantic structure:

```yaml
contributions:
  - id: contribution-local-id
    claim_ref: object-id#claim-id
    role: supportive
    finding: "..."
    population_or_context: "..."
    methodology: "..."
    limitations:
      - id: limitation-id
        statement: "..."
        why_it_matters: "..."
        reopening_or_reduction_condition: "..."
```

Evidence-role vocabulary is bounded to:

- `compatible`
- `supportive`
- `discriminating`
- `contradictory`
- `falsifying`
- `inconclusive`

A contribution requires an explanation/finding; a bare role label is insufficient.

The same Evidence object may carry different roles for different claims, and multiple contributions for the same claim where results/populations/methods differ.

### 10.3 Evidence boundaries

The validator and schema must preserve these distinctions:

- source identity != evidential force;
- recommendation != demonstrated efficacy;
- mixed-population evidence remains mixed unless an explicit generalisation assessment exists;
- package evidence does not silently become component evidence;
- group-level result does not automatically become an individual-level conclusion;
- compatible evidence is not automatically discriminating evidence.

### 10.4 Source locators

Do not repeat the v0.1 restriction that every source requires an HTTPS URL.

Typed locators may include:

- HTTPS URL;
- DOI;
- ISBN;
- archive identifier;
- repository or dataset identifier;
- explicit offline citation where no online locator exists.

The validator checks the declared locator type rather than assuming every source is a webpage.

## 11. Resource schema v0.2

A Resource represents something people may use or access. It may own substantive claims because statements about availability, function, efficacy, safety, cost, or access can require evidence and uncertainty routes.

Minimum fields:

- `id`
- `type: resource`
- `name`
- `category`
- `description`
- `intended_use`
- `audience_or_context`
- typed `related_objects`
- `claims`
- `experience_ids`
- `limitations`
- `cost_or_access_notes`
- `conflicts_of_interest`
- `status`
- `provenance`

Initial categories may include:

- tool;
- app;
- game;
- book;
- media;
- service;
- accommodation;
- organisation;
- community;
- practical guide;
- product;
- education/work resource;
- other.

Resource categories describe what something is, not whether it works.

A Resource may validly have no efficacy claim. Its existence must not require efficacy evidence.

Commercial ownership, sponsorship, affiliate relationships, author conflicts, or other relevant interests must remain separately representable from claim evidence.

## 12. Perspective schema v0.2

A Perspective represents an attributed viewpoint, interpretation, framing, or position. It is not a generic factual claim container in v0.2.

Minimum fields:

- `id`
- `type: perspective`
- `held_by`
- `position`
- `reasoning`
- typed `supporting_material_refs`
- typed `disagreement_refs`
- `scope`
- `status`
- `provenance`

`held_by` must support bounded representation of whose position is being described without implying that every member of a group or institution holds it.

Evidence may be cited as material used by or relevant to a Perspective, but citation does not convert the Perspective into demonstrated fact.

If the system needs to assess a factual proposition contained within a Perspective, that proposition must be represented through a permitted Claim-owning object rather than inferred from the Perspective object itself.

## 13. Experience schema v0.2

An Experience represents a reported human experiential pattern, not a diagnostic, causal, prevalence, or efficacy conclusion.

Minimum fields:

- `id`
- `type: experience`
- `name`
- `description`
- `contexts`
- `reported_by`
- `variability`
- typed `related_objects`
- `evidence_ids`
- `question_ids`
- `status`
- `provenance`

The initial schema should support aggregated or published experience descriptions without requiring personally identifying testimony.

Public-contribution consent, withdrawal, privacy, and testimony-level identity rules remain deferred.

Frequency of reports must not be interpreted as prevalence unless prevalence is represented as a separate evidenced claim elsewhere.

Contradictory and minority experiences must remain representable without forcing synthetic consensus.

## 14. Typed cross-object references

Important cross-object references must declare or structurally constrain the expected target type rather than relying on unqualified ID arrays.

A generic typed reference may use a structure such as:

```yaml
- type: concept
  id: sensory-processing
```

or a field whose schema itself constrains target type, such as `evidence_ids` or `question_ids`.

The validator must reject:

- missing target objects;
- target objects of the wrong type;
- ambiguous untyped references in fields that require a semantic target type.

Canonical claim references remain a special typed reference because they point to a local claim inside a permitted parent object.

## 15. Relationship representation

Replace the v0.1 minimal relation structure with a richer v0.2 relation record.

Minimum semantic form:

```yaml
type: associated_with
target:
  type: concept
  id: sensory-processing
reason: "..."
confidence: moderate
evidence_ids:
  - evidence-id
uncertainties:
  - id: relation-uncertainty-id
    statement: "..."
    why_it_matters: "..."
    reopening_or_reduction_condition: "..."
question_ids:
  - question-id
```

Initial vocabulary:

Structural/navigation:

- `broader_than`
- `narrower_than`

Descriptive/evidential:

- `associated_with`
- `experienced_as`
- `supported_by`
- `challenged_by`
- `described_by`
- `used_for`
- `debated_by`
- `questions`

Do not add open-ended causal terms in the initial implementation.

If causal relationships are later required, they need a separately accepted evidential standard and relation contract.

### Reciprocity

The validator distinguishes:

- relationships requiring an inverse pair;
- relationships that may have an inverse but do not require one;
- directional relationships that must not be mechanically mirrored.

Initially:

```text
broader_than <-> narrower_than
```

must be reciprocal.

No other inverse rule is invented without explicit semantic definition.

## 16. Validator architecture

Refactor `scripts/validate.py` from a single-schema v0.1 validator into a version-dispatch validator.

Suggested flow:

```text
load authoritative JSON objects + explicit test fixtures in test context
       |
validate common file/JSON integrity
       |
read schema_version
       |
0.1 ---------------------- 0.2
 |                          |
existing schema          v0.2 dispatcher
 |                          |
existing semantic        type-specific semantic
checks                    checks
       \                    /
        repository-wide reference/graph checks
```

The validator must fail closed on unknown schema versions and unknown object types.

Test fixtures must never be included in the authoritative object count or treated as publishable knowledge.

## 17. Repository-wide semantic checks

JSON Schema alone is insufficient. Python validation should enforce at least:

- globally unique top-level object IDs;
- filename matches object ID;
- object path/type consistency;
- permitted claim ownership by object type;
- unique local claim IDs within a claim-owning object;
- canonical claim reference resolution;
- Evidence Contribution -> claim resolution;
- bounded evidence-role vocabulary;
- evidence contribution explanation/finding present;
- question reference resolution;
- evidence reference resolution;
- typed experience/resource/perspective/concept reference resolution;
- structural relation reciprocity where required;
- no dangling relation targets;
- no duplicate local IDs where the schema defines stable embedded records;
- non-blank required descriptive content;
- valid dates;
- typed locator validation;
- commercial/conflict data rules where relevant;
- preservation of existing v0.1 reciprocal claim/source and perspective/source rules;
- migration compatibility invariants.

## 18. Object directory layout

The eventual authoritative layout is:

```text
objects/
├── concepts/
├── evidence/
├── questions/
├── resources/
├── perspectives/
└── experiences/
```

During schema implementation, do not populate the five new authoritative directories with new ND content merely to exercise validation.

Use test fixtures instead.

## 19. Fixture strategy

Create clearly non-authoritative fixtures under:

```text
tests/fixtures/v0.2/
├── concepts/
├── evidence/
├── questions/
├── resources/
├── perspectives/
└── experiences/
```

Fixtures should be synthetic or explicitly labelled test-only so they cannot be mistaken for accepted ND knowledge.

A minimal valid fixture graph should exercise all six top-level object types plus embedded Claim, Uncertainty, Evidence Contribution, typed reference, and relation records.

## 20. Required positive tests

The implementation PR should prove at least:

1. all five existing v0.1 concepts still validate unchanged;
2. one valid fixture of each v0.2 top-level type validates;
3. a v0.2 Concept can own a claim with exact evidence and uncertainty routes;
4. a v0.2 Resource can own an availability/function/efficacy claim without conflating resource existence with efficacy;
5. a Resource can validly exist with no efficacy claim;
6. an Evidence object can contain multiple claim-specific Contributions;
7. one Evidence object can be supportive for one exact claim and inconclusive or contradictory for another;
8. an Evidence Contribution can retain its own population/context, methodology, finding, and limitations;
9. a local Uncertainty can exist without becoming a Question;
10. a standalone Question can link across more than one object;
11. a resolved Question can preserve reopening conditions;
12. structural inverse relations validate when reciprocal;
13. contradictory Experience fixtures can coexist;
14. a Perspective remains representable without being treated as fact;
15. non-URL evidence locators validate when correctly typed;
16. typed references resolve only to permitted target types.

## 21. Required negative tests

The implementation PR should reject at least:

- unknown schema version;
- unknown object type;
- duplicate global object ID;
- filename/object-ID mismatch;
- object stored in the wrong type directory;
- Claim collection on an object type not permitted to own claims;
- duplicate local claim ID within one object;
- malformed canonical claim reference;
- claim reference to a missing object;
- claim reference to a missing claim;
- claim reference to an object type that cannot own claims;
- missing Evidence object referenced by a claim;
- Evidence Contribution attached to a nonexistent claim;
- invalid evidence role;
- bare evidence role with no contribution finding/explanation;
- missing population/context where required for an empirical contribution;
- missing Question referenced by an object;
- local Uncertainty silently coerced into a Question-shaped record;
- typed reference resolving to the wrong target type;
- `broader_than` without reciprocal `narrower_than`;
- dangling relation target;
- blank required descriptive content;
- invalid dates;
- invalid typed locator;
- commercial/conflict data violating declared rules;
- migration fixture that loses a v0.1 claim, source route, uncertainty route, perspective, scope distinction, or provenance field.

## 22. Migration proof for the five v0.1 concepts

Migration remains a later, separate lane.

Before modifying authoritative concept files, build a deterministic migration proof comparing each v0.1 object with its proposed v0.2 representation.

For each object, prove preservation of:

- object ID;
- aliases;
- summary and scope;
- every claim ID and exact claim text;
- claim confidence;
- every source route;
- every uncertainty route;
- perspectives;
- relations;
- ecosystem entry points or their explicit successor mapping;
- provenance;
- review state.

The migration report must classify every relevant v0.1 element as one of:

- preserved verbatim;
- structurally normalised without semantic change;
- mapped into an Evidence object plus one or more Evidence Contributions;
- retained as a local Uncertainty record;
- explicitly promoted to a standalone Question;
- intentionally retained embedded;
- unresolved mapping requiring owner review.

No migration proceeds if any item falls into an unclassified loss state.

## 23. Migration ordering

Recommended later sequence:

1. implement schemas and validator with fixtures only;
2. validate unchanged v0.1 repository and v0.2 fixtures together;
3. produce a deterministic migration proof for one existing concept without changing the authoritative file;
4. compare old and proposed representations mechanically and editorially;
5. stop for owner acceptance of that one-concept migration candidate;
6. only after successful acceptance, consider the remaining four concepts as a bounded batch;
7. only after the migration model is proven should new authoritative v0.2 knowledge objects be admitted.

Schema design, migration mechanics, and content revision must not be mixed into one review.

## 24. Existing v0.1 behaviours that remain protected

Current validation already enforces useful invariants that must not regress:

- non-empty stable identifiers;
- no extra untracked top-level properties under v0.1;
- valid provenance dates;
- commercial source conflict records;
- reciprocal claim/source mappings;
- reciprocal perspective/source mappings;
- no cross-category local-ID collisions within a v0.1 concept;
- no dangling relations;
- filename/object-ID agreement;
- no duplicate object IDs across the repository.

The v0.2 implementation may generalise these checks but must not silently weaken them.

## 25. Implementation PR scope

The bounded schema implementation PR may include only:

- `schema/object-v0.2.json`;
- `schema/schema-v0.2.md`;
- `schema/common-v0.2.json`;
- six `schema/types/*-v0.2.json` files;
- validator changes required for version dispatch and cross-object semantic checks;
- explicit v0.2 test fixtures;
- regression tests proving v0.1 compatibility and v0.2 rules;
- documentation needed to explain the validator contract.

It must not include:

- migration of the five authoritative concepts;
- new authoritative neurodiversity knowledge content;
- edits to claim wording in existing concepts;
- promotion of existing uncertainties into Questions without a separately reviewed mapping;
- search indexing;
- database selection or migration;
- graph database work;
- website rendering changes;
- AI retrieval or response generation;
- public contribution workflows;
- deployment or DNS changes.

## 26. Acceptance criteria for schema implementation

The implementation candidate is ready for review only if:

- every schema is valid JSON Schema 2020-12;
- the top-level dispatcher fails closed on unknown versions/types;
- the five current v0.1 objects validate unchanged;
- all positive fixture tests pass;
- all required negative tests fail for the intended reason;
- claim ownership is enforced;
- Evidence source identity is structurally separated from Evidence Contributions;
- Evidence Contributions route to exact claims;
- local Uncertainty is structurally distinct from standalone Question;
- typed references resolve to the expected target type;
- structural inverse rules are enforced without inventing unsupported inverses;
- migration-loss regression tests exist before any authoritative migration begins;
- no authoritative ND content is added or altered.

## 27. Protected boundary after implementation

A successful schema + validator + fixture implementation does **not** authorise migration of authoritative knowledge.

The next protected lane after implementation is:

> deterministic migration proof for one existing v0.1 concept, with no authoritative mutation until the proof and proposed mapping are separately reviewed and accepted.
