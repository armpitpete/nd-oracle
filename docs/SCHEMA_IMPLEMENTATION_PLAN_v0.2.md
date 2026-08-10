# ND Oracle Schema Implementation Plan v0.2

Status: proposed implementation plan only. This document does not itself authorise schema mutation, validator changes, migration of existing knowledge objects, creation of new knowledge objects, website/search/AI work, or deployment.

## 1. Purpose

Translate the accepted `docs/KNOWLEDGE_OBJECT_MODEL_v0.2.md` into an implementable schema and validation plan without losing any v0.1 knowledge, provenance, uncertainty, or evidential meaning.

The plan deliberately separates four stages:

1. schema definition;
2. validator compatibility;
3. fixture-based proof;
4. later migration of authoritative objects.

The existing five v0.1 concepts remain authoritative and unchanged until a separately reviewed migration candidate is accepted.

## 2. Governing constraints

Implementation must preserve these invariants:

- v0.1 objects continue to validate during the transition;
- no existing object ID changes silently;
- no existing claim wording changes as a side effect of migration;
- no evidence, uncertainty, perspective, population, context, or provenance is lost;
- experience is not converted into proof;
- perspective is not converted into fact;
- resource existence is not converted into efficacy or endorsement;
- guidance is not converted into demonstrated efficacy;
- evidence merely compatible with a theory or claim is not represented as uniquely supportive;
- relations do not imply unsupported causation;
- unresolved questions remain inspectable and reopenable;
- every cross-object reference must resolve deterministically.

## 3. Compatibility strategy

Use an additive transition rather than a big-bang migration.

During the compatibility phase the repository validator should accept both:

- `schema_version: "0.1"` concept objects under the existing v0.1 schema; and
- `schema_version: "0.2"` objects under the new multi-object dispatcher.

The five current concepts should remain v0.1 initially. New v0.2 structures should first be proven with test fixtures, not authoritative content.

Only after the v0.2 schema and validator survive regression testing should a separate migration proposal convert the five concepts.

## 4. Proposed schema file layout

```text
schema/
├── object-v0.1.json                 # unchanged compatibility schema
├── schema-v0.1.md                   # unchanged historical contract
├── object-v0.2.json                 # top-level v0.2 dispatcher
├── schema-v0.2.md                   # human-readable v0.2 contract
├── common-v0.2.json                 # shared definitions
└── types/
    ├── concept-v0.2.json
    ├── evidence-v0.1.json
    ├── question-v0.1.json
    ├── resource-v0.1.json
    ├── perspective-v0.1.json
    └── experience-v0.1.json
```

The type files use their own initial type versions while participating in the overall ND Oracle object schema version `0.2`.

The top-level `object-v0.2.json` should dispatch by `type` using JSON Schema 2020-12 `oneOf` or an equivalent deterministic discriminator.

## 5. Shared object envelope

Every v0.2 object should share a minimal common envelope:

```yaml
schema_version: "0.2"
id: stable-lowercase-id
type: concept | evidence | question | resource | perspective | experience
status: ...
provenance: ...
```

Shared definitions should include:

- stable object identifier;
- non-blank text;
- ISO dates where applicable;
- lifecycle/review state;
- provenance;
- confidence vocabulary;
- typed object references;
- claim references;
- relation representation.

The common layer should remain deliberately small. Type-specific meaning belongs in the type schemas rather than a universal oversized envelope.

## 6. Claim identity and cross-object references

Claims remain stable, addressable entities but do not become a seventh standalone object type in v0.2.

Existing v0.1 claim IDs are local to their parent concept. Cross-object evidence therefore needs an unambiguous canonical reference without forcing a claim-ID rewrite.

Recommended canonical representation:

```text
<object-id>#<claim-id>
```

Example:

```text
autism#autism-claim-2
```

This preserves the existing claim IDs while making cross-object references deterministic.

The validator should reject:

- malformed claim references;
- references to missing objects;
- references to missing claims inside an existing object;
- references to objects that cannot carry the referenced claim.

A future schema may promote claims to standalone objects if real reuse patterns justify it. v0.2 should not do that pre-emptively.

## 7. Concept schema v0.2

The concept schema should preserve the semantic content of v0.1 while replacing embedded material only where standalone object references are appropriate.

Required conceptual fields from the accepted model:

- `id`
- `type`
- `name`
- `aliases`
- `status`
- `summary`
- `scope`
- `claims`
- `relations`
- `question_ids`
- `provenance`

### Claim requirements

Each substantive claim should retain:

- stable local `id`;
- exact claim text;
- local confidence;
- evidence routes;
- uncertainty/question routes.

The schema must not treat confidence as a property of the whole concept.

### Embedded legacy data

The first v0.2 implementation should not automatically delete embedded v0.1 `sources`, `uncertainties`, or `perspectives` from migrated concepts.

