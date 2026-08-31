# ND Oracle

ND Oracle is a provenance-first knowledge commons for the full neurodiversity ecosystem. It connects concepts and claims to evidence, lived experience, uncertainty, and practical resources—including tools, games, apps, books and media, services, organisations, communities, and accommodations.

This repository is the system of record. The public site at `https://ndoracle.org` is a reading-first window onto validated repository content; it does not replace the repository as the knowledge authority.

## Governing rules

1. Never make the next person rediscover an uncertainty already identified.
2. Every serious question leaves the knowledge system better than it found it.
3. No conclusion without its route back to evidence and uncertainty.
4. Measure success by epistemic work saved, not text produced.

## Current repository state

The accepted v1.1 authoritative corpus contains exactly 119 governed objects:

- 20 reviewed Concept objects;
- 58 reviewed Resource objects spanning tools/apps, accessibility and AAC, practical guides, games, work/study support, organisations, services, books and media;
- 38 reviewed Question objects that route ordinary practical needs across governed Concepts and Resources;
- 3 governed Evidence objects supporting the bounded claim-bearing Resource pilot.

Resource inclusion is **not endorsement**. A Resource may be listed without an efficacy claim when its identity, access route, intended use, limitations, cost/access notes and conflicts are useful. Serious testable propositions require governed evidence and uncertainty routes; the claim-bearing pilot makes those routes visible without turning inclusion into an endorsement.

Question routes use the boundary **Relevant to inspect, not recommended**. They expose a bounded current understanding, related governed objects, adjacent Questions, evidence gaps, dissent and reopening conditions without turning discovery into a personalised recommendation.

Every v0.2 Resource requires at least one typed access locator. HTTPS URLs are enforced for web locators so a public catalogue entry cannot become an unreachable name with no governed route to the thing being described.

v1.1 preserves the accepted v1.0 corpus, reading/navigation surface, evidence presentation and 142-route public contract while hardening deterministic ordinary-language discovery. The v1.1 policy adds a compositional personal clinical-decision boundary, explicit requested-jurisdiction containment, meaningful lexical eligibility, governed route-scope provenance fingerprints and Python/browser decision-trace parity. Orientation remains disabled because ablation showed it was unnecessary. No knowledge objects or schemas changed for v1.1.

## Production state

Production is the accepted v1.1 bounded-discovery release at `https://ndoracle.org`, deployed from exact main SHA `3032305dd81d48b2c6cc777b72f038267f995819` by deployment workflow run `33425750168` (run #16). The generated artifact SHA-256 is `84f6ac3e76d07d26367794b87cf6f85736aa4d8e976865d2d79a806bd429dfb7` and the Cloudflare deployment identity is `https://29c88484.nd-oracle.pages.dev`.

Fresh post-deployment verification ran from a GitHub-hosted runner against the canonical domain in workflow run `33426342672` (run #16), job `99600728836`, from exact source SHA `3032305dd81d48b2c6cc777b72f038267f995819`. It passed the complete 322-test regression suite before verifying all 142 canonical routes, all 20 Concept routes, all 58 Resource routes, all 38 Question routes, the v1.1 bounded discovery contract, governed evidence, navigation and frozen public compatibility contracts.

See `docs/PRODUCTION_STATE_v1.1.md` for the accepted v1.1 deployment and live-proof evidence. Historical accepted production states remain recorded separately in their versioned production-state documents, including `docs/PRODUCTION_STATE_v1.0.md`.

## Repository map

```text
objects/concepts/                    Reviewed concept objects
objects/resources/                   Reviewed resource objects
objects/questions/                   Reviewed practical question objects
objects/evidence/                    Governed evidence objects
schema/object-v0.1.json              v0.1 concept contract
schema/object-v0.2.json              v0.2 object dispatcher
schema/types/                        v0.2 object-type contracts
discovery/routing-policy-v1.1.json   Shared deterministic v1.1 discovery policy
site/                                Static public site source
scripts/validate.py                  Schema, governance-route, and graph checks
scripts/check_content_freshness.py   Review-age/freshness gate
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
docs/PRODUCTION_STATE_v0.8.md        Historical accepted v0.8 deployment evidence
docs/PRODUCTION_STATE_v0.9.md        Historical accepted v0.9 deployment evidence
docs/PRODUCTION_STATE_v1.0.md        Historical accepted v1.0 deployment evidence
docs/PRODUCTION_STATE_v1.1.md        Accepted v1.1 deployment and live-proof evidence
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
python scripts/check_content_freshness.py --fail-overdue
python -m unittest discover -s tests
```

## Public interface boundary

The site remains intentionally semantic, reading-first and privacy-first. All canonical content remains useful without JavaScript. `/find/` adds one bounded same-origin local JavaScript enhancement for deterministic discovery while retaining a useful no-script fallback.

Typed discovery text remains in browser memory and is not submitted in a URL or form request. The public surface has no accounts, profiling, personalised ranking, analytics, query storage, external search service or AI answer authority. Discovery returns bounded governed routes; generated text does not become a source of truth or bypass governed evidence and uncertainty.

## Licensing

ND Oracle uses a deliberate split licence:

- **software/code:** Apache License 2.0 (`Apache-2.0`), see `LICENSE`;
- **original ND Oracle knowledge content, prose/documentation and applicable database rights:** Creative Commons Attribution 4.0 International (`CC BY 4.0`), see `CONTENT_LICENSE.md`;
- **third-party material:** not relicensed by ND Oracle unless a specific rights notice says otherwise.

The licence grant applies only to rights the relevant contributor or rights-holder is entitled to license. File-specific and item-specific rights notices take precedence. Attribution must not imply endorsement by ND Oracle or its contributors.

Software contributions use the Developer Certificate of Origin 1.1 sign-off process in `DCO.md`. Original content contributions require the parallel rights-and-licensing certification in `CONTRIBUTING.md`. ND Oracle does not require a Contributor Licence Agreement at this stage.