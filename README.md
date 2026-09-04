# ND Oracle

ND Oracle is a provenance-first knowledge commons for the full neurodiversity ecosystem. It connects concepts and claims to evidence, lived experience, uncertainty, and practical resources—including tools, games, apps, books and media, services, organisations, communities, and accommodations.

This repository is the system of record. The public site at `https://ndoracle.org` is a reading-first window onto validated repository content; it does not replace the repository as the knowledge authority.

## Governing rules

1. Never make the next person rediscover an uncertainty already identified.
2. Every serious question leaves the knowledge system better than it found it.
3. No conclusion without its route back to evidence and uncertainty.
4. Measure success by epistemic work saved, not text produced.

## Current repository state

The current repository and accepted production contain exactly **319 governed objects**:

- 20 reviewed Concept objects;
- 144 reviewed Resource objects;
- 152 reviewed Question objects;
- 3 normalized v0.2 Evidence objects;
- **403 canonical public routes**.

The frozen **UK Reference Baseline v1** remains intact underneath the first accepted international package: **Republic of Ireland Assessment & diagnosis v1**. The Ireland package adds exactly 4 Questions and 8 reviewed, claimless HSE Resources covering adult autism, child autism, adult ADHD, and the distinction between HSE Assessment of Need and clinical diagnostic assessment. Child ADHD remains deliberately deferred because current first-party evidence does not yet justify a strong uniform national access route.

Current accepted production was generated from exact source SHA `10fe0a0bc1f1a075e420dd0bc432d0a69cc15197` and tree `bce34c6908a409daefce1ba24ce06349fa24cac2`, then freshly verified at `https://ndoracle.org`. Frozen UK discovery, clinical, privacy, provenance, ranking, Evidence-Layer and AI-authority boundaries remain unchanged; Ireland is added through a separate additive jurisdiction extension.

Resource inclusion is **not endorsement**. A Resource may be listed without an efficacy claim when its identity, access route, intended use, limitations, cost/access notes and conflicts are useful. Serious testable propositions require governed evidence and uncertainty routes; the claim-bearing pilot makes those routes visible without turning inclusion into an endorsement.

Question routes use the boundary **Relevant to inspect, not recommended**. They expose a bounded current understanding, related governed objects, adjacent Questions, evidence gaps, dissent and reopening conditions without turning discovery into a personalised recommendation.

Every v0.2 Resource requires at least one typed access locator. HTTPS URLs are enforced for web locators so a public catalogue entry cannot become an unreachable name with no governed route to the thing being described.

The current accepted public contract contains 403 canonical routes. It preserves the v1.2 public-site builder identity, frozen discovery architecture, reading/navigation surface and privacy/static boundaries while exposing the frozen UK Reference Baseline v1 plus the bounded Republic of Ireland Assessment & diagnosis v1 package. The Evidence Layer contributes `/evidence/` plus 60 deterministic Evidence detail projections.

Assessment & diagnosis preserves the accepted adult/child × autism/ADHD × England/Scotland/Wales/Northern Ireland matrix plus its UK cross-cutting routes and now includes four accepted Republic-of-Ireland journeys. England-specific Right to Choose remains contained to England; Northern Ireland HSC/NHS and Republic-of-Ireland HSE routes are explicitly separate; HSE adult autism public/private access, adult ADHD regional rollout and Assessment-of-Need distinctions remain bounded. The Ireland slice adds 8 reviewed, claimless first-party HSE Resources. Discovery keeps the frozen 41-route v1.1 registry and 29-route UK Assessment extension unchanged, then adds 12 exact Republic-of-Ireland scope bindings for 82 governed scoped routes in accepted production. No schema, ranking-weight, clinical-decision, privacy/query-handling, analytics or AI-authority boundary is weakened.

Relationships & family keeps parenting a neurodivergent child separate from support for a neurodivergent or disabled parent; ordinary relationship communication does not displace safeguarding where fear, control, violence or sexual pressure is present; consent remains explicit and revocable; ND Oracle does not diagnose a partner, decide who is right, or decide whether a relationship should continue; and disability-service access preserves the England/Scotland/Wales versus Northern Ireland legal split. The accepted 48-case benchmark was integrated without changing frozen ranking weights.

## Production state

