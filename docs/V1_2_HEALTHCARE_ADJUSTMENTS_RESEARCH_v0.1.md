# ND Oracle v1.2 healthcare communication/access parity research v0.1

Status: evidence baseline for the next bounded content slice after v1.2 production acceptance. This document is not merge or deployment authority.

Checked: 2026-08-31.

## Why this is the leading next slice

The fresh 125-object audit shows all three plausible national queries below still select unrelated governed routes:

- `healthcare communication adjustments Scotland` -> disabled-student support Scotland;
- `healthcare communication adjustments Wales` -> disabled-travel support Wales;
- `healthcare communication adjustments Northern Ireland` -> disabled-student support Northern Ireland.

England already has `healthcare-communication-adjustments-england` plus `nhs-england-accessible-information-adjustments`, so the defect is a clear jurisdiction-parity gap rather than absence of the need model itself.

## Authoritative source baseline

### Scotland

Primary route:

- NHS inform — **Communication and involving you**
- https://www.nhsinform.scot/care-support-and-rights/health-rights/communication-and-consent/communication-and-involving-you/
- Current page states that NHS information should be provided in a way the person can understand and that meets their needs; communication equipment/support can be provided; NHS staff can arrange interpreters/AAC support; people can have someone with them at appointments; and help can be requested where making or keeping appointments is difficult.

Supplementary practical route:

- NHS inform — **Support with accessing healthcare if you have a learning disability**
- https://www.nhsinform.scot/care-support-and-rights/health-rights/access/support-with-accessing-healthcare-if-you-have-a-learning-disability/
- Last updated 4 June 2026. It gives concrete examples of reasonable adjustments including accessible formats, longer appointments, a supporter, pre-visits, appointment timing and a less busy waiting area, and explicitly discusses sensory needs and communication preferences.
- Limitation: its direct audience is people with a learning disability, so it must not be presented as a neurodivergence-wide entitlement source by itself.

Assessment: sufficient authoritative evidence exists for a Scotland navigation Resource and practical Question, provided wording stays at the level of asking about communication/access support and does not generalise the learning-disability-specific examples beyond their source context.

### Wales

Primary route:

- Welsh Government — **Accessible communication and information standards in healthcare**
- https://www.gov.wales/accessible-communication-and-information-standards-healthcare
- First published 22 September 2025.
- The standards explicitly cover people whose language or communication barriers arise from neurodivergence. They apply across NHS Wales and include GP, emergency, pharmacy, dentist, optician, community and secondary-care settings.
- The standards cover identifying, recording, flagging, sharing and meeting communication/information needs; accessible formats; multiple appointment-contact methods; environmental barriers such as noise; communication support; and practical recording of individual needs.

Policy letter:

- Welsh Government Health Circular WHC/2025/038
- https://www.gov.wales/accessible-communication-and-information-standards-healthcare-whc2025038-html
- Status includes compliance for NHS bodies and action for GP practices; review date 22 September 2027.

Assessment: strongest of the three national source baselines. A Wales Resource can accurately describe the current all-Wales standards as navigation to first-party policy, with claims kept empty if the object is intended only to route users rather than adjudicate legal compliance.

### Northern Ireland

Primary rights route:

- nidirect — **Your rights in health**
- https://www.nidirect.gov.uk/articles/your-rights-health
- States that disabled people have rights of access to doctors' surgeries, dental surgeries, hospitals and other health services, and can ask for information in a usable format where reasonable.
- Northern Ireland uses its own disability-discrimination framework; this route must not be described as an Equality Act 2010 route.

Practical GP route:

- nidirect — **Your local doctor (GP)**
- https://www.nidirect.gov.uk/articles/your-local-doctor-gp
- States that if a person has communication problems or needs more time to discuss issues with the doctor, they should be able to book a longer appointment.

Supplementary HSC communication route:

- HSCNI Strategic Planning and Performance Group — **Making Communication Accessible for All Guide**
- https://online.hscni.net/wpfd_file/making-communication-accessible-for-all-guide/
- Official HSCNI material directs staff to identify and record information/communication needs and make service delivery flexible and communication-friendly.

Assessment: sufficient evidence exists for a Northern Ireland navigation Resource and practical Question. Wording should use the NI disability-rights/HSC framework and avoid importing England/Scotland/Wales legal terminology.

## Proposed bounded object set

After the current v1.2 release is accepted in production, the smallest coherent v0.2 implementation is exactly six new governed objects:

Questions:

1. `healthcare-communication-adjustments-scotland`
2. `healthcare-communication-adjustments-wales`
3. `healthcare-communication-adjustments-northern-ireland`

Resources:

1. `nhs-scotland-healthcare-communication-support`
2. `nhs-wales-accessible-communication-standards`
3. `northern-ireland-healthcare-communication-access`

No new Concept is currently justified. Existing `communication-differences`, `sensory-processing` and `sensory-overload` are sufficient relationship anchors.

## Proposed Question framing

Use parallel practical wording rather than legal adjudication:

- Scotland: **How can I ask for communication or sensory support at a health appointment in Scotland?**
- Wales: **How can I ask for communication or sensory adjustments at a health appointment in Wales?**
- Northern Ireland: **How can I ask for communication or access adjustments at a health appointment in Northern Ireland?**

The NI wording deliberately does not assume the Equality Act terminology used in Great Britain.

## Content authority boundary

The new Resources should be navigation/access records. Default `claims: []` unless a separately reviewed claim-bearing need emerges. They should not decide whether a specific provider has breached disability law, what adjustment is legally required in an individual case, or what clinical communication method is appropriate for a person.

## Acceptance design

A future implementation should require:

- exactly 131 governed objects if only these six are added: 20 Concepts + 64 Resources + 44 Questions + 3 Evidence;
- three national healthcare-adjustment queries selecting their matching Question first;
- matching official Resource available for each nation;
- incompatible national scoped routes excluded;
- England healthcare-adjustments route unchanged;
- clinical diagnosis/medication boundaries unchanged;
- all three new Resources remain non-claim-bearing navigation objects unless separately justified;
- exact scope-provenance bindings for the six new scoped routes;
- no ranking-weight change and no orientation activation;
- frozen v1.1 and v1.2 discovery regressions remain green;
- full site build, route-count update, Python/browser parity and hostile exact-tree review;
- stop at a protected merge gate.

## Sequencing constraint

Do not merge this content slice before the current v1.2 release candidate has been merged, deployed and accepted live. Otherwise the production acceptance boundary would move while still being tested. Research can proceed now; governed implementation should start from the accepted post-v1.2 production `main` SHA.
