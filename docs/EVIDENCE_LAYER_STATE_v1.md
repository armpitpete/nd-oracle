# Evidence Layer v1 — implementation state

Date: 2026-09-03

## Acceptance baseline

Evidence Layer v1 governs both accepted evidence models without forcing semantic migration:

- 49 governed Claims;
- 49/49 with complete Evidence and uncertainty routes;
- 57 accepted legacy v0.1 embedded source records;
- 3 normalized v0.2 Evidence objects;
- 60 total governed source records;
- 29 Claims with at least two governed source routes;
- zero uncovered Claims;
- zero orphan normalized Evidence objects.

The public Evidence projection adds `/evidence/` plus one deterministic detail route for each governed source record. These are projections, not new authoritative objects, so the authoritative object count remains 154. The expected canonical public route count becomes 238.

## Deliberate non-migrations

Legacy v0.1 sources remain authoritative under their accepted schema. They are projected publicly but are not duplicated as v0.2 Evidence objects merely to increase a count. A legacy source is not assigned a v0.2 contribution role that its source record never expressed.

Source-class diversity is an audit signal, not a quota. Dataset, book, commercial or other Evidence should be added only when a real governed Claim needs that source and the source materially improves the evidence route.

## Frozen boundaries

Evidence Layer v1 does not change schemas, discovery ranking/eligibility, clinical or diagnostic boundaries, jurisdiction filtering, browser/Python discovery parity, query privacy, analytics, static-runtime policy, external search or AI answer authority. Ordinary `/find/` continues to exclude Evidence pages.

## Freshness

Evidence review cadence is source-kind specific. This is a review interval for ND Oracle's interpretation/source route, not an expiry date for a publication. Accepted legacy embedded sources inherit the review state of the parent Concept unless separately migrated.

## Issue #106

The current v0.2 schema already distinguishes year/month/day precision. Issue #106 remains a narrower research backlog for uncertain candidate bibliographic dates where even the best day-level candidate must not be asserted as exact fact. Evidence Layer v1 does not require a schema mutation.