Current production is the accepted **UK Reference Baseline v1 + Republic of Ireland Assessment & diagnosis v1** deployment of the `v1.2` public-site builder contract at `https://ndoracle.org`, generated from exact source SHA `10fe0a0bc1f1a075e420dd0bc432d0a69cc15197` and tree `bce34c6908a409daefce1ba24ce06349fa24cac2` by deployment workflow run `33896144673` (run #24). The generated artifact SHA-256 is `4967f8a711aefeb8bf878de7dba5a18063cd57d0b1ca54e53d6022d9cfe5f033` and the Cloudflare deployment identity is `https://325a78a3.nd-oracle.pages.dev`.

Fresh network-backed production verification ran against the canonical domain in workflow run `33896431576` (run #18), job `101100054619`. It revalidated all 319 governed objects, ran the complete 439-test deployed-source regression suite, and verified all 403 canonical live routes plus the governed discovery/evidence and frozen compatibility contracts. Exact-tree candidate acceptance also proved 49/49 Claim coverage with 0 gaps, 60 governed source records with 0 overdue and 319 governed objects with 0 overdue.

`contracts/current-production.json` is the canonical machine-readable current-production pointer. It references `docs/PRODUCTION_STATE_2026-09-04_IRELAND_ASSESSMENT_DIAGNOSIS_v1.md`, the immutable human-readable evidence record for this deployment after reconciliation. `docs/PRODUCTION_STATE_2026-09-04_UK_REFERENCE_BASELINE_v1.md`, `docs/PRODUCTION_STATE_2026-09-03_RELATIONSHIPS_FAMILY.md`, `docs/PRODUCTION_STATE_2026-09-03.md`, `docs/PRODUCTION_STATE_v1.2.md` and earlier production-state documents remain frozen historical evidence.

The administrative production-state reconciliation is not itself a deployment. The accepted public artifact remains the exact artifact generated from source SHA `10fe0a0bc1f1a075e420dd0bc432d0a69cc15197`.

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
discovery/assessment-diagnosis-ireland-v1.json Additive Republic-of-Ireland assessment discovery extension
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
docs/ASSESSMENT_DIAGNOSIS_IRELAND_v1.md Republic-of-Ireland assessment reference contract
docs/ASSESSMENT_DIAGNOSIS_IRELAND_SOURCE_MATRIX_v1.md Republic-of-Ireland source/jurisdiction matrix
docs/RELATIONSHIPS_FAMILY_UK_v1.md   Relationships & family bounded coverage contract
docs/RELATIONSHIPS_FAMILY_UK_SOURCE_MATRIX_v1.md Relationships & family source matrix
docs/UK_BREADTH_CANDIDATE_v1.md      UK breadth candidate contract and acceptance gates
docs/UK_REFERENCE_BASELINE_v1.md       Frozen UK Reference Baseline v1 content-state record
docs/INTERNATIONAL_EXPANSION_ARCHITECTURE_v1.md International jurisdiction-package architecture and gates
docs/INTERNATIONAL_PILOT_IRELAND_READINESS_v1.md First non-UK pilot source-readiness decision
contracts/international-pilot-ireland-readiness-v1.json Machine-readable Ireland pilot readiness contract
contracts/international-expansion-v1.json Machine-readable international expansion architecture contract
docs/ORGANISATIONS_PEER_COMMUNITY_UK_v1.md Organisations & peer community UK v1 contract
docs/ORGANISATIONS_PEER_COMMUNITY_UK_SOURCE_MATRIX_v1.md Organisations & peer community source/geography matrix
contracts/organisations-peer-community-uk-v1.json Machine-readable leadership/access/moderation/privacy metadata
benchmarks/organisations-peer-community-uk-v1.json Organisations & peer community deterministic/hostile benchmark
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
docs/PRODUCTION_STATE_2026-09-04_IRELAND_ASSESSMENT_DIAGNOSIS_v1.md Current accepted deployment evidence
docs/PRODUCTION_STATE_2026-09-04_UK_REFERENCE_BASELINE_v1.md Previous accepted UK-baseline deployment evidence
docs/PRODUCTION_STATE_2026-09-03_RELATIONSHIPS_FAMILY.md Previous accepted deployment evidence
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
