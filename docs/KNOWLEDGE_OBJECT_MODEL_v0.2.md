# ND Oracle Knowledge Object Model v0.2

Status: proposed design contract. No schema migration is authorised by this document alone.

## 1. Purpose

ND Oracle v0.2 expands the current concept-only knowledge model into a multi-object system while preserving the project's epistemic rules: evidence must remain traceable, uncertainty must remain visible, lived experience must not be converted into proof, and resources must not be converted into endorsements.

The minimum object types are:

- Concept
- Evidence
- Question
- Resource
- Perspective
- Experience

The object model exists to answer a prior question before content is added: **what kind of thing is this information?**

## 2. Cross-object requirements

Every object must have:

- a stable lowercase hyphenated `id`;
- an explicit object `type`;
- lifecycle/review status;
- provenance sufficient to identify how the object was created and reviewed;
- version-safe references to other objects by stable IDs;
- no silent conversion of uncertainty into certainty;
- no unsupported causal language.

Where an object makes or carries a substantive claim, the route to evidence and uncertainty must remain recoverable.

## 3. Concept object

### Purpose

Represents a stable thing people may want to understand, such as autism, ADHD, masking, autistic burnout, executive function, or sensory processing.

### Required conceptual fields

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

### Boundary rules

A concept is not automatically a diagnosis, theory, experience, resource, or intervention. Scope must state both what the concept includes and excludes. Concept claims remain separately reviewable and must not inherit confidence merely from the concept's existence.

## 4. Evidence object

### Purpose

Represents material used to support, challenge, contextualise, or constrain claims. Examples include research papers, systematic reviews, authoritative guidance, historical documents, surveys, datasets, and community-generated evidence sources where appropriate.

### Required conceptual fields

- `id`
- `type`
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
- `provenance`

### Evidence-role vocabulary

Evidence may be marked, at claim level, as:

- `compatible`
- `supportive`
- `discriminating`
- `contradictory`
- `falsifying`
- `inconclusive`

Evidence merely compatible with a theory or claim must never be represented as uniquely supporting it.

### Boundary rules

A paper is not a conclusion. A recommendation is not demonstrated efficacy. Mixed-population evidence remains mixed unless an explicit generalisation assessment is recorded. Package evidence must not silently become component evidence.

## 5. Question object

### Purpose

Represents an unresolved question or uncertainty worth preserving so that later users do not have to rediscover it.

### Required conceptual fields

- `id`
- `type`
- `question`
- `status`
- `why_it_matters`
- `related_object_ids`
- `current_understanding`
- `evidence_needed`
- `reopening_conditions`
- `provenance`

### Status examples

- `open`
- `partially_resolved`
- `resolved`
- `not_currently_answerable`

### Boundary rules

A question may preserve multiple plausible answers. Resolution requires an inspectable evidential route and must not erase earlier uncertainty or dissent.

## 6. Resource object

### Purpose

Represents something people may use, including tools, apps, games, books, media, services, accommodations, organisations, or practical resources.

### Required conceptual fields

- `id`
- `type`
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
- `provenance`

### Boundary rules

Existence is not endorsement. Popularity is not efficacy. A commercial claim must remain distinguishable from independent evidence. Resource facts, efficacy claims, safety claims, and user experiences must not be collapsed into one statement.

## 7. Perspective object

### Purpose

Represents a viewpoint, interpretation, framing, or position held by an identifiable person, community, professional group, institution, or school of thought.

### Required conceptual fields

- `id`
- `type`
- `held_by`
- `position`
- `reasoning`
- `supporting_material_ids`
- `disagreement_ids`
- `scope`
- `provenance`

### Boundary rules

Institutional classification is not truth. Community usefulness is not diagnostic validation. Lived or professional authority does not remove the need to distinguish perspective from demonstrated factual claims.

## 8. Experience object

### Purpose

Represents a reported human experience or recurring experiential pattern, such as shutdown, sensory overload, masking fatigue, hyperfocus, or difficulty transitioning.

### Required conceptual fields

- `id`
- `type`
- `name`
- `description`
- `contexts`
- `reported_by`
- `variability`
- `related_concept_ids`
- `evidence_ids`
- `question_ids`
- `provenance`

### Boundary rules

Experience is evidence of experience, not automatic evidence of mechanism, diagnosis, prevalence, or treatment efficacy. The model must permit contradictory and minority experiences without forcing a synthetic consensus.

## 9. Relationship model

Relationships must state why two objects are connected. `related_to` must not become a catch-all substitute for modelling the actual relationship.

A future relation representation should support at least:

```yaml
relation:
  type: associated_with
  target_id: sensory-processing
  reason: "Sensory load may alter the context in which executive performance is observed."
  confidence: moderate
  evidence_ids:
    - evidence-id
  question_ids:
    - uncertainty-id
```

### Initial relationship vocabulary

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

Causal terms such as `causes`, `prevents`, `fixes`, or `proves` must not be used unless the evidential standard for that exact causal statement is explicitly satisfied.

Reciprocal relationships should either be encoded explicitly or generated under a documented deterministic rule. The system must not create inconsistent inverse relationships.

## 10. Migration principles from v0.1

The five existing concept objects are the migration test set.

Migration must:

1. preserve stable concept IDs;
2. preserve exact claim meaning unless a separately reviewed revision is accepted;
3. preserve source routes and uncertainty routes;
4. preserve provenance and review history;
5. avoid converting embedded sources, perspectives, or uncertainties into standalone objects unless identity and cross-reference mappings are explicit;
6. avoid information loss during normalisation;
7. preserve population, context, and scope distinctions;
8. preserve dissent and reopening conditions where present.

The governing migration test is:

> Can v0.2 represent everything already captured in v0.1 without losing provenance, scope, uncertainty, or evidential meaning?

If not, v0.2 is not ready for schema implementation.

## 11. Category-error examples

### Resource versus efficacy

Bad:

> Weighted blankets reduce autistic distress.

Better model:

- Resource: weighted blanket
- Evidence: studies evaluating defined outcomes in defined populations
- Experience: reports of benefit, neutrality, or discomfort
- Question: who benefits, under what conditions, and with what burdens or harms?

### Experience versus diagnosis

Bad:

> Difficulty starting tasks means ADHD.

Better model:

- Experience: difficulty initiating tasks
- Related concepts: executive function, ADHD, autism, fatigue, stress, environmental demand
- Question: which explanations fit this person and context?

### Recommendation versus evidence

Bad:

> A guideline recommends a sensory adaptation, therefore the adaptation is proven effective.

Better model:

- Evidence object records the guideline as guidance
- Separate evidence objects record controlled efficacy evidence where it exists
- Resource/intervention claims are bounded to the outcomes and populations actually studied

## 12. Acceptance criteria before schema implementation

The v0.2 design is ready for schema work only if review confirms:

- object boundaries are sufficiently clear;
- evidence is separate from conclusions;
- experience is separate from proof;
- perspectives are separate from factual claims;
- resources are separate from endorsements;
- questions/uncertainties remain first-class;
- relationships carry interpretable meaning;
- unsupported causation is not implied;
- existing v0.1 knowledge can migrate without information loss;
- population and context leakage is prevented;
- provenance remains recoverable across every migration.

## 13. Deferred decisions

This document deliberately does not specify:

- final JSON Schema syntax;
- database technology;
- search index design;
- graph database choice;
- UI rendering;
- AI retrieval or response generation;
- public contribution workflows;
- final relation vocabulary beyond the initial bounded set.

Those decisions belong downstream of acceptance of this knowledge model.
