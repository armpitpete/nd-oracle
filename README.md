# ND Oracle

ND Oracle is a provenance-first knowledge commons for the full neurodiversity ecosystem. It connects concepts and claims to evidence, lived experience, uncertainty, and practical resources—including tools, games, apps, books and media, services, organisations, communities, and accommodations.

This repository is the system of record. The public site at `https://ndoracle.org` is a reading-first window onto validated repository content; it does not replace the repository as the knowledge authority.

## Governing rules

1. Never make the next person rediscover an uncertainty already identified.
2. Every serious question leaves the knowledge system better than it found it.
3. No conclusion without its route back to evidence and uncertainty.
4. Measure success by epistemic work saved, not text produced.

## Current repository state

The current repository candidate contains exactly 283 governed objects. It is the bounded `coverage/uk-breadth-v1` candidate and is **not accepted production**:

- 20 reviewed Concept objects;
- 125 reviewed Resource objects;
- 135 reviewed Question objects;
- 3 normalized v0.2 Evidence objects;
- 367 canonical public routes in the candidate build contract.

The UK-breadth slice adds 49 reviewed Questions and 26 reviewed, claimless Resources across daily living, sensory needs, communication, work, education, money and administration, sleep, food and eating, healthcare access, mental wellbeing, mobility and travel, technology and accessibility, books and media, and organisations / peer community. The candidate preserves frozen discovery, jurisdiction, clinical, privacy, provenance, ranking and AI-authority boundaries.

Accepted production remains the 2026-09-03 Relationships & family deployment: 208 governed objects and 292 canonical routes from exact source SHA `5c05d775a5d548c0f4ad92f78e25008febe40d69`. `contracts/current-production.json` remains the only current-production pointer until a separately protected deployment and fresh live verification succeed.

Resource inclusion is **not endorsement**. A Resource may be listed without an efficacy claim when its identity, access route, intended use, limitations, cost/access notes and conflicts are useful. Serious testable propositions require governed evidence and uncertainty routes; the claim-bearing pilot makes those routes visible without turning inclusion into an endorsement.

Question routes use the boundary **Relevant to inspect, not recommended**. They expose a bounded current understanding, related governed objects, adjacent Questions, evidence gaps, dissent and reopening conditions without turning discovery into a personalised recommendation.

Every v0.2 Resource requires at least one typed access locator. HTTPS URLs are enforced for web locators so a public catalogue entry cannot become an unreachable name with no governed route to the thing being described.

The current accepted public contract contains 292 canonical routes. It preserves the v1.2 public-site builder identity, frozen discovery architecture, reading/navigation surface and privacy/static boundaries while including devolved healthcare-communication parity, bounded Games & downtime coverage, the UK Assessment & diagnosis reference implementation, and the Relationships & family UK v1 bounded reference slice. The Evidence Layer contributes `/evidence/` plus 60 deterministic Evidence detail projections.

Assessment & diagnosis contains the adult/child × autism/ADHD × England/Scotland/Wales/Northern Ireland matrix plus cross-cutting routes for private assessment, waiting/support, refusal or disagreement, after-assessment outcomes, communication/sensory adjustments, co-occurring autism/ADHD and other neurodevelopmental assessments. England-specific Right to Choose is contained to England; Scottish health-board variation, Welsh health-board/local-service variation and Northern Ireland Trust/service-development variation remain explicit. Fifteen assessment Resources are claimless service/guidance listings, not provider endorsements or diagnostic claims. Discovery adds 29 cryptographically scope-bound routes without replacing the frozen 41-route v1.1 scope registry, producing 70 governed scoped routes in current accepted production. No schema, ranking-weight, clinical-decision, privacy/query-handling, analytics or AI-authority boundary is weakened.

