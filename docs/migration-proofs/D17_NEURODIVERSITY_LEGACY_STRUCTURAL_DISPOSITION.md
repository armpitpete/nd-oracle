# D17 — Neurodiversity legacy structural disposition

Status: owner decision accepted; decision record only.

Accepted on: 2026-08-11

Accepted against protected `main`:

`586f9589c4c14a0bcb7a84bc0c579bfef94f6d7c`

Owner decision:

`nd-neurodiversity-legacy-structural-disposition`

## Accepted disposition

For migration of the reciprocal Autism/Neurodiversity v0.1 structural records:

- preserve the Autism → Neurodiversity and Neurodiversity → Autism legacy records together;
- preserve each record's exact legacy relation type, target and explanatory note;
- record their migration disposition as `legacy_retained_unmapped`;
- do **not** emit a v0.2 `narrower_than` / `broader_than` taxonomy edge from those records;
- preserve D5 and D6 as historical decisions;
- supersede only D5's assumption that lossless preservation requires emitting the reciprocal v0.2 taxonomy pair;
- treat any future Autism → Neurodiversity-Paradigm semantic graph link as separately reviewed, evidence-backed enrichment;
- use ADHD only as a consistency test in this decision; do not expand migration scope to ADHD.

## Why this is bounded

The accepted review found a material tension inside the legacy records themselves: their type labels look taxonomic while their notes describe discourse/ecosystem association. Current reviewed terminology distinguishes neurodiversity from neurodivergence and does not cleanly support treating Autism or ADHD as literal taxonomic subtypes of Neurodiversity.

`legacy_retained_unmapped` therefore preserves the source record without silently selecting one side of that tension and turning it into a stronger current ontology claim.

## What this decision does not authorise

D17 does **not** authorise:

- mutation of `structural-candidate.json`;
- schema or validator changes;
- a replacement relation type or target;
- a relation-confidence value;
- creation of a new semantic enrichment relation;
- mutation of authoritative v0.1 Autism or Neurodiversity objects;
- authoritative v0.2 replacement;
- ADHD migration-scope expansion;
- publication or deployment.

Those remain separately protected gates.

## Preserved repository anchors

At acceptance:

- paired structural candidate blob: `c4ee90bbe829b85a4022e7d8ef48caa4692bd903`;
- relation-semantics review blob: `45513bd4ad8918c9598bea7cd276cd345ac4c6ff`;
- common v0.2 schema blob: `ce0141ee7031f21fa2bd72b2faa3371aed3e622b`;
- authoritative Autism blob: `b2d3809ecfcdb1d81c793a2401f0533a4b17ea98`;
- authoritative Neurodiversity blob: `5a38bc4250079412dd3f4da1d598dfcab984ca66`;
- authoritative ADHD blob: `719f26a9af773cd1bcf670df4d12ed5f6bcf0a23`.

The next implementation lane, if pursued, is a separately reviewed update to the non-authoritative paired migration candidate so that it represents the accepted `legacy_retained_unmapped` disposition without altering authoritative objects or inventing a replacement relation.