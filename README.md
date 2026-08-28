# ND Oracle

ND Oracle is a provenance-first knowledge commons for the full neurodiversity ecosystem. It connects concepts and claims to evidence, lived experience, uncertainty, and practical resources—including tools, games, apps, books and media, services, organisations, communities, and accommodations.

This repository is the system of record. The public site at `https://ndoracle.org` is a reading-first window onto validated repository content; it does not replace the repository as the knowledge authority.

## Governing rules

1. Never make the next person rediscover an uncertainty already identified.
2. Every serious question leaves the knowledge system better than it found it.
3. No conclusion without its route back to evidence and uncertainty.
4. Measure success by epistemic work saved, not text produced.

## Current repository state

The v0.9 candidate authoritative corpus contains exactly 100 objects:

- 20 reviewed v0.1 Concept objects;
- 50 reviewed v0.2 Resource objects spanning tools/apps, accessibility and AAC, practical guides, games, work/study support, organisations, services, books and media;
- 30 reviewed v0.2 Question objects that route ordinary practical needs across governed Concepts and Resources.

Resource inclusion is **not endorsement**. A Resource may be listed without an efficacy claim when its identity, access route, intended use, limitations, cost/access notes and conflicts are useful. Any efficacy, safety or other serious testable proposition requires its own governed Claim and Evidence route.

Question routes use the boundary **Relevant to inspect, not recommended**. They expose a bounded current understanding, related governed objects, adjacent Questions, evidence gaps, dissent and reopening conditions without turning a listing into a personalised recommendation.

Every v0.2 Resource requires at least one typed access locator. HTTPS URLs are enforced for web locators so a public catalogue entry cannot become an unreachable name with no governed route to the thing being described.

The v0.9 candidate is a content-and-navigation release, not a design release. It adds need-led hubs, browse-by-type, geographic-scope navigation, a complete A–Z, related-question links and a governed freshness gate. With the larger corpus, the candidate public contract is exactly 125 canonical routes. See `docs/CONTENT_NAVIGATION_v0.9.md` and `docs/CONTENT_GAP_MAP_v0.9.md`.

## Production state

Production remains the accepted v0.8 content/navigation release at `https://ndoracle.org`, deployed from exact main SHA `e4a93bbbd579b8a033954300e540a11dafc65f5d` by deployment workflow run `33178697469` (run #12). The generated artifact SHA-256 is `75594181876f422d62fde519ec3db29574bfdd48e6b797df15b940d223597479` and the Cloudflare deployment identity is `https://9b09ce0c.nd-oracle.pages.dev`.

The post-deployment v0.8 verifier passed all 62 canonical routes, all 25 Resource routes, all 14 Question routes, cross-content navigation, the inherited v0.6 reading/resource contracts, the frozen v0.7 five-question compatibility contract, 404, robots, sitemap, Oracle compatibility noindex route, and www redirect behaviour. See `docs/PRODUCTION_STATE_v0.8.md` for the frozen deployment and verification evidence.

The v0.9 candidate does **not** redefine production until its exact `main` SHA is separately authorised, deployed and verified live.

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
docs/CONTENT_NAVIGATION_v0.9.md      100-object/125-route candidate contract
docs/CONTENT_GAP_MAP_v0.9.md         Need-led editorial coverage map
docs/PRODUCTION_STATE_v0.8.md        Accepted v0.8 deployment evidence
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
