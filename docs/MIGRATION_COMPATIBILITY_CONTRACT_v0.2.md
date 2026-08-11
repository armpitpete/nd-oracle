# ND Oracle Transitional Migration Compatibility Contract v0.2

Status: **proposal for owner acceptance**. Documentation only. This contract does not modify schema, validator behaviour, authoritative objects, site code, or production.

Base repository state: `cb4546bb27ba78909c8f4ac84bb36104601171cf`.

Primary evidence: the accepted Autism deterministic migration proof recorded by PR #30. That proof established that all v0.1 preservation units can be inventoried, but some cannot be represented losslessly under the current v0.2 contract without additional evidence or owner decisions.

## Purpose

This contract defines how ND Oracle may prepare v0.1 → v0.2 migration candidates without either:

1. inventing semantics that are absent from v0.1;
2. weakening the accepted v0.2 knowledge model merely to make migration convenient; or
3. silently dropping legacy information that has no current v0.2 home.

The governing rule is:

> **A migration candidate may be incomplete, but it may never be silently lossy.**

A candidate is not authoritative merely because it validates syntactically. Every legacy preservation unit must have an explicit disposition before authoritative replacement can be considered.

## Non-goals

This contract does not:

- migrate any authoritative object;
- change `schema/object-v0.2.json` or any v0.2 type schema;
- change `scripts/validate.py`;
- weaken structural reciprocity;
- infer new scientific or clinical claims;
- promote embedded uncertainty or ecosystem questions automatically into standalone Question objects;
- decide that v0.1 `related_to` means v0.2 `associated_with`;
- decide how list-valued v0.1 uncertainty reduction conditions should be represented in v0.2;
- authorise website, search, Oracle/AI, deployment, DNS, analytics, accounts, forms, comments, or personal-data changes.

## Core invariants

### 1. Source authority remains the v0.1 Git blob until acceptance

Every migration package MUST identify:

- authoritative source path;
- source Git blob SHA;
- source schema version;
- object ID;
- migration contract version.

If the authoritative source blob changes, the package is stale and MUST be rebuilt or explicitly reconciled.

### 2. Preservation inventory is mandatory

Every package MUST begin from the deterministic `v01_preservation_inventory()` output for the exact source blob.

Every preservation unit MUST be assigned exactly one current disposition:

- `represented_exactly` — preserved without semantic reinterpretation;
- `represented_with_verified_enrichment` — v0.2 requires additional information that has been verified from an identified source;
- `owner_decision_required` — more than one materially plausible semantic mapping exists;
- `structural_dependency` — representation depends on migration of another object or relation-connected unit;
- `legacy_retained_unmapped` — no accepted v0.2 representation currently exists;
- `rejected_with_reason` — an explicit owner decision accepts non-preservation, with rationale and reopening condition.

No unit may be omitted, defaulted, or treated as preserved merely because a candidate validates.

### 3. Missing semantics are never fabricated

A migration tool MUST NOT synthesize values merely to satisfy required v0.2 fields.

Examples include:

- Evidence Contribution `role`;
- Evidence Contribution `finding`;
- Evidence Contribution `population_or_context`;
- Evidence Contribution `methodology`;
- Evidence `title`, `date`, or `authorship` when not deterministically present;
- Perspective representation scope;
- Perspective reasoning;
- Perspective scope.

A placeholder that looks like substantive data is prohibited. Missing required semantics remain explicit migration blockers until verified enrichment or a separately accepted schema-policy change resolves them.

### 4. Enrichment is a new evidential act

When migration requires information not encoded in v0.1, enrichment MUST be distinguishable from deterministic transformation.

Each enrichment record MUST identify:

- target v0.2 field;
- source preservation unit or legacy record that triggered the need;
- evidence route used to supply the new value;
- exact proposed value;
- actor or process that supplied it;
- review state;
- uncertainty or limitation, where applicable.

Parsing a citation string is not automatically equivalent to verifying title, authorship, date, methodology, population, or findings.

### 5. Existing proposition text and confidence are protected

Migration MUST NOT silently rewrite:

- Claim text;
- Claim IDs;
- Claim confidence;
- object ID;
- summary;
- aliases;
- scope includes/excludes;
- provenance history.

Any substantive revision belongs to a separate editorial/evidential change, even if performed near migration.

### 6. Legacy uncertainty is preserved before it is reshaped

The v0.1 uncertainty fields `question`, `why_it_matters`, `what_would_reduce_it`, and `status` MUST remain recoverable from the migration package.

Where the v0.2 embedded Uncertainty shape does not provide a lossless deterministic representation — including list-valued `what_would_reduce_it` versus a single `reopening_or_reduction_condition` string — the original record remains in the preservation ledger and the mapping is `owner_decision_required` until accepted.

Joining a list into prose is not treated as lossless merely because all words remain present.

### 7. Perspective migration requires attribution discipline

A v0.1 Perspective MAY supply candidate material for a v0.2 Perspective, but absent fields MUST NOT be invented.

For the Autism specimen, deterministic data exists for:

- Perspective ID;
- attributed holder name;
- summary/position text;
- source routes.

The current v0.1 record does not deterministically provide the v0.2 fields for holder representation scope, reasoning, or Perspective scope. Those remain enrichment requirements or owner decisions.

### 8. Evidence identity and Evidence Contribution are separate migration tasks

A v0.1 source MAY deterministically seed an Evidence identity using preserved source ID, citation, locator and source kind where those values are explicit.

It MUST NOT be treated as a complete v0.2 Evidence object until required source metadata is verified.

A v0.1 `supports` route proves that the legacy object linked a source to a Claim or Perspective. It does **not** by itself determine a v0.2 Evidence Contribution role, finding, population/context, methodology, or limitation set.

Therefore Claim ↔ Evidence routing and Evidence Contribution enrichment are separately tracked.

### 9. Structural reciprocity is not weakened for migration convenience

The authoritative v0.2 validator continues to require reciprocal `broader_than` / `narrower_than` Concept relations.

A migration package for a Concept with a structural edge MUST record the reciprocal object as a `structural_dependency` unless both sides can be represented as a valid v0.2 structural pair in the candidate graph.

The migration unit therefore expands to the minimum structural closure required by reciprocal structural relations. This is a staging rule, not an automatic authorisation to migrate every connected object.

Mixed-version authoritative reciprocity is not considered valid merely to enable incremental replacement.

### 10. Non-structural relation mapping is explicit

Exact relation vocabulary matches may be transformed deterministically only when semantics remain unchanged.

The v0.1 relation `related_to` has no exact v0.2 synonym. Mapping it to `associated_with` requires owner acceptance or a later explicit compatibility rule. Until then the original relation is retained in the preservation ledger as `owner_decision_required`.

### 11. Ecosystem entry points are preserved as legacy semantics

`ecosystem_entry_points` have no accepted v0.2 Concept field.

They MUST therefore remain verbatim in the migration package as `legacy_retained_unmapped` until an accepted model extension or explicit owner disposition exists.

Their embedded questions MUST NOT automatically become standalone Question objects. Promotion requires the independent-reusability test defined by the v0.2 model and separate review.

### 12. Validation and migration readiness are different states

A candidate package may contain candidate v0.2 objects that are not yet eligible for authoritative repository validation because required enrichment is unresolved.

Migration status is therefore separate from JSON Schema validity.

The allowed package states are:

1. `inventoried` — exact source blob anchored and all preservation units enumerated;
2. `mapped` — every unit has a disposition;
3. `enrichment_pending` — one or more required v0.2 semantics still need evidence-backed enrichment;
4. `owner_decision_pending` — one or more semantic choices require explicit owner acceptance;
5. `structural_dependency_pending` — reciprocal or other bounded graph dependencies remain unresolved;
6. `candidate_complete` — candidate graph plus preservation ledger account for every unit and all required enrichment is evidenced;
7. `ready_for_authoritative_review` — candidate passes applicable schemas/graph checks and has no unresolved preservation unit;
8. `accepted_for_authoritative_replacement` — separate owner acceptance has authorised the exact replacement candidate.

