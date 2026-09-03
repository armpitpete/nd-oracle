# Relationships & family — UK v1 candidate state

Date: 2026-09-03
Base main: `8679d6ebd555b46b6ba42950276b2d1722d1737b`

## Baseline defect evidence

- `friendship misunderstandings autism` returned `no_match`.
- `support parenting a neurodivergent child UK` could route to `autistic-parent-support-uk`, which answers a different question: support for an autistic parent.
- Current accepted production remains 190 governed objects and 274 canonical routes. This candidate does not rewrite current-production evidence before a separately authorised deployment.

## Candidate scope

Adds a bounded strong seed rather than claiming all relationship/family needs are solved:

- 10 governed Questions:
  - friendship misunderstandings;
  - partner communication/processing/sensory needs;
  - boundaries;
  - conflict and repair;
  - intimacy/consent;
  - parenting a neurodivergent child;
  - disabled/neurodivergent parent service access;
  - family-event sensory/social load;
  - relationship safety/domestic-abuse routing;
  - explicit no-authority route for “should I leave or stay?”.
- 8 claimless Resources from NHS, GOV.UK, equality regulators, Contact and the National Autistic Society.
- 48-case deterministic Relationships & family discovery/safety benchmark.
- source matrix and section contract.

Expected object count if merged: **208 governed objects** (20 Concepts, 99 Resources, 86 Questions, 3 Evidence). Exact canonical-route and regression-test totals are CI-derived and must not be written into production evidence until accepted deployment verification.

## Preserved boundaries

- no schema change;
- no ranking-weight change;
- no new AI authority;
- no query storage, profiling or analytics;
- no personalised relationship decision;
- no diagnosis inference weakening;
- no medication-boundary weakening;
- no claim-bearing Resource;
- no provider endorsement;
- no production deployment.

## Completion gate

The implementation candidate is complete only after exact-head CI is green and hostile review confirms the two baseline defects are corrected without discovery, clinical, jurisdiction, privacy, evidence or release-state regression. Merge and production remain protected exact-SHA actions.
