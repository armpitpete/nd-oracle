# D1-D17 paired migration state normalization

Status: **non-authoritative normalization candidate; authoritative replacement remains unauthorised**.

Prepared against protected `main`:

`657e7f7f0093c6f8765f5955dab8357e4bc17f1d`

## Purpose

Fold the accepted D1-D17 decisions forward into one current Autism + Neurodiversity migration package instead of leaving later work to infer state from historical research files and pre-decision ledgers.

The historical partial paired builder remains available as the preservation/inventory stage. `scripts/build_normalized_paired_migration_candidate.py` is the normalized pipeline: it builds that package and then applies D1-D17 through `scripts/normalize_paired_migration_candidate.py`.

## Materialized candidate objects

The normalized package materializes nine schema-shaped v0.2 objects:

- Concept: `autism`
- Concept: `neurodiversity`
- Evidence: `autism-source-who`
- Evidence: `autism-source-neurobiology`
- Evidence: `neurodiversity-source-botha`
- Evidence: `neurodiversity-source-singer-2017-revised-print`
- Perspective: `autism-perspective-clinical`
- Perspective: `neurodiversity-perspective-collective`
- Perspective: `neurodiversity-perspective-paradigm`

The 2016 Singer Kindle identity is preserved separately rather than materialized as an invalid Evidence object while its required full date remains unresolved.

## Decisions folded forward

- D1 supplies the accepted future Autism neurobiology citation correction.
- D2 remains `legacy_retained_unmapped` for Autism `related_to` records.
- D4 remains `legacy_retained_unmapped` for Autism ecosystem entries.
- D7 supplies the accepted WHO Perspective framing.
- D8 supplies the accepted Botha citation correction.
- D9 and D10 supply the accepted Neurodiversity Perspective framing fields.
- D11 preserves distinct Singer 2016 and 2017 Evidence identities.
- D12 supplies the accepted 2017 full date.
- D13 and D14 preserve all four accepted edition-specific Singer Claim bindings.
- D15/D16 supply the lossless embedded-Uncertainty representation: legacy question text is retained as neutral `text`, reduction/reopening routes remain an ordered array, and lifecycle state remains explicit.
- D17 preserves the reciprocal Autism/Neurodiversity legacy relation records as `legacy_retained_unmapped` and emits no v0.2 taxonomy edge.

D3, D5 and D6 remain historical decisions whose earlier migration assumptions have been overtaken by D16/D17 where explicitly recorded; their records are not rewritten.

## Remaining blockers

Normalization reduces current unfinished work to two explicit blockers:

1. `singer-2016-full-date` — v0.2 Evidence requires a full date, but the 2016 Kindle day-level date remains unaccepted.
2. `dependency-neurodiversity-adhd` — the Neurodiversity↔ADHD legacy structural semantics require a separately reviewed disposition; D17 did not expand its authority to ADHD.

The package therefore remains `enrichment_pending`. It does not claim `candidate_complete`.

## Validation target

Regression tests require:

- the migration package itself to satisfy the migration contract;
- no stale `owner_decision_required` preservation disposition after D1-D17 normalization;
- exactly one pending enrichment: Singer 2016 full date;
- exactly one unresolved structural dependency: Neurodiversity↔ADHD;
- all nine materialized objects to pass v0.2 JSON Schema and semantic reference checks as an isolated non-authoritative candidate graph;
- D16 uncertainty arrays to remain ordered and lossless;
- D17 to emit no Autism↔Neurodiversity taxonomy edge;
- the anchored authoritative v0.1 Autism and Neurodiversity blobs to remain unchanged.

## Protected boundaries

This normalization does **not** authorise or perform:

- authoritative v0.1 mutation;
- authoritative v0.2 replacement;
- acceptance of a Singer 2016 full date;
- a Neurodiversity↔ADHD semantic disposition;
- ADHD migration-scope expansion;
- a new semantic relation or confidence value;
- publication or deployment.

The next substantive work after this normalization is reviewed evidence work on the Singer 2016 date, followed by the separately protected Neurodiversity↔ADHD semantic disposition.