A migration adapter may temporarily support explicit legacy-preservation fields or perform a reviewed one-to-one normalisation. The chosen method must be lossless and tested before authoritative migration.

## 8. Evidence schema v0.1

Evidence objects represent inspectable material, not truth statements.

Minimum fields:

- `id`
- `type: evidence`
- `title`
- `source_kind`
- `citation`
- `locator`
- `date`
- `accessed`
- `authorship`
- `methodology`
- `population_or_context`
- `findings`
- `limitations`
- `evidence_roles`
- `status`
- `provenance`

### Evidence roles

At claim level, allow only the accepted bounded vocabulary:

- `compatible`
- `supportive`
- `discriminating`
- `contradictory`
- `falsifying`
- `inconclusive`

Each role record should identify the exact canonical claim reference it applies to.

The schema should require role-specific explanation rather than allowing a bare role label to imply more than the source supports.

### Source locators

Do not repeat the v0.1 restriction that every source must have an HTTPS URL.

The locator model should permit appropriately typed identifiers such as:

- HTTPS URL;
- DOI;
- ISBN;
- archive identifier;
- repository/dataset identifier;
- explicit offline citation where no online locator exists.

The validator should validate the declared locator type rather than assuming every source is a webpage.

## 9. Question schema v0.1

Minimum fields:

- `id`
- `type: question`
- `question`
- `status`
- `why_it_matters`
- `related_object_ids`
- `current_understanding`
- `evidence_needed`
- `reopening_conditions`
- `provenance`

Allowed initial statuses:

- `open`
- `partially_resolved`
- `resolved`
- `not_currently_answerable`

### Question versus embedded uncertainty

Do not assume every v0.1 uncertainty becomes a standalone Question object.

Some uncertainties are local limitations on a specific claim. A standalone Question object should be created only when the uncertainty is independently useful, reusable, or genuinely researchable across objects.

Migration must record any promotion mapping explicitly.

Resolved questions must preserve prior uncertainty, the evidential route that justified resolution, and reopening conditions.

## 10. Resource schema v0.1

Minimum fields:

- `id`
- `type: resource`
- `name`
- `category`
- `description`
- `intended_use`
- `audience_or_context`
- `related_concept_ids`
- `evidence_ids`
- `experience_ids`
- `limitations`
- `cost_or_access_notes`
- `conflicts_of_interest`
- `status`
- `provenance`

Initial resource categories may include:

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

Categories describe what a resource is, not whether it works.

Commercial ownership, sponsorship, affiliate relationships, author conflicts, or other relevant interests must be representable separately from efficacy evidence.

## 11. Perspective schema v0.1

Minimum fields:

- `id`
- `type: perspective`
- `held_by`
- `position`
- `reasoning`
- `supporting_material_ids`
- `disagreement_ids`
- `scope`
- `status`
- `provenance`

The schema should support identifiable groups or institutions without implying that all members share a single view.

`held_by` should therefore permit a bounded description of representation and scope rather than merely a name string.

Perspective objects may cite evidence, but evidence citation does not convert the perspective itself into a factual conclusion.

## 12. Experience schema v0.1

Minimum fields:

- `id`
- `type: experience`
- `name`
- `description`
- `contexts`
- `reported_by`
- `variability`
- `related_concept_ids`
- `evidence_ids`
- `question_ids`
- `status`
- `provenance`

The initial schema should support aggregated or published experience descriptions without requiring storage of personally identifying testimony.

Public-contribution consent, withdrawal, privacy, and testimony-level identity rules remain deferred and must not be accidentally designed into this schema by storing unnecessary personal data.

Frequency of experience reports must not be interpreted as prevalence unless prevalence is supported by separate evidence.

Contradictory and minority experiences must remain representable.

## 13. Relationship representation

Replace the v0.1 minimal relation structure with a richer relation object for v0.2:

```yaml
type: associated_with
target_id: sensory-processing
reason: "..."
confidence: moderate
evidence_ids:
  - evidence-id
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

If causal relationships are needed later, they require a separately defined evidential standard and relation contract.

### Reciprocity

The validator should distinguish:

- relationships that require an inverse pair;
- relationships that may have an inverse but do not require one;
- directional relationships that must not be mechanically mirrored.

For the initial structural pair:

```text
broader_than <-> narrower_than
```

reciprocity should be enforced.

Other inverse rules should not be invented until their semantics are explicitly defined.

## 14. Validator architecture

Refactor `scripts/validate.py` from a single-schema v0.1 validator into a version-dispatch validator.

Suggested flow:

```text
load all JSON objects
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
        repository-wide graph/reference checks
