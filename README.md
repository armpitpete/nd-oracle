# ND Oracle

ND Oracle is a provenance-first knowledge commons for the full neurodiversity ecosystem. It connects concepts and claims to evidence, lived experience, uncertainty, and practical resources—including tools, games, apps, books and media, services, organisations, communities, and accommodations.

This repository is the system of record. The public site at `https://ndoracle.org` is a reading-first window onto validated repository content; it does not replace the repository as the knowledge authority.

## Governing rules

1. Never make the next person rediscover an uncertainty already identified.
2. Every serious question leaves the knowledge system better than it found it.
3. No conclusion without its route back to evidence and uncertainty.
4. Measure success by epistemic work saved, not text produced.

## Current repository state

The accepted v0.9 authoritative corpus contains exactly 100 objects:

- 20 reviewed v0.1 Concept objects;
- 50 reviewed v0.2 Resource objects spanning tools/apps, accessibility and AAC, practical guides, games, work/study support, organisations, services, books and media;
- 30 reviewed v0.2 Question objects that route ordinary practical needs across governed Concepts and Resources.

Resource inclusion is **not endorsement**. A Resource may be listed without an efficacy claim when its identity, access route, intended use, limitations, cost/access notes and conflicts are useful. Any efficacy, safety or other serious testable proposition requires its own governed Claim and Evidence route.

Question routes use the boundary **Relevant to inspect, not recommended**. They expose a bounded current understanding, related governed objects, adjacent Questions, evidence gaps, dissent and reopening conditions without turning a listing into a personalised recommendation.

Every v0.2 Resource requires at least one typed access locator. HTTPS URLs are enforced for web locators so a public catalogue entry cannot become an unreachable name with no governed route to the thing being described.

v0.9 is a content-and-navigation release, not a design release. It adds need-led hubs, browse-by-type, geographic-scope navigation, a complete A–Z, related-question links and a governed freshness gate. The accepted public contract is exactly 125 canonical routes. See `docs/CONTENT_NAVIGATION_v0.9.md` and `docs/CONTENT_GAP_MAP_v0.9.md`.

## Production state

Production is the accepted v0.9 content/navigation release at `https://ndoracle.org`, deployed from exact main SHA `286c1999a27509e74da2c70e5076fbdcda46e1a1` by deployment workflow run `33204071981` (run #14). The generated artifact SHA-256 is `e13ed02c4f6794844fa6b2930937bdada772f0d15330290972acfc761b505076` and the Cloudflare deployment identity is `https://74c14b3d.nd-oracle.pages.dev`.

Fresh post-deployment verification ran from a GitHub-hosted runner against the canonical domain in workflow run `33204284355` (run #173), job `98961250853`. It passed all 125 canonical routes, all 20 Concept routes, all 50 Resource routes, all 30 Question routes, need/type/place/A–Z navigation, the accepted v0.8 object-set compatibility layer, inherited v0.6 reading/resource contracts, the frozen v0.7 five-question homepage/discovery contract, 404, robots, sitemap, Oracle compatibility noindex route and www redirect behaviour. The proof run completed with all 315 tests passing.

The initial v0.9 upload from SHA `5665f8a988fe3ba58da1fd111ce45067668d9721` was deliberately not accepted after live verification exposed a two-link homepage compatibility regression. PR #95 repaired it before the accepted deployment. See `docs/PRODUCTION_STATE_v0.9.md` for the frozen deployment, repair and verification evidence.

## Repository map

```text
objects/concepts/                    Reviewed concept objects
objects/resources/                   Reviewed resource objects
objects/questions/                   Reviewed practical question objects
schema/object-v0.1.json              v0.1 concept contract
schema/object-v0.2.json              v0.2 six-object dispatcher
schema/types/                        v0.2 object-type contracts
site/                                Static public site source
scripts/validate.py                  Schema, governance-route, and graph checks
scripts/check_content_freshness.py   Review-age/freshness gate
scripts/build_site.py                Current reading-first static site generator
scripts/build_site_v08.py            Preserved v0.8 builder code
scripts/verify_live_site.py          Current production HTTP/content verifier
scripts/verify_live_site_v08.py      Preserved v0.8 verifier code
docs/ECOSYSTEM_PUBLICATION_v0.6.md   Ecosystem publication contract
docs/PUBLIC_QUESTION_DISCOVERY_v0.7.md Question-led discovery contract
docs/CONTENT_NAVIGATION_v0.8.md      Accepted v0.8 findability contract
docs/CONTENT_NAVIGATION_v0.9.md      Accepted 100-object/125-route contract
docs/CONTENT_GAP_MAP_v0.9.md         Need-led editorial coverage map
docs/PRODUCTION_STATE_v0.8.md        Historical accepted v0.8 deployment evidence
docs/PRODUCTION_STATE_v0.9.md        Accepted v0.9 deployment and live-proof evidence
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

The site remains intentionally semantic, reading-first, privacy-first, and functional without JavaScript. The ecosystem and question-led discovery layers add static routes over governed repository content without accounts, profiling, recommendation scoring, personalised ranking, analytics, query storage or an AI answer surface.

A later free-text Oracle discovery layer may route ordinary questions across the knowledge graph, but generated answers must never become the source of truth or bypass governed evidence and uncertainty.

## Licensing status

No reuse licence has yet been selected. Copyright remains with contributors until an owner explicitly adopts a licence. This is recorded as an open governance decision rather than guessed.
