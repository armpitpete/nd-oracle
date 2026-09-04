# ND Oracle international expansion architecture v1

Date: 2026-09-04
Status: candidate architecture

## Decision

International expansion will proceed **one jurisdiction package at a time**. ND Oracle will not create an undifferentiated global layer and will not manufacture empty country shells.

The UK Reference Baseline v1 remains the reference implementation. The Assessment & diagnosis UK model is the primary jurisdictional precedent because it already proves national/local separation, clinical authority limits, first-party source preference, exact scope provenance and protected release gates.

## Architectural model

A country implementation is a **jurisdiction package**, not a folder containing country-labelled copies of UK content.

Each package may contain:

1. country identity;
2. applicable first-order subdivisions where materially relevant;
3. health/service regions or equivalent operational areas where materially relevant;
4. local provider/service examples only when explicitly labelled local;
5. governed Questions, Resources and Evidence;
6. source matrix;
7. additive discovery scope bindings;
8. deterministic benchmark cases;
9. freshness and reopening rules;
10. release/production evidence when published.

The hierarchy is conceptually:

`country -> subdivision -> service region -> local service -> governed route`

The exact levels are country-specific. ND Oracle must not force every country into a state/province model when its real service geography is different.

## Core rule: no silent jurisdiction inheritance

Geographic authority is never inferred merely because one place sits inside another.

- A local service rule must not become a national rule.
- A national entitlement or process must not be assumed to apply unchanged in every local implementation unless the authoritative source says so.
- A source's scope may narrow a parent jurisdiction but may not silently broaden it.
- Country-level Questions may link to local variation, but they must make the variation visible.
- UK routes must never surface as though they were local guidance for another country.

Discovery can use a jurisdiction relation to find relevant governed routes; it cannot create jurisdictional truth.

## No empty-country rule

A country package may enter the repository only when it can support a useful bounded slice.

Minimum entry requirements:

- at least one real user journey that can be answered or explicitly bounded;
- authoritative or otherwise defensible sources for that journey;
- an explicit jurisdiction/source matrix;
- at least one governed Question;
- at least one reviewed Resource or Evidence route as appropriate;
- limitations and reopening conditions;
- freshness ownership;
- deterministic hostile cases proving that neighbouring jurisdictions do not leak into the package.

A country name, flag, ISO code or placeholder page is not sufficient.

## Default pilot domain

The default first domain for a new country is **Assessment & diagnosis** because it stress-tests the hardest jurisdiction boundaries early:

- public versus private routes;
- referral mechanisms;
- national versus regional/local service authority;
- child versus adult routes;
- clinical versus educational assessment;
- diagnosis versus medication/prescribing;
- waiting/support routes;
- disagreement/no-diagnosis outcomes.

If authoritative assessment-pathway evidence is not maintainable, the country should not be added merely to satisfy geographic coverage. A different first domain requires an explicit reason recorded in the package.

## Source hierarchy

Default preference order:

1. national government or national health/public-service authority;
2. national clinical or professional guidance;
3. national programme/service guidance;
4. subdivision/state/province/region authority;
5. local public provider/service authority;
6. professional regulator/body;
7. peer-reviewed evidence for serious propositions not established by operational sources;
8. peer/community sources for lived-experience, access or practical context within their proper evidential scope.

Commercial directories and provider marketing may support identity/access facts but do not establish clinical quality, entitlement or efficacy.

## Language and translation

A package records the language of each authoritative source.

- First-party material in the jurisdiction's own language is preferred.
- English-only discoverability is not a reason to exclude authoritative local-language evidence.
- Machine translation may assist research but does not become authoritative provenance by itself.
- Published translated summaries must preserve the original source route and identify that the ND Oracle wording is a translation/summary.
- Translation uncertainty must remain visible when wording could materially affect entitlement, clinical meaning or safety.

## Discovery architecture

International expansion remains additive to the frozen discovery model.

Each country gets a versioned discovery extension that:

- names the package version;
- binds route scope to exact governed fields;
- records jurisdiction identity explicitly;
- contains deterministic intent phrases only for governed routes;
- cannot replace or mutate frozen UK scope bindings;
- includes hostile cross-border cases.

