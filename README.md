# ND Oracle

ND Oracle is a provenance-first knowledge commons for the full neurodiversity ecosystem. It connects concepts and claims to evidence, lived experience, uncertainty, and practical resources—including tools, games, apps, books and media, services, organisations, communities, and accommodations.

This repository is the system of record. The public site at `https://ndoracle.org` is a reading-first window onto validated repository content; it does not replace the repository as the knowledge authority.

## Governing rules

1. Never make the next person rediscover an uncertainty already identified.
2. Every serious question leaves the knowledge system better than it found it.
3. No conclusion without its route back to evidence and uncertainty.
4. Measure success by epistemic work saved, not text produced.

## Current repository state

The current repository and accepted production contain exactly **366 governed objects**:

- 20 reviewed Concept objects;
- 168 reviewed Resource objects;
- 175 reviewed Question objects;
- 3 normalized v0.2 Evidence objects;
- **450 canonical public routes**.

The frozen **UK Reference Baseline v1** remains intact beneath additive international packages. Accepted production now includes:

- **Republic of Ireland Assessment & diagnosis v1**;
- **NHS bulletin promotion v1**;
- completed reference-depth packages for **Books & media, Sleep, Food & eating, and Mobility & travel**;
- **Australia Assessment & diagnosis v1** national orientation;
- **Canada Assessment & diagnosis v1** federal orientation plus explicitly narrower Ontario implementation.

Republic-of-Ireland child ADHD remains deliberately deferred because current first-party evidence still does not justify a strong uniform national access route. Private-provider ranking remains prohibited, and no speculative second Ireland domain was created merely for geographic breadth.

The three implemented non-UK jurisdiction packages — Republic of Ireland, Australia and Canada — have now completed the architecture proof required before geography-schema reconsideration. The result is to **retain additive jurisdiction sidecars**. No core geography schema migration is justified, and mass-country expansion remains prohibited.

Current accepted production was generated from exact source SHA `8e60f264adfda2822312a05e835bc352ef263225` and tree `e287f1a6003724b10ea130ef40d846b9837981de`, then freshly verified at `https://ndoracle.org`. Frozen clinical, privacy, provenance, ranking, Evidence-Layer and AI-authority boundaries remain unchanged.

Resource inclusion is **not endorsement**. A Resource may be listed without an efficacy claim when its identity, access route, intended use, limitations, cost/access notes and conflicts are useful. Serious testable propositions require governed evidence and uncertainty routes.

Question routes use the boundary **Relevant to inspect, not recommended**. They expose bounded current understanding, related governed objects, evidence gaps, dissent and reopening conditions without turning discovery into personalised recommendation.

The current accepted public contract contains **450 canonical routes**. The Evidence Layer remains at 60 governed source records across 49 governed Claims, with **49/49 covered and 0 gaps**.

Assessment & diagnosis preserves the adult/child × autism/ADHD × England/Scotland/Wales/Northern Ireland matrix and UK cross-cutting routes, then adds explicit Republic-of-Ireland, Australia, Canada and Ontario scope through additive sidecars. Discovery retains the frozen 41-route v1.1 registry and 29-route UK Assessment extension, then adds 12 Republic-of-Ireland, 4 Australia and 4 Canada/Ontario bindings for **90 governed scoped routes**. The frozen routing-policy file and ranking weights remain unchanged.

Books & media, Sleep, Food & eating and Mobility & travel are now reference-complete for the declared bounded remit. Evidence-threshold decisions remain visible where completeness would otherwise require invention: media does not become clinical evidence; sleep routes do not diagnose or prescribe; sensory eating, ARFID, pica and dysphagia remain distinct; and transport operator information does not become a quality score.

Relationships & family retains its existing safeguarding, consent, communication and jurisdiction boundaries.

## Production state

Current production is the accepted **Reference depth + international v1** deployment of the `v1.2` public-site builder contract at `https://ndoracle.org`, generated from exact source SHA `8e60f264adfda2822312a05e835bc352ef263225` and tree `e287f1a6003724b10ea130ef40d846b9837981de` by deployment workflow run `33987304421` (run #26).

The generated artifact SHA-256 is `d598e73f1403d11dc668bed209bd0c54218c587d65b3bd51e25215e26c5c2543` and the Cloudflare deployment identity is `https://9784eb1f.nd-oracle.pages.dev`. The workflow verified and preserved the existing Direct Upload project `nd-oracle`, production branch `main`, project subdomain `nd-oracle.pages.dev`, and exact custom-domain set `ndoracle.org`. No Pages-project, DNS, custom-domain, secret or other production-configuration mutation was performed.

Fresh network-backed production verification ran against the canonical domain in workflow run `33987460412` (run #20), job `101363565001`. It revalidated all **366 governed objects**, ran the complete **467-test deployed-source regression suite**, and verified all **450 canonical live routes** plus the governed discovery/evidence and frozen compatibility contracts.

Exact-head candidate acceptance also proved:

- 49/49 governed Claims covered;
- 0 Evidence gaps;
- 60 governed source records with 0 overdue;
- 366 governed objects with 0 overdue;
- Question contract 175;
- Resource contract 168;
- Concept contract 20.

`contracts/current-production.json` is the canonical machine-readable current-production pointer. It references `docs/PRODUCTION_STATE_2026-09-05_REFERENCE_DEPTH_INTERNATIONAL_v1.md`, the human-readable evidence record for this deployment after reconciliation.

`docs/PRODUCTION_STATE_2026-09-04_NHS_BULLETIN_PROMOTION_v1.md`, the Ireland production record, the UK Reference Baseline production record and earlier production-state documents remain frozen historical evidence.

The administrative production-state reconciliation is **not** another deployment. The accepted public artifact remains the exact artifact generated from source SHA `8e60f264adfda2822312a05e835bc352ef263225`.

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
discovery/assessment-diagnosis-australia-v1.json Additive Australia assessment discovery extension
discovery/assessment-diagnosis-canada-v1.json Additive Canada/Ontario assessment discovery extension
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
docs/INTERNATIONAL_PILOT_AUSTRALIA_READINESS_v1.md Australia source-readiness decision
docs/INTERNATIONAL_PILOT_CANADA_READINESS_v1.md Canada source-readiness decision
docs/ASSESSMENT_DIAGNOSIS_AUSTRALIA_SOURCE_MATRIX_v1.md Australia assessment source/jurisdiction matrix
docs/ASSESSMENT_DIAGNOSIS_CANADA_SOURCE_MATRIX_v1.md Canada assessment source/jurisdiction matrix
docs/INTERNATIONAL_THREE_PACKAGE_ARCHITECTURE_REVIEW_v1.md Three-country architecture review
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
docs/PRODUCTION_STATE_2026-09-05_REFERENCE_DEPTH_INTERNATIONAL_v1.md Current accepted deployment evidence
docs/PRODUCTION_STATE_2026-09-04_NHS_BULLETIN_PROMOTION_v1.md Previous accepted deployment evidence
docs/PRODUCTION_STATE_2026-09-04_IRELAND_ASSESSMENT_DIAGNOSIS_v1.md Previous accepted Ireland deployment evidence
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
