# ND Oracle content and navigation v0.9

Date: 2026-08-28

## Priority

v0.9 is a content-and-navigation release. It deliberately does **not** add visual redesign, analytics, free-text AI answers, accounts, personalised ranking or diagnosis tooling.

## Candidate corpus

- 20 reviewed Concepts
- 50 reviewed Resources
- 30 reviewed practical Questions
- 100 governed objects total

Resource inclusion remains **listed, not endorsed**. The Resource catalogue remains claimless unless a separate governed claim/evidence route exists. Question pages remain **Relevant to inspect, not recommended**.

## Completion ledger for the 20-point content/navigation programme

1. **Content-gap map — complete.** `docs/CONTENT_GAP_MAP_v0.9.md` records ordinary-need domains, current coverage and missing lanes.
2. **Questions 14 → 30 — complete.** Sixteen additional governed Questions expand sensory, communication, work, study, assessment, sleep, food, masking/burnout, dyscalculia and family/parent routes.
3. **Daily life hub — complete.** `/needs/daily-life/`.
4. **Sensory & environment hub — complete.** `/needs/sensory-environment/`.
5. **Communication hub — complete.** `/needs/communication/`.
6. **Work hub — complete.** `/needs/work/`.
7. **Education & study hub — complete.** `/needs/education-study/`.
8. **Assessment & diagnosis cluster — complete.** `/needs/assessment-diagnosis/` plus adult autism/ADHD assessment Questions and reviewed NHS/NICE Resources. The boundary remains informational, not diagnostic.
9. **10 additional Concepts — complete.** Dyscalculia, Masking and camouflaging, Autistic burnout, Monotropism, Interoception, Alexithymia, Stimming, Communication differences, Task initiation and Sensory overload. Each has a reading-first explanation and ordinary orientation question as well as the precise evidence-backed object.
10. **Resources 25 → 50 — complete.** Twenty-five additional reviewed Resources expand first-party/official routes, peer/support organisations, accessibility, AAC, work/study support and practical material.
11. **Useful software/tools expansion — complete.** The Resource batch broadens task, accessibility, reading, transcription and AAC routes while preserving the non-endorsement boundary.
12. **Books & media expansion — complete.** The governed Books & media catalogue adds further memoir, practical and fiction entries; it remains an inspectable catalogue rather than a recommendation list.
13. **Browse by need — complete.** `/needs/` gives every current Question exactly one primary need group and links eight major life-area hubs.
14. **Browse by content type — complete.** `/types/` separates Questions, Topics and Resource categories including organisations, services, tools, apps, guides, work/education resources, games, books and media.
15. **Geographic scope navigation — complete.** `/places/` groups Resource listings by the jurisdiction expressed in their reviewed audience/scope text. Each Resource page exposes the same derived navigation label with an explicit `navigation scope, not eligibility` boundary.
16. **Reverse links — complete.** Existing Topic → Question/Resource and Resource → Question routes remain; Question pages now also expose adjacent governed Questions based on shared related-object references.
17. **Related Questions — complete.** Up to five adjacent Questions are ranked deterministically by number of shared governed related-object references. No semantic or personalised recommendation score is introduced.
18. **A–Z index — complete.** `/a-z/` exposes all 100 current Concepts, Resources and Questions in one static alphabetical index.
19. **Freshness checks — complete.** `scripts/check_content_freshness.py` uses governed `provenance.last_reviewed` metadata to surface overdue objects. Resources are due after 180 days; current other governed content after 365 days. CI runs the audit with `--fail-overdue`. The check is deliberately network-independent so transient outages do not decide publication. A stale former charity-domain candidate encountered during this batch was rejected rather than added, demonstrating why access-route review matters.
20. **100-object milestone — complete.** The candidate reaches exactly 20 Concepts + 50 Resources + 30 Questions.

## Public route contract

v0.8 accepted 62 canonical routes. The larger corpus contributes 51 additional detail routes:

- +10 Concepts
- +25 Resources
- +16 Questions

That produces 113 routes before new navigation. v0.9 adds 12 navigation routes:

- `/needs/`
- `/needs/daily-life/`
- `/needs/sensory-environment/`
- `/needs/communication/`
- `/needs/work/`
- `/needs/education-study/`
- `/needs/assessment-diagnosis/`
- `/needs/health-wellbeing/`
- `/needs/relationships-family/`
- `/types/`
- `/places/`
- `/a-z/`

**Candidate total: 125 canonical routes.**

The builder refuses a route count other than 125 and refuses duplicate sitemap routes.

## Compatibility

The accepted v0.8 object set is treated as a required subset rather than freezing the whole corpus at 25 Resources and 14 Questions. Regression checks require all 25 accepted v0.8 Resources and all 14 accepted v0.8 Questions to remain present while the catalogue grows.

The first five v0.7 Question routes retain their separate compatibility verification. The v0.6 reading/resource and production HTTP contracts remain inherited.

## Question grouping

Question grouping is deterministic and derived from the governed Question text/current understanding using ordered navigation rules. Every Question must appear exactly once in the primary need index. Grouping is a findability device; it is not a diagnosis, ontology assertion or recommendation score.

## Geographic grouping

Geographic labels are derived only from reviewed Resource audience/scope text. The current labels are:

- United Kingdom
- Great Britain
- England
- Northern Ireland
- International / not jurisdiction-specific

The label is explicitly not an eligibility or legal determination. Readers are told to inspect the source Resource for current rules.

## Freshness policy

`provenance.last_reviewed` is the system-of-record date for when an object and its access/source route were last checked.

- Resource re-review threshold: 180 days
- Concept/Question and other current governed-object threshold: 365 days
- Missing or invalid `last_reviewed`: overdue immediately

CI compiles code, validates all objects, runs the freshness audit, then runs regression tests.

## Non-goals

v0.9 does not add:

- a chatbot or free-text answer authority;
- diagnosis or screening;
- analytics or tracking;
- accounts or profiling;
- personalised ranking;
- efficacy claims for listed Resources;
- visual redesign.

The release goal is simply: **more governed knowledge, and more reliable ways to find it.**