Relationships & family keeps parenting a neurodivergent child separate from support for a neurodivergent or disabled parent; ordinary relationship communication does not displace safeguarding where fear, control, violence or sexual pressure is present; consent remains explicit and revocable; ND Oracle does not diagnose a partner, decide who is right, or decide whether a relationship should continue; and disability-service access preserves the England/Scotland/Wales versus Northern Ireland legal split. The accepted 48-case benchmark was integrated without changing frozen ranking weights.

## Production state

Current production is the accepted 2026-09-03 Relationships & family deployment of the `v1.2` public-site builder contract at `https://ndoracle.org`, generated from exact source SHA `5c05d775a5d548c0f4ad92f78e25008febe40d69` and tree `5861cd9ecbd33b2e465bbbd9027324182a9ef12b` by deployment workflow run `33796135523` (run #22). The generated artifact SHA-256 is `4864e9a9aa56a3278ad46d4a32695354f25018b9ce9d2ccb46cf8fa68ba4ba2a` and the Cloudflare deployment identity is `https://7452fa61.nd-oracle.pages.dev`.

Fresh network-backed production verification ran against the canonical domain in workflow run `33796510768` (run #17), job `100785403728`. It revalidated all 208 governed objects, ran the complete 392-test regression suite, and verified all 292 canonical live routes plus the governed discovery/evidence and frozen compatibility contracts. Exact-head run `33795297003` (#331) on the identical accepted tree separately proved 49/49 Claim coverage with 0 gaps, 60 governed source records with 0 overdue and 208 governed objects with 0 overdue.

`contracts/current-production.json` is the canonical machine-readable current-production pointer. It references `docs/PRODUCTION_STATE_2026-09-03_RELATIONSHIPS_FAMILY.md`, the immutable human-readable evidence record for this accepted deployment. `docs/PRODUCTION_STATE_2026-09-03.md`, `docs/PRODUCTION_STATE_v1.2.md` and earlier production-state documents remain frozen historical evidence and are not used as implicit current-state pointers.

The administrative state-reconciliation commit that updates these records is not itself a deployment. The accepted public artifact remains the exact artifact generated from source SHA `5c05d775a5d548c0f4ad92f78e25008febe40d69`.

## Repository map

```text
objects/concepts/                    Reviewed concept objects
objects/resources/                   Reviewed resource objects
objects/questions/                   Reviewed practical question objects
objects/evidence/                    Governed evidence objects
schema/object-v0.1.json              v0.1 concept contract
schema/object-v0.2.json              v0.2 object dispatcher
schema/types/                        v0.2 object-type contracts
discovery/routing-policy-v1.1.json   Frozen deterministic v1.1 discovery policy
discovery/assessment-diagnosis-uk-v1.json Additive UK assessment discovery extension
site/                                Static public site source
scripts/validate.py                  Schema, governance-route, and graph checks
scripts/check_content_freshness.py   Review-age/freshness gate, including Evidence source-kind cadence
scripts/evidence_coverage.py         Claim/Evidence coverage registry and CI gate
scripts/evidence_public.py           Public Evidence projection and static browsing
contracts/evidence-layer-v1.json     Machine-readable Evidence policy
contracts/current-production.json    Canonical machine-readable current-production pointer
docs/EVIDENCE_LAYER_STATE_v1.md      Current Evidence-layer implementation state
docs/ASSESSMENT_DIAGNOSIS_UK_v1.md   UK assessment/diagnosis reference contract
docs/ASSESSMENT_DIAGNOSIS_UK_SOURCE_MATRIX_v1.md UK source/jurisdiction matrix
docs/RELATIONSHIPS_FAMILY_UK_v1.md   Relationships & family bounded coverage contract
docs/RELATIONSHIPS_FAMILY_UK_SOURCE_MATRIX_v1.md Relationships & family source matrix
docs/UK_BREADTH_CANDIDATE_v1.md      UK breadth candidate contract and acceptance gates
benchmarks/uk-breadth-v1.json        UK breadth deterministic discovery/hostile benchmark
scripts/build_site.py                Current self-contained static site generator
scripts/discovery.py                 Deterministic governed discovery index/routing
scripts/verify_live_site.py          Current production HTTP/content verifier
scripts/build_site_v06.py            Preserved historical compatibility source
scripts/build_site_v08.py            Preserved historical compatibility source
docs/ECOSYSTEM_PUBLICATION_v0.6.md   Ecosystem publication contract
docs/PUBLIC_QUESTION_DISCOVERY_v0.7.md Historical question-led discovery contract
docs/CONTENT_NAVIGATION_v0.8.md      Historical accepted v0.8 findability contract
docs/CONTENT_NAVIGATION_v0.9.md      Historical accepted v0.9 navigation contract
docs/CONTENT_GAP_MAP_v0.9.md         Historical need-led editorial coverage map
docs/CONTENT_GAP_MAP_v1.4.md         Current need-led editorial coverage map
docs/GAMES_DOWNTIME_FACETS_v1.md     Governed descriptive-facet contract for games and downtime
docs/PRODUCTION_STATE_2026-09-03_RELATIONSHIPS_FAMILY.md Current accepted deployment evidence
docs/PRODUCTION_STATE_2026-09-03.md  Previous same-day accepted deployment evidence
docs/PRODUCTION_STATE_v0.8.md        Historical accepted v0.8 deployment evidence
docs/PRODUCTION_STATE_v0.9.md        Historical accepted v0.9 deployment evidence
docs/PRODUCTION_STATE_v1.0.md        Historical accepted v1.0 deployment evidence
docs/PRODUCTION_STATE_v1.1.md        Historical accepted v1.1 deployment evidence
docs/PRODUCTION_STATE_v1.2.md        Historical accepted 2026-09-01 v1.2 deployment evidence
LICENSE                              Apache-2.0 software licence text
CONTENT_LICENSE.md                   CC BY 4.0 content/database licence scope
DCO.md                               Developer Certificate of Origin 1.1
GOVERNANCE.md                        Decision rights and protected changes
CONTRIBUTING.md                      Contribution, provenance and rights rules
```

## Validate

```shell
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python scripts/evidence_coverage.py --summary --fail-gaps
python scripts/evidence_source_freshness.py --fail-overdue
python scripts/check_content_freshness.py --fail-overdue
python -m unittest discover -s tests
```

## Public interface boundary

The site remains intentionally semantic, reading-first and privacy-first. All canonical content remains useful without JavaScript. `/find/` adds one bounded same-origin local JavaScript enhancement for deterministic discovery while retaining a useful no-script fallback.

Typed discovery text remains in browser memory and is not submitted in a URL or form request. Evidence inspection adds no second script or query surface: `/evidence/` is statically rendered, and readers can browse it or use their browser's built-in Find in page command. No Evidence query is transmitted, stored, profiled or allowed to alter ordinary `/find/` ranking. The public surface has no accounts, profiling, personalised ranking, analytics, query storage, external search service or AI answer authority. Discovery returns bounded governed routes; generated text does not become a source of truth or bypass governed evidence and uncertainty.

## Licensing

ND Oracle uses a deliberate split licence:

- **software/code:** Apache License 2.0 (`Apache-2.0`), see `LICENSE`;
- **original ND Oracle knowledge content, prose/documentation and applicable database rights:** Creative Commons Attribution 4.0 International (`CC BY 4.0`), see `CONTENT_LICENSE.md`;
- **third-party material:** not relicensed by ND Oracle unless a specific rights notice says otherwise.

The licence grant applies only to rights the relevant contributor or rights-holder is entitled to license. File-specific and item-specific rights notices take precedence. Attribution must not imply endorsement by ND Oracle or its contributors.

Software contributions use the Developer Certificate of Origin 1.1 sign-off process in `DCO.md`. Original content contributions require the parallel rights-and-licensing certification in `CONTRIBUTING.md`. ND Oracle does not require a Contributor Licence Agreement at this stage.
