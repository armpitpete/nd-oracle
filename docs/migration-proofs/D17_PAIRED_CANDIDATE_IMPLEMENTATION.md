# D17 paired-candidate implementation proof

Status: **non-authoritative implementation candidate prepared; authoritative migration remains unauthorised**.

Prepared after guarded squash merge of PR #57, against protected repository `main`:

`266362fe083fb278fc1dcc8f0a90619906194f07`

## Authority chain

D17 (`d17-neurodiversity-legacy-structural-disposition`) accepted the semantic disposition only. Its decision record deliberately did **not** itself authorise mutation of `structural-candidate.json`.

After PR #57 recorded and merged that owner decision, the owner explicitly opened the next substantive lane:

> non-authoritative paired-candidate implementation of D17: replace the proposed taxonomy emission with the accepted `legacy_retained_unmapped` disposition, without inventing a replacement relation or expanding to ADHD.

This proof records that later implementation authority. D17 is not rewritten.

## Implemented candidate semantics

`migration-candidates/autism-neurodiversity/structural-candidate.json` now preserves both reciprocal legacy records as migration data:

- Autism legacy record: `narrower_than -> neurodiversity`, note `Autism is commonly situated within neurodiversity discourse.`
- Neurodiversity legacy record: `broader_than -> autism`, note `Autism is commonly discussed within the neurodiversity ecosystem.`

For both records the current candidate now states:

- `disposition: legacy_retained_unmapped`
- `emit_v02_semantic_edge: false`
- no current v0.2 `type` field
- no current v0.2 `target` field
- no `confidence` value
- `confidence_status: not_required_without_v02_edge`

The old `paired-structural-relation-confidence` blocker ID is retained only for historical traceability and marked `resolved_by_d17_no_v02_edge`. D6 remains historical policy. It becomes relevant again only if a new semantic graph relation is separately proposed.

## Generator repair

`scripts/build_paired_migration_candidate.py` was updated so regeneration cannot recreate the superseded taxonomy/confidence assumptions.

The generated package now:

- retains the Autism -> Neurodiversity and Neurodiversity -> Autism legacy relation units as `legacy_retained_unmapped` with exact `legacy_value`;
- resolves `dependency-autism-neurodiversity` through D17 rather than through an invented confidence value;
- does not generate `resolve-autism-neurodiversity-structural-confidence` enrichment;
- preserves D1-D7 plus the later canonical owner decisions, including D17, in generated `owner-decisions.json`;
- keeps `dependency-neurodiversity-adhd` unresolved and outside the paired migration scope.

The package remains `owner_decision_pending`. `legacy_retained_unmapped` units, ADHD and other migration work still prevent authoritative readiness.

## Protected boundaries

This implementation does **not** authorise or perform:

- mutation of authoritative v0.1 Autism, Neurodiversity or ADHD objects;
- authoritative v0.2 replacement;
- a replacement Concept-to-Concept or Concept-to-Perspective relation;
- a relation-confidence value;
- schema or validator change;
- weakening reciprocity validation;
- ADHD migration scope expansion;
- publication or deployment.

The v0.2 common schema remains blob `ce0141ee7031f21fa2bd72b2faa3371aed3e622b`.

Authoritative source blobs remain:

- Autism: `b2d3809ecfcdb1d81c793a2401f0533a4b17ea98`
- Neurodiversity: `5a38bc4250079412dd3f4da1d598dfcab984ca66`
- ADHD: `719f26a9af773cd1bcf670df4d12ed5f6bcf0a23`

## Result

The candidate no longer turns an ambiguous legacy discourse relationship into a current taxonomy claim merely because the old relation label looked taxonomic. It preserves the source record, records the accepted disposition, and leaves any future semantic relation as a new evidence-backed act.
