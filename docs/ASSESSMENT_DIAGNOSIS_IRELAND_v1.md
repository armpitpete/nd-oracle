# Assessment & Diagnosis — Republic of Ireland reference contract v1

Date: 2026-09-04
Parent architecture: `docs/INTERNATIONAL_EXPANSION_ARCHITECTURE_v1.md`
Readiness decision: `docs/INTERNATIONAL_PILOT_IRELAND_READINESS_v1.md`

## Purpose

Define the first non-UK ND Oracle jurisdiction package as a bounded Republic-of-Ireland Assessment & diagnosis reference slice without weakening the frozen UK, clinical, privacy, provenance, ranking, Evidence or release-state boundaries.

## Jurisdiction model

The package scope is **Republic of Ireland**.

It must not silently include Northern Ireland. Republic-of-Ireland HSE routes and Northern Ireland HSC/NHS routes are separate service systems even though both are on the island of Ireland.

The HSE remains one national organisation, but current delivery is organised through six health regions with local decision-making. National guidance may therefore coexist with regional/catchment variation.

## Included journeys

v1 contains four Questions:

1. adult autism assessment in the Republic of Ireland;
2. child autism assessment in the Republic of Ireland;
3. adult ADHD assessment in the Republic of Ireland;
4. HSE Assessment of Need versus clinical diagnostic assessment.

Child ADHD is deliberately deferred because current first-party evidence does not yet justify a strong, uniform national access route.

## Adult autism boundary

Current HSE guidance says the HSE does not provide adult autism assessments and that adults seeking formal assessment currently need to pay for private assessment. ND Oracle may report that access fact, but it must not:

- recommend a private provider;
- infer provider quality;
- decide whether a person should seek diagnosis;
- treat the national autism protocol as proof of a public adult service.

## Child autism boundary

The HSE National Protocol for Autism Assessment and Intervention Pathways, effective 25 March 2026, provides a national framework. Child referral/support routing can still depend on need and local service organisation.

Children's disability support must not be made conditional on diagnosis or Assessment of Need where HSE guidance explicitly says otherwise.

## Adult ADHD boundary

The HSE Adult ADHD Model of Care describes the intended national specialist model, but current team rollout remains incomplete and region/catchment dependent.

ND Oracle must distinguish:

- model of care;
- actual current local access;
- diagnosis;
- medication initiation;
- titration;
- prescribing;
- ongoing treatment.

No local team or catchment may be promoted into a national access promise.

## Assessment of Need boundary

HSE Assessment of Need is a separate statutory process under the Disability Act 2005. It is not interchangeable with autism or ADHD clinical diagnostic assessment.

The reviewed HSE guidance says Assessment of Need is not required to access health services. That does not guarantee access to any specific service.

## Discovery rule

The Republic-of-Ireland package is additive.

- frozen `discovery/routing-policy-v1.1.json` remains unchanged;
- frozen UK Assessment extension remains unchanged;
- `discovery/assessment-diagnosis-ireland-v1.json` adds a Republic-of-Ireland scope set and exact governed-field bindings in memory;
- `Republic of Ireland` and bounded `Ireland` aliases resolve only to the Republic-of-Ireland scope;
- `Northern Ireland` is matched before `Ireland` so the shorter alias cannot swallow the northern jurisdiction;
- ranking weights remain unchanged.

## Acceptance gates

Before v1 can be called an accepted reference slice:

- all 4 Questions validate;
- all 8 new Resources remain reviewed and claimless;
- exact Republic-of-Ireland scope fingerprints match committed governed fields;
- Northern Ireland and Republic-of-Ireland routes fail closed across the border;
- England Right to Choose cannot surface as an Irish entitlement;
- Assessment of Need cannot become clinical diagnosis;
- adult ADHD Model of Care cannot become universal service availability;
- child ADHD remains deferred;
- full regression suite passes;
- hostile diff review passes;
- exact-head merge is separately authorised.

Production remains a separate protected release decision.

## Non-goals

- no comprehensive Ireland neurodivergence corpus;
- no child ADHD national route in v1;
- no provider ranking;
- no new core schema;
- no analytics, geolocation or personalisation;
- no medication advice;
- no production deployment in this candidate.
