# ND Oracle

ND Oracle is a provenance-first knowledge commons for the full neurodiversity ecosystem. It connects concepts and claims to evidence, lived experience, uncertainty, and practical resources—including tools, games, apps, books and media, services, organisations, communities, and accommodations.

This repository is the system of record. The public site at `https://ndoracle.org` is a reading-first window onto validated repository content; it does not replace the repository as the knowledge authority.

## Governing rules

1. Never make the next person rediscover an uncertainty already identified.
2. Every serious question leaves the knowledge system better than it found it.
3. No conclusion without its route back to evidence and uncertainty.
4. Measure success by epistemic work saved, not text produced.

## Current repository state

The authoritative corpus currently contains 30 objects:

- 10 reviewed v0.1 Concept objects covering Neurodiversity, Autism, ADHD, Executive function, Sensory processing, Dyslexia, Developmental co-ordination disorder, Tourette syndrome, Learning disability and Developmental language disorder;
- 15 reviewed v0.2 Resource objects spanning tools/apps, games, workplace support, organisations and books;
- 5 reviewed v0.2 Question objects that route ordinary practical needs across governed Concepts and Resources.

Resource inclusion is **not endorsement**. A Resource may be listed without an efficacy claim when its identity, access route, intended use, limitations, cost/access notes and conflicts are useful. Any efficacy, safety or other serious testable proposition requires its own governed Claim and Evidence route.

Question routes use the boundary **Relevant to inspect, not recommended**. They expose a bounded current understanding, related governed objects, evidence gaps, dissent and reopening conditions without turning a listing into a personalised recommendation.

Every v0.2 Resource requires at least one typed access locator. HTTPS URLs are enforced for web locators so a public catalogue entry cannot become an unreachable name with no governed route to the thing being described.

## Production state

Production is the accepted v0.7 question-led discovery release at `https://ndoracle.org`, deployed from exact main SHA `a074b6da26f95f58f15f38e44ae2b7a43fe6383c` by deployment workflow run `33174604415` (run #11). The generated artifact SHA-256 is `f987e707af2df3551a3a8657d03c8b67be91209b09d948206d2c0963557e923b` and the Cloudflare deployment identity is `https://b7b9549a.nd-oracle.pages.dev`.

The post-deployment v0.7 verifier passed all 42 canonical routes, all 15 Resource routes, all 5 Question routes, the inherited v0.6 reading/resource contracts, the v0.7 question-led discovery contract, 404, robots, sitemap, Oracle compatibility noindex route, and www redirect behaviour. See `docs/PRODUCTION_STATE_v0.7.md` for the frozen deployment and verification evidence.

## Repository map

```text
objects/concepts/                  Reviewed concept objects
objects/resources/                 Reviewed resource objects
objects/questions/                 Reviewed practical question objects
schema/object-v0.1.json            v0.1 concept contract
schema/object-v0.2.json            v0.2 six-object dispatcher
schema/types/                      v0.2 object-type contracts
site/                              Static public site source
scripts/validate.py                Schema, governance-route, and graph checks
scripts/build_site.py              Reading-first static site generator
scripts/verify_live_site.py        Production HTTP/reading/discovery verifier
docs/ECOSYSTEM_PUBLICATION_v0.6.md Ecosystem publication contract
docs/PUBLIC_QUESTION_DISCOVERY_v0.7.md Question-led discovery contract
docs/PRODUCTION_STATE_v0.7.md      Accepted v0.7 deployment evidence
GOVERNANCE.md                      Decision rights and protected changes
CONTRIBUTING.md                    Contribution and provenance rules
```

## Validate

```shell
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests
```

## Public interface boundary

The site remains intentionally semantic, reading-first, privacy-first, and functional without JavaScript. The ecosystem and question-led discovery layers add static routes over governed repository content without accounts, profiling, recommendation scoring, personalised ranking, analytics, query storage or an AI answer surface.

A later free-text Oracle discovery layer may route ordinary questions across the knowledge graph, but generated answers must never become the source of truth or bypass governed evidence and uncertainty.

## Licensing status

No reuse licence has yet been selected. Copyright remains with contributors until an owner explicitly adopts a licence. This is recorded as an open governance decision rather than guessed.