Examples of required hostile cases:

- a UK-only entitlement must not surface as a Canadian, Irish or Australian entitlement;
- a state/province route must not be presented as national;
- a local service example must not be presented as the country's general process;
- private-provider identity must not become provider endorsement;
- assessment questions must not cross into diagnosis or medication decisions.

## Data-model decision

**Do not change the core object schema for international geography yet.**

Use additive, versioned sidecar contracts for jurisdiction metadata and scope bindings, following the existing UK Assessment and Organisations patterns.

A core schema change should be reconsidered only after at least **three independently implemented country packages** expose repeated fields or validation needs that cannot be maintained safely through sidecars.

A future schema proposal must demonstrate:

- repeated real-world need rather than anticipated elegance;
- migration safety;
- stable ID preservation;
- backwards compatibility;
- no loss of provenance or uncertainty;
- exact impact on discovery and public routes.

## Package states

Country packages use these lifecycle states:

- `candidate` — being researched or built; not accepted public truth;
- `accepted` — exact-head review and merge gates passed;
- `production` — protected deployment and fresh live verification passed;
- `stale` — a critical source or pathway has exceeded its review window or materially changed;
- `paused` — maintenance cannot currently meet the required evidence standard;
- `retired` — package intentionally withdrawn, with historical provenance retained.

A package cannot claim `production` merely because its files exist on `main`.

## Package readiness gate

Before a country package can be called an accepted reference slice:

1. source authority and geography are mapped;
2. national/local distinctions are explicit;
3. at least one useful user journey is governed;
4. serious claims have Evidence and uncertainty routes;
5. local examples are labelled local;
6. clinical/legal/medication boundaries are preserved;
7. discovery scope is exact and additive;
8. cross-jurisdiction hostile tests pass;
9. freshness review passes;
10. full repository regression passes;
11. hostile diff review passes;
12. protected exact-head merge authority is separately granted.

Production additionally requires exact-main deployment, artifact identity and fresh network-backed verification.

## Expansion sequencing

International work follows this sequence:

1. choose one pilot country;
2. run a source-readiness probe before creating governed content;
3. build one bounded jurisdiction package;
4. test and hostile-review it;
5. merge only through the normal protected exact-head gate;
6. publish only through the normal protected deployment gate;
7. review what the first non-UK package taught us;
8. repeat for a second country;
9. repeat for a third country;
10. only then reconsider whether the sidecar model or package process needs structural change.

Parallel mass-country expansion is explicitly rejected for v1.

## Country selection criteria

Choose the next country by maintainability and usefulness, not by a target count.

Prefer jurisdictions where:

- authoritative public information is accessible;
- source ownership and geography can be understood;
- major user journeys can be bounded without guessing;
- freshness can realistically be maintained;
- language competence or review support is available;
- the package teaches the architecture something new.

Population size, commercial value or English-language convenience alone are insufficient.

## Global/common content

Some Concepts and practical principles may be reusable across countries, but reuse does not erase jurisdiction.

- Concepts may remain general where the evidence genuinely is.
- Country-specific access, entitlement, clinical process, legal process and service navigation remain scoped.
- A global Question is allowed only when its answer does not depend on jurisdiction, or when it explicitly asks the reader to choose a jurisdiction-specific route.
- No global fallback may silently substitute UK public-service guidance.

## Maintenance rule

Every accepted country package must name:

- critical sources;
- review cadence;
- owner/reopening trigger;
- known unstable pathways;
- local/national uncertainty;
- last reviewed date.

A critical-source change may move the package to `stale` even when the rest of the repository remains valid.

## Non-goals

International expansion v1 does not introduce:

- a graph database;
- a new core object schema;
- automatic geolocation;
- personalised ranking;
- country completeness scores;
- provider quality rankings;
- automatic translation as evidence;
- AI-generated jurisdiction advice;
- a promise to cover every country.

## Architecture conclusion

The durable model is:

**UK Reference Baseline v1 -> one tested jurisdiction package -> second package -> third package -> architecture review.**

The immediate next task after this architecture is accepted is a **single-country source-readiness probe**, not content generation across multiple countries.
