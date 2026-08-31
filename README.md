# ND Oracle

ND Oracle is a provenance-first knowledge commons for the full neurodiversity ecosystem. It connects concepts and claims to evidence, lived experience, uncertainty, and practical resources—including tools, games, apps, books and media, services, organisations, communities, and accommodations.

This repository is the system of record. The public site at `https://ndoracle.org` is a reading-first window onto validated repository content; it does not replace the repository as the knowledge authority.

## Governing rules

1. Never make the next person rediscover an uncertainty already identified.
2. Every serious question leaves the knowledge system better than it found it.
3. No conclusion without its route back to evidence and uncertainty.
4. Measure success by epistemic work saved, not text produced.

## Current repository state

The accepted v1.0 authoritative corpus contains exactly 119 governed objects:

- 20 reviewed Concept objects;
- 58 reviewed Resource objects spanning tools/apps, accessibility and AAC, practical guides, games, work/study support, organisations, services, books and media;
- 38 reviewed Question objects that route ordinary practical needs across governed Concepts and Resources;
- 3 governed Evidence objects supporting the bounded claim-bearing Resource pilot.

Resource inclusion is **not endorsement**. A Resource may be listed without an efficacy claim when its identity, access route, intended use, limitations, cost/access notes and conflicts are useful. Serious testable propositions require governed evidence and uncertainty routes; the v1.0 claim-bearing pilot makes those routes visible without turning inclusion into an endorsement.

Question routes use the boundary **Relevant to inspect, not recommended**. They expose a bounded current understanding, related governed objects, adjacent Questions, evidence gaps, dissent and reopening conditions without turning discovery into a personalised recommendation.

Every v0.2 Resource requires at least one typed access locator. HTTPS URLs are enforced for web locators so a public catalogue entry cannot become an unreachable name with no governed route to the thing being described.

v1.0 is a governed-discovery and evidence-depth release. It preserves the accepted reading/navigation surface while adding deterministic ordinary-language discovery at `/find/`, explicit no-answer behaviour, a frozen 50-case discovery benchmark, bounded evidence presentation and improved jurisdiction precision. The accepted public contract is exactly 142 canonical routes.

## Production state

Production is the accepted v1.0 governed-discovery release at `https://ndoracle.org`, deployed from exact main SHA `a0081e7d879e23568792ad5a468250eeb21dd20b` by deployment workflow run `33383848729` (run #15). The generated artifact SHA-256 is `e8155159a1f439e5d8a17e65e1bb960430207ad43e1836959fdb1d48737ded51` and the Cloudflare deployment identity is `https://9c561434.nd-oracle.pages.dev`.

Fresh post-deployment verification ran from a GitHub-hosted runner against the canonical domain in workflow run `33384188012` (run #15), job `99462984077`, from exact source SHA `a0081e7d879e23568792ad5a468250eeb21dd20b`. It passed the complete 305-test regression suite before verifying all 142 canonical routes, all 20 Concept routes, all 58 Resource routes, all 38 Question routes, v1.0 governed discovery/evidence, navigation and frozen compatibility contracts.

See `docs/PRODUCTION_STATE_v1.0.md` for the frozen deployment and live-proof evidence. Historical accepted production states remain recorded separately in their versioned production-state documents.

## Repository map

```text
objects/concepts/                    Reviewed concept objects
objects/resources/                   Reviewed resource objects
objects/questions/                   Reviewed practical question objects
objects/evidence/                    Governed evidence objects
schema/object-v0.1.json              v0.1 concept contract
schema/object-v0.2.json              v0.2 object dispatcher
schema/types/                        v0.2 object-type contracts
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
docs/PRODUCTION_STATE_v1.0.md        Accepted v1.0 deployment and live-proof evidence
GOVERNANCE.md                        Decision rights and protected changes
CONTRIBUTING.md                      Contribution and provenance rules
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

## Licensing status

No reuse licence has yet been selected. Copyright remains with contributors until an owner explicitly adopts a licence. This is recorded as protected governance issue #105 rather than guessed.
