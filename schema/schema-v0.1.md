# Schema v0.1

## Unit of knowledge

An object is a stable, versioned node. v0.1 implements `concept`; the shared envelope is designed to support later `resource`, `evidence`, `uncertainty`, `perspective`, `organisation`, `community`, `service`, `accommodation`, `tool`, `game`, `app`, and `media` objects without forcing them into a clinical hierarchy.

Each concept contains:

- identity, aliases, lifecycle status, and timestamps;
- a concise definition and scope boundaries;
- claims with confidence, evidence routes, and uncertainty routes;
- sources with authorship, source kind, persistent locator, and access date;
- uncertainties with impact and the evidence that could reduce them;
- perspectives, including whose position is represented;
- typed links to other stable object IDs;
- practical entry points across the wider ecosystem;
- provenance for the object itself.

## Confidence vocabulary

- `high`: consistent, directly relevant support with important limits understood.
- `moderate`: useful support exists, but transfer, measurement, or coverage limits matter.
- `low`: preliminary, indirect, sparse, or substantially disputed support.
- `contested`: credible perspectives conflict or the framing itself is disputed.
- `not_applicable`: the statement is descriptive, administrative, or explicitly a perspective rather than an empirical conclusion.

Confidence is local to a claim's exact wording and scope.

## Evidence routes

Claims refer to source IDs rather than embedding citations. They also refer to uncertainty IDs. A validator rejects broken routes and serious claims without both routes. `none_identified` is allowed only as an explicit uncertainty record, so absence of a known limitation is itself visible and revisitable.

## Provenance

Every object records creator, creation method, creation date, and review state. Sources distinguish peer-reviewed research, authoritative guidance, community or lived-experience material, historical material, and other source kinds. v0.1 does not pretend these kinds are interchangeable.

## Deliberate limits

- The five seed nodes are not an ontology of people and do not define who is neurodivergent.
- Relations are useful navigation assertions, not causal claims.
- Practical entry points are categories to populate, not endorsements.
- Evidence items are embedded in concepts for v0.1; normalization into standalone evidence objects is deferred until real reuse patterns justify it.
- Uncertainty resolution history, translations, fine-grained claim authorship, and community review attestations need a later schema migration.