```

The validator should fail closed on unknown schema versions and unknown object types.

## 15. Repository-wide semantic checks

JSON Schema alone is insufficient. The Python validator should enforce at least:

- globally unique object IDs;
- filename matches object ID;
- object path/type consistency;
- canonical claim reference resolution;
- cross-object evidence-role resolution;
- question reference resolution;
- evidence reference resolution;
- experience/resource/perspective reference resolution;
- required structural relation reciprocity;
- no dangling object relations;
- no duplicate IDs within an object where local IDs exist;
- evidence-role vocabulary enforcement;
- resource conflict fields where relevant;
- migration compatibility invariants.

## 16. Object directory layout

The eventual authoritative layout should be:

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

## 17. Fixture strategy

Create non-authoritative fixtures under a clearly separated test path, for example:

```text
tests/fixtures/v0.2/
├── concepts/
├── evidence/
├── questions/
├── resources/
├── perspectives/
└── experiences/
```

Fixtures should use synthetic or explicitly test-only content so schema implementation cannot be mistaken for accepted ND knowledge.

A minimal valid fixture set should exercise all six object types and their cross-references.

## 18. Required positive tests

The implementation PR should prove:

1. all existing five v0.1 concepts still validate unchanged;
2. one valid fixture of each v0.2 type validates;
3. a v0.2 concept can route an exact claim to evidence and a question;
4. an evidence object can carry different roles for different exact claims;
5. structural inverse relations validate when reciprocal;
6. a resource can exist with no efficacy evidence without being invalid;
7. contradictory experience fixtures can coexist;
8. a resolved question can preserve reopening conditions;
9. non-URL evidence locators can validate when correctly typed.

## 19. Required negative tests

The implementation PR should reject at least:

- unknown schema version;
- unknown object type;
- duplicate global object ID;
- filename/object-ID mismatch;
- object stored in the wrong type directory;
- malformed canonical claim reference;
- reference to missing claim;
- reference to missing evidence;
- reference to missing question;
- invalid evidence role;
- evidence role attached to a nonexistent claim;
- `broader_than` without reciprocal `narrower_than`;
- dangling relation target;
- blank required descriptive content;
- invalid dates;
- resource commercial/conflict data that violates the declared rules;
- migration fixture that loses a v0.1 claim, source route, uncertainty route, or provenance field.

## 20. Migration proof for the five v0.1 concepts

Migration must be a later, separate lane.

Before modifying authoritative concept files, build a deterministic migration proof that compares each v0.1 object with its proposed v0.2 representation.

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

The migration report should distinguish:

- preserved verbatim;
- structurally normalised without semantic change;
- intentionally promoted to standalone object;
- intentionally retained embedded;
- unresolved mapping requiring owner review.

No migration should proceed if any item falls into an unclassified loss state.

## 21. Migration ordering

Recommended later sequence:

1. implement schemas and validator with fixtures only;
2. validate unchanged v0.1 repository and v0.2 fixtures together;
3. produce migration candidate for one existing concept;
4. compare old and new representations mechanically and editorially;
5. if accepted, migrate the remaining four concepts in a bounded batch;
6. only then allow creation of new authoritative v0.2 knowledge objects.

This prevents schema design and content revision from being mixed into one review.

## 22. Existing v0.1 behaviours that must remain protected

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

## 23. Explicit non-goals for the implementation PR

The schema implementation PR must not include:

- migration of the five authoritative concepts;
- new neurodiversity knowledge content;
- search indexing;
- database selection or migration;
- graph database work;
- website or rendering changes;
- AI retrieval or generation;
- public contribution flows;
- deployment or DNS changes;
- analytics, accounts, forms, or personal-data collection.

## 24. Proposed implementation PR scope

A later schema implementation PR should be limited to approximately:

```text
schema/object-v0.2.json
schema/common-v0.2.json
schema/schema-v0.2.md
schema/types/*.json
scripts/validate.py
tests/test_validation.py
tests/fixtures/v0.2/**
CHANGELOG.md
```

Existing v0.1 schema files and authoritative knowledge objects should remain unchanged unless an unavoidable compatibility correction is separately identified and reviewed.

## 25. Acceptance test for schema implementation

The implementation is ready for protected merge review only if all of the following are true:

- existing v0.1 objects validate unchanged;
- every v0.2 object type has positive and negative fixtures;
- all cross-object references are deterministic and checked;
- exact claims can be addressed without rewriting existing claim IDs;
- evidence roles remain claim-specific;
- uncertainty/question routes remain inspectable;
- relationships cannot silently imply causation;
- migration loss tests pass;
- no authoritative object has yet been migrated;
- no downstream website/search/AI/deployment work is included.

## 26. Protected boundaries after this plan

Acceptance of this plan would authorise only a bounded schema implementation candidate matching the scope above.

It would not authorise:

- migration of authoritative v0.1 objects;
- creation of new authoritative knowledge objects;
- public release;
- search/database/UI/AI implementation;
- deployment.

Each remains a separate later gate.
