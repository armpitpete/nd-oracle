# Neurodiversity relation-semantics review

Status: non-authoritative research/proof only.

Prepared against protected `main` `52ef8fad6da75b8fa772a3bfabfe9d7a89c6981b` after PR #55 recorded the conclusion that relation semantics must be reviewed before structural confidence.

## Question

What does the legacy statement that Autism is "part of" or situated within neurodiversity actually mean for ND Oracle migration?

The authoritative v0.1 Autism relation is typed `narrower_than -> neurodiversity`, but its own note says:

> Autism is commonly situated within neurodiversity discourse.

The reciprocal Neurodiversity record is typed `broader_than -> autism`, while its note says:

> Autism is commonly discussed within the neurodiversity ecosystem.

ADHD has the same type/note pattern and is used here only as a consistency test.

## Current terminology check

The review checked current public terminology sources on 2026-08-11:

- National Autistic Society: neurodiversity describes diversity across all human brains; autism is described as a form of neurodivergence.
- NHS: autism is often called a type of neurodivergence.
- NHS England autism-informed care: neurodiversity is the diversity of all minds; neurodivergence encompasses autism and ADHD among other differences.
- NHS England independent ADHD Taskforce: neurodiversity describes the population as a whole; ADHD is discussed as neurodivergence outside clinical settings.

These sources support a distinction between **neurodiversity** (population-level diversity / a framing or paradigm) and **neurodivergence** (a descriptor that can include autism and ADHD). They do not cleanly support treating Autism or ADHD as literal taxonomic subtypes of the Neurodiversity concept.

## Option test

### 1. Keep `narrower_than / broader_than`

Rejected as a lossless migration disposition. It privileges the legacy type label over the explanatory note and hardens a discourse relationship into a current ontology claim.

### 2. Replace with `associated_with`

Safer than taxonomy, but still not lossless. It changes the legacy relation type and erases the specific discourse/ecosystem character of the note. It could be proposed later as enrichment, but should not be disguised as mechanical migration.

### 3. Add a new `situated_within_discourse` relation type

Not recommended at this stage. It would encode the wording more directly, but there is not yet evidence that a new schema relation type has enough reuse to justify expanding the common relation vocabulary.

### 4. Emit no direct v0.2 semantic edge and preserve the legacy unit

Recommended. Preserve the reciprocal original relation records together, including exact type, target and note, under an explicit `legacy_retained_unmapped` migration disposition. This loses nothing and invents nothing.

### 5. Add a new relation to the Neurodiversity Paradigm Perspective

Plausible future enrichment. A relation such as Autism `described_by` the Neurodiversity-Paradigm Perspective may represent the contemporary framing more precisely than a Concept-to-Concept taxonomy edge. But it would be a new evidence-backed semantic act and must not be represented as though it were the migrated legacy edge. Its evidence, target and confidence would require separate review.

## D5 and D6

D5 remains historical evidence that both sides of the reciprocal legacy pair must be handled together and neither may silently disappear. This review reopens only D5's assumption that preservation requires emitting a v0.2 reciprocal `broader_than/narrower_than` pair. The D5 record is not rewritten.

D6 also remains intact. If the legacy pair is retained unmapped instead of being emitted as a v0.2 relation, no confidence value is required for that migrated edge because there is no migrated v0.2 edge. Confidence returns as a live question only if a new relation is separately proposed.

## ADHD consistency test

ADHD shows the same mismatch: its v0.1 relation says `narrower_than -> neurodiversity`, while the note says ADHD is commonly situated within neurodiversity discourse. Current NHS England terminology describes ADHD as neurodivergence and neurodiversity as population-level diversity. This supports treating the issue as a general migration-semantic problem rather than an Autism-only anomaly.

This does **not** expand the current migration scope to ADHD.

## Recommended owner decision

Candidate: `nd-neurodiversity-legacy-structural-disposition`

Recommended acceptance:

> Accept the relation-semantics disposition: preserve the reciprocal Autism/Neurodiversity v0.1 broader_than/narrower_than records together as legacy-retained-unmapped for migration, and do not emit a v0.2 taxonomy edge from them. Preserve D5 and D6 as historical decisions; supersede only D5's mapping assumption, not its record or its requirement that neither side be silently dropped. Treat any future Autism-to-Neurodiversity-Paradigm relation as separately reviewed enrichment. ADHD remains a consistency test only.

This decision would **not** authorise paired-candidate mutation, schema/validator change, a replacement relation, relation confidence, authoritative migration, ADHD expansion, publication, or deployment.
