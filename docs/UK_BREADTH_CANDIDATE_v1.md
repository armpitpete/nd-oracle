# ND Oracle UK breadth candidate v1

Date: 2026-09-04

## Purpose

This record defines the bounded UK-breadth candidate built from protected `main` at `3867a4734a66ebee07f37d593beeaaa7f4701a2f`. It is a repository candidate only. It does not change accepted production, authorize merge, or authorize deployment.

## Candidate contract

The candidate contains:

- 20 reviewed Concepts;
- 125 reviewed Resources;
- 135 reviewed practical Questions;
- 3 normalized Evidence objects;
- 283 governed objects total;
- 367 canonical public routes.

The slice adds 49 reviewed Questions and 26 reviewed, claimless Resources across daily living, sensory needs, communication, work, education, money and administration, sleep, food and eating, healthcare access, mental wellbeing, mobility and travel, technology and accessibility, books and media, and organisations / peer community.

## Accepted production boundary

Accepted production remains the 2026-09-03 Relationships & family deployment:

- source SHA `5c05d775a5d548c0f4ad92f78e25008febe40d69`;
- 208 governed objects;
- 292 canonical routes;
- production identity resolved only through `contracts/current-production.json`.

This candidate must not rewrite that production pointer before a separately protected deployment and fresh live verification.

## Frozen architecture

This candidate does not change:

- schemas or object-type contracts;
- `discovery/routing-policy-v1.1.json`;
- the additive Assessment & diagnosis discovery extension;
- ranking weights or lexical eligibility;
- diagnosis or medication decision boundaries;
- jurisdiction scope sets or provenance bindings;
- query-storage, profiling, analytics or external-search policy;
- AI answer authority;
- current production identity;
- Cloudflare production deployment workflow.

The temporary branch-only writer workflow used to wire navigation is deliberately removed before acceptance.

## Safety gates

Permanent tests require:

- urgent mental-health content to route to current human services and refuse crisis assessment/counselling;
- ARFID content to remain informational and non-diagnostic;
- sleep/medication content to refuse start/stop/increase/decrease dosing decisions;
- benefit challenge navigation to avoid legal advice;
- every new Resource to remain claimless, reviewed and reachable by HTTPS;
- frozen diagnosis and medication refusals to remain authoritative.

## Discovery and projection acceptance

`benchmarks/uk-breadth-v1.json` provides 29 deterministic cases covering representative new domain routes plus hostile clinical-boundary cases.

`tests/test_uk_breadth_v1.py` binds:

- exact 283-object candidate counts;
- exact 367-route candidate contract;
- all 49 new Question routes;
- all 26 new Resource routes;
- resource review / locator / claimlessness invariants;
- critical clinical, crisis and legal-authority wording;
- accepted-production immutability;
- absence of the temporary writer workflow;
- preservation of the frozen v1.1 routing contract.

## Acceptance sequence

Before merge:

1. PR head must be based on protected `main` with no behind commits.
2. Full PR-triggered validation must pass on the exact head.
3. Validation must include compile, object validation, Evidence coverage, Evidence-source freshness, governed-content freshness and the complete unittest suite.
4. The final exact diff must receive hostile review for authority, clinical safety, jurisdiction, provenance, privacy, release state and accidental workflow mutation.
5. The exact reviewed head SHA must be recorded in the PR acceptance record.
6. Stop at the protected exact-head merge-authorisation gate.

No merge or deployment authority is granted by this document.