No earlier state implies a later one.

## Migration package

A future implementation of this contract SHOULD produce a non-authoritative package with this logical structure:

```text
migration-candidates/<object-or-unit>/
├── manifest.json
├── preservation-ledger.json
├── candidate/
│   └── ... proposed v0.2 objects ...
├── enrichment-ledger.json
├── dependency-ledger.json
└── decision-log.md
```

The exact filesystem location and machine-readable schemas are implementation details for a later protected lane.

### `manifest.json`

At minimum:

- migration contract version;
- source repository commit;
- source path(s);
- source blob SHA(s);
- source object ID(s);
- candidate object IDs;
- package status;
- created/updated metadata.

### `preservation-ledger.json`

For every `v01_preservation_inventory()` unit:

- exact unit value;
- disposition;
- candidate destination, if any;
- evidence/enrichment reference, if any;
- owner-decision reference, if any;
- unresolved reason, if any.

### `enrichment-ledger.json`

For every non-deterministic required field:

- target object and field;
- proposed value;
- evidence route;
- source of the enrichment;
- review state;
- limitations.

### `dependency-ledger.json`

For graph-coupled migration work:

- source object;
- relation;
- dependent object;
- reason the dependency is required;
- current resolution status.

### `decision-log.md`

Records explicit owner decisions, rejected alternatives, rationale, and reopening conditions. Rejected mappings remain visible rather than disappearing after a decision.

## Autism specimen under this contract

The accepted Autism proof becomes the first conformance case.

### Deterministically preservable

The migration package can preserve without substantive reinterpretation:

- object identity and naming;
- aliases;
- summary;
- scope includes/excludes;
- Claim IDs, text and confidence;
- legacy Claim→source routes as routes requiring Evidence conversion;
- source IDs, source kinds, citations, HTTPS locators and accessed dates;
- original uncertainty records verbatim in the preservation ledger;
- original Perspective record verbatim in the preservation ledger;
- original relation records verbatim in the preservation ledger;
- ecosystem entry points verbatim in the preservation ledger;
- original provenance.

### Blocking enrichment

Before a valid authoritative v0.2 Autism graph can exist, evidence-backed work is still required for:

- Evidence Contribution semantics;
- Evidence metadata absent from v0.1;
- Perspective fields absent from v0.1.

### Structural dependency

Autism's `narrower_than → neurodiversity` relation requires the reciprocal Neurodiversity side to participate in the candidate structural graph before authoritative v0.2 validation can pass without weakening reciprocity.

### Owner decisions still required

- whether `related_to` is accepted as `associated_with` for legacy migration;
- how list-valued `what_would_reduce_it` maps to the current v0.2 single-string field;
- the eventual v0.2 home or explicit disposition for ecosystem entry points.

## Acceptance criteria for a future implementation lane

A migration-compatibility implementation is not complete until tests prove that:

1. source blob drift invalidates a package;
2. every preservation unit must have exactly one disposition;
3. unknown or omitted units fail closed;
4. placeholder values cannot satisfy enrichment requirements;
5. deterministic transforms cannot manufacture Evidence Contribution semantics;
6. enrichment records require an evidence route;
7. unresolved owner decisions prevent `ready_for_authoritative_review`;
8. unresolved structural dependencies prevent `ready_for_authoritative_review`;
9. legacy-unmapped units remain recoverable byte-for-byte or structurally equivalent to their original JSON value;
10. ecosystem entry-point questions are not auto-promoted;
11. `related_to` is not auto-converted to `associated_with` without an accepted policy rule;
12. an exact completed package can be validated without modifying the authoritative v0.1 source object;
13. authoritative replacement remains a separate exact-candidate owner action.

## Protected next step if this contract is accepted

Acceptance of this document would authorise only the next bounded implementation lane:

> Implement migration-package schemas, a migration-proof validator, and Autism package fixtures against the accepted contract, with **no authoritative object replacement** and no change to the v0.2 authoritative schemas unless a separately identified contract defect requires owner review.

That implementation must stop at an exact-head reviewed PR before any authoritative migration candidate is accepted or installed.
