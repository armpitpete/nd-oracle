# ND Oracle v1.2 healthcare communication parity v0.2

Status: implementation candidate for Issue #127.

This slice addresses one bounded need-coverage gap: healthcare communication/access adjustment navigation for Scotland, Wales and Northern Ireland. It does not reopen the accepted v1.1 discovery architecture and does not combine adult assessment, workplace support, travel, school-transition or everyday-life gaps.

## Baseline

Accepted v1.2 production source: `fad8e560979ba67bf94104d02f3b5100db8572cf`.

Implementation starts from protected `main` after the v1.2 production-state record merge: `46766af54cc8c1a7f45a91508890de49d0f5a71a`.

The pre-change 125-object audit recorded these wrong-domain top results:

- `healthcare communication adjustments Scotland` -> `/questions/disabled-student-support-scotland/`
- `healthcare communication adjustments Wales` -> `/questions/disabled-travel-support-wales/`
- `healthcare communication adjustments Northern Ireland` -> `/questions/disabled-student-support-northern-ireland/`

The existing England healthcare communication Question was already a correct positive control.

## Refreshed authoritative sources — 2026-09-01

### Scotland

Primary general route:

- NHS inform — **Communication and involving you**
- `https://www.nhsinform.scot/care-support-and-rights/health-rights/communication-and-consent/communication-and-involving-you/`
- Last updated by NHS inform: 15 January 2025.

The page summarises NHS Scotland patient communication rights, including information in a way the person can understand and communication equipment/support. The wider Charter page, last updated 25 June 2026, confirms the charter is for people using NHS services across Scotland and normally includes NHS primary care such as GPs, dentists, opticians and pharmacists.

Supplementary audience-limited route:

- NHS inform — **Support with accessing healthcare if you have a learning disability**
- `https://www.nhsinform.scot/care-support-and-rights/health-rights/access/support-with-accessing-healthcare-if-you-have-a-learning-disability/`
- Last updated: 4 June 2026.

This page gives practical examples including accessible formats, longer appointments, a supporter, pre-visits, suitable appointment timing and less-busy waiting arrangements. It is explicitly for people with a learning disability. The v0.2 Resource therefore treats it as supplementary and does not generalise those examples into a universal neurodivergence entitlement.

### Wales

- Welsh Government — **Accessible communication and information standards in healthcare**
- `https://www.gov.wales/accessible-communication-and-information-standards-healthcare-html`
- First/last published: 22 September 2025.

- Welsh Health Circular **WHC/2025/038**
- `https://www.gov.wales/accessible-communication-and-information-standards-healthcare-whc2025038-html`
- First published 22 September 2025; last updated 23 September 2025; review/expiry date 22 September 2027.

The renewed All-Wales NHS standards explicitly include communication barriers arising from neurodivergence. They cover identifying, recording, flagging, sharing and meeting communication/information needs and apply across NHS Wales settings including GP practices, community pharmacies, dentists, opticians, community/hospital sites and secondary care. Service-delivery provisions include accessible formats, multiple appointment-contact methods, communication support and circumstances requiring longer appointment times.

### Northern Ireland

- nidirect — **Your rights in health**
- `https://www.nidirect.gov.uk/articles/your-rights-health`

This records disability-discrimination access rights for Northern Ireland health and social services and says information can be requested in a usable format where reasonable.

- nidirect — **Your local doctor (GP)**
- `https://www.nidirect.gov.uk/articles/your-local-doctor-gp`

This says that if a person has communication problems or needs more time to discuss issues with a doctor, they should be able to book a longer appointment.

- HSC Northern Ireland — **Making Communication Accessible for All: A Guide for Health & Social Care Staff**
- `https://online.hscni.net/download/2452/physical-and-sensory-disability/33166/making-communication-accessible-for-all-guide.pdf`

The HSC guide is staff-facing. It supports communication-friendly service practice and is not treated as a personalised entitlement document.

Northern Ireland uses its own disability-discrimination framework. This slice deliberately does not import Equality Act 2010 framing into the NI Question or Resource.

## Governed additions

Exactly six new governed objects are added.

Questions:

1. `healthcare-communication-adjustments-scotland`
2. `healthcare-communication-adjustments-wales`
3. `healthcare-communication-adjustments-northern-ireland`

Resources:

1. `nhs-scotland-healthcare-communication-support`
2. `nhs-wales-accessible-communication-standards`
3. `northern-ireland-healthcare-communication-access`

No new Concept is required. The Questions reuse:

- `communication-differences`
- `sensory-processing`
- `sensory-overload`

All three Resources are reviewed navigation/access records with `claims: []`.

## Expected corpus

After the six additions:

- 20 Concepts
- 64 Resources
- 44 Questions
- 3 Evidence
- **131 governed objects**

The static build is expected to add six canonical routes, but the final route count must be derived from the build rather than treated as an assumption.

## Discovery changes permitted by this slice

The six new routes receive bounded routing phrases and exact jurisdiction scope-provenance bindings using the existing v1.1 mechanism. The governed scoped-route registry cardinality advances from 35 to 41.

The following are unchanged:

- jurisdiction scope sets and extraction rules;
- ranking weights;
- lexical eligibility thresholds;
- personal diagnosis/medication hard boundaries;
- orientation remains disabled;
- Python/browser evaluator semantics;
- privacy/query handling;
- static/passive runtime boundary;
- external-search policy;
- analytics/profile policy;
- AI answer authority.

## Acceptance

The candidate must prove:

- matching Scotland/Wales/Northern Ireland healthcare communication queries select the matching Question first;
- each matching official Resource is discoverable;
- incompatible national healthcare routes are excluded;
- the England healthcare route remains top for England;
- all new Resources remain non-claim-bearing;
- all six routes have exact scope-provenance fingerprints and scope bindings;
- 131 objects validate with zero overdue;
- frozen v1.1 and v1.2 discovery, clinical, privacy and compatibility tests remain green;
- Python/browser parity remains exact;
- the static build derives the canonical route count and contains no unexpected runtime surface;
- full CI and exact-tree hostile review pass.

No merge or deployment is authorised by this implementation document. The work stops at the protected merge gate.